#!/usr/bin/env python3
"""
folio render — paged HTML → PDF → page PNGs → spread contact sheet.

Usage
  python render.py brochure.html                     # PDF + PNGs + contact sheet into ./out
  python render.py brochure.html --out build --bleed 3   # print PDF with 3 mm bleed
  python render.py brochure.html --no-editable       # skip the editable page-embedded HTML
  python render.py brochure.html --pages 1-4         # previews for a subset (PDF is always full)
  python render.py poster.html --png-only --dpi 300  # posters: PNGs + editable HTML only, no PDF

Outputs (in --out, default ./out next to the HTML)
  <name>.pdf            the PDF (trim size, or trim+bleed with --bleed)
  pages/p-001.png ...   one PNG per page, cropped to trim, for looking at every page
  contact.png           reader's-spread contact sheet (cover alone, then 2–3, 4–5 …)
  <name>.editable.html  flat, page-embedded, editable HTML (FD / Canva-import format) — made by
                        editable.py on every render, with a fidelity check against the original

Requires: playwright (chromium), pypdfium2, pillow.
"""
import argparse, json, sys
from pathlib import Path

MM_PER_PX = 25.4 / 96.0


def parse_range(spec, n):
    if not spec:
        return list(range(n))
    out = set()
    for part in spec.split(","):
        if "-" in part:
            a, b = part.split("-")
            out.update(range(int(a) - 1, min(int(b), n)))
        else:
            out.add(int(part) - 1)
    return sorted(i for i in out if 0 <= i < n)


def load(page, html_path):
    page.goto(html_path.resolve().as_uri(), wait_until="load")
    page.evaluate("document.fonts.ready.then(() => true)")
    page.wait_for_function(
        "Array.from(document.images).every(i => i.complete)", timeout=60000)


def page_geometry(page):
    """Trim and bleed in mm, read from the first .page element."""
    return page.evaluate("""() => {
      const p = document.querySelector('.page');
      if (!p) return null;
      const r = p.getBoundingClientRect();
      const t = p.querySelector('.trim');
      const tr = t ? t.getBoundingClientRect() : r;
      return { w: r.width, h: r.height, bleed: (tr.left - r.left),
               count: document.querySelectorAll('.page').length };
    }""")


def render(args):
    from playwright.sync_api import sync_playwright
    html = Path(args.html)
    out = Path(args.out) if args.out else html.parent / "out"
    (out / "pages").mkdir(parents=True, exist_ok=True)
    name = html.stem

    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page()
        load(page, html)
        if args.bleed:
            page.add_style_tag(content=f":root{{--bleed:{args.bleed}mm !important}}")
        geo = page_geometry(page)
        if not geo:
            sys.exit("No .page elements found — is this a folio document?")
        w_mm, h_mm = geo["w"] * MM_PER_PX, geo["h"] * MM_PER_PX
        bleed_mm = geo["bleed"] * MM_PER_PX
        page.add_style_tag(content=f"@page {{ size: {w_mm:.3f}mm {h_mm:.3f}mm; margin: 0 }}"
                                   " @media print { .page { margin: 0 !important; box-shadow: none !important; } }")
        page.emulate_media(media="print")
        if args.png_only:  # posters: the PDF is only the rasteriser's input
            import tempfile
            tmp = Path(tempfile.mkdtemp())
            pdf_path = tmp / f"{name}.pdf"
        else:
            pdf_path = out / f"{name}.pdf"
        page.pdf(path=str(pdf_path), prefer_css_page_size=True, print_background=True)
        browser.close()

    # ---- rasterise ----
    import pypdfium2 as pdfium
    from PIL import Image
    doc = pdfium.PdfDocument(str(pdf_path))
    n = len(doc)
    if n != geo["count"]:
        print(f"WARNING: PDF has {n} pages but the HTML has {geo['count']} .page elements "
              "— something is overflowing its page box (check heights / break-after).")
    scale = args.dpi / 72.0
    crop_px = bleed_mm / 25.4 * args.dpi
    pngs = []
    for i in parse_range(args.pages, n):
        img = doc[i].render(scale=scale).to_pil().convert("RGB")
        if crop_px > 0.5:
            c = round(crop_px)
            img = img.crop((c, c, img.width - c, img.height - c))
        p = out / "pages" / f"p-{i+1:03d}.png"
        img.save(p, dpi=(args.dpi, args.dpi))
        pngs.append((i, p))
    doc.close()  # Windows keeps the file locked while pdfium holds it

    contact = contact_sheet(pngs, out / "contact.png", single=args.single or args.png_only)

    result = {"pdf": str(pdf_path), "pages": n, "trim_mm": [round(w_mm - 2 * bleed_mm, 2), round(h_mm - 2 * bleed_mm, 2)],
              "bleed_mm": round(bleed_mm, 2), "previews": str(out / "pages"), "contact": str(contact)}
    if args.png_only:
        import shutil
        sys.path.insert(0, str(Path(__file__).parent))
        from preflight import pdf_checks
        fonts = []
        pdf_checks(pdf_path, fonts)  # the fallback-font check still runs on the throwaway PDF
        if fonts: result["pdf_font_issues"] = [f["msg"] for f in fonts]
        shutil.rmtree(pdf_path.parent, ignore_errors=True)
        del result["pdf"]

    if not args.no_editable:
        import subprocess
        ed = subprocess.run([sys.executable, str(Path(__file__).with_name("editable.py")), str(html), "--out", str(out),
                             "--max-mb", str(args.max_mb)] + (["--no-check"] if args.pages else []), capture_output=True, text=True)
        try:
            er = json.loads(ed.stdout)
            result["editable"] = er["editable"]
            result["editable_mb"] = er.get("size_mb")
            result["editable_fidelity_pct"] = er.get("fidelity_pct")
            if er.get("check_pages"): result["editable_check_pages"] = er["check_pages"]; result["editable_diff"] = er.get("diff_sheet")
            if er.get("warnings"): result["editable_warnings"] = er["warnings"]
        except Exception:
            result["editable_error"] = (ed.stderr or ed.stdout)[-800:]
    print(json.dumps(result, indent=2))


def contact_sheet(pngs, dest, single=False, thumb_h=620, gap=36, bg=(203, 205, 209)):
    """Lay pages out as a reader sees them: cover alone on the right, then spreads.
    Single sheets (posters, flyers) pack left to right, one slot each.
    >>> import tempfile, os; from PIL import Image; d = tempfile.mkdtemp()
    >>> pngs = [(i, os.path.join(d, f"{i}.png")) for i in range(4)]
    >>> _ = [Image.new("RGB", (100, 141)).save(f) for _, f in pngs]
    >>> [Image.open(contact_sheet(pngs, os.path.join(d, n), single=s, thumb_h=141)).size[0] for n, s in (("s.png", True), ("b.png", False))]
    [580, 744]
    """
    from PIL import Image, ImageDraw, ImageFilter
    if not pngs:
        return None
    imgs = {i: Image.open(p) for i, p in pngs}
    w0, h0 = next(iter(imgs.values())).size
    tw = round(w0 * thumb_h / h0)
    # group into spreads by absolute page index
    rows = []
    if single:
        rows = [[i] for i in sorted(imgs)]
    else:
        spreads = {}
        for i in imgs:
            key = 0 if i == 0 else (i + 1) // 2
            spreads.setdefault(key, []).append(i)
        rows = [sorted(v) for _, v in sorted(spreads.items())]
    per_line = min(3 if not single else 6, len(rows))
    lines = [rows[k:k + per_line] for k in range(0, len(rows), per_line)]
    sw = tw if single else 2 * tw  # single sheets get a one-page slot, not half a spread
    W = gap + per_line * (sw + gap)

    def slot_x(i, x, spread):
        if single or (len(spread) == 1 and i == 0):
            return x if single else x + tw
        return x if i % 2 == 1 else x + tw  # verso left, recto right
    H = gap + len(lines) * (thumb_h + gap + 18)
    sheet = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(sheet)
    for li, line in enumerate(lines):
        y = gap + li * (thumb_h + gap + 18)
        for si, spread in enumerate(line):
            x = gap + si * (sw + gap)
            # shadow
            shadow = Image.new("RGBA", (sw + 30, thumb_h + 30), (0, 0, 0, 0))
            ImageDraw.Draw(shadow).rectangle((15, 20, 15 + sw, 20 + thumb_h), fill=(0, 0, 0, 70))
            shadow = shadow.filter(ImageFilter.GaussianBlur(9))
            for i in spread:
                px = slot_x(i, x, spread)
                sheet.paste(shadow.crop((0, 0, tw + 30, thumb_h + 30)), (px - 15, y - 15), shadow.crop((0, 0, tw + 30, thumb_h + 30)))
            for i in spread:
                px = slot_x(i, x, spread)
                t = imgs[i].resize((tw, thumb_h), Image.LANCZOS)
                sheet.paste(t, (px, y))
                d.text((px + 4, y + thumb_h + 4), f"{i+1}", fill=(70, 72, 78))
            if len(spread) == 2:  # spine shading
                g = Image.new("L", (24, thumb_h), 0)
                for gx in range(24):
                    g.paste(int(55 * (1 - abs(gx - 12) / 12)), (gx, 0, gx + 1, thumb_h))
                sheet.paste((0, 0, 0), (x + tw - 12, y, x + tw + 12, y + thumb_h), g)
    sheet.save(dest)
    return dest


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")  # Windows consoles default to cp1252 and crash on ■ — “
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("html")
    ap.add_argument("--out")
    ap.add_argument("--bleed", type=float, default=0, help="bleed in mm for the print PDF (usually 3)")
    ap.add_argument("--dpi", type=int, default=110, help="preview PNG resolution")
    ap.add_argument("--pages", help="preview subset, e.g. 1-4,9")
    ap.add_argument("--single", action="store_true", help="contact sheet of single pages (posters, flyers)")
    ap.add_argument("--no-editable", action="store_true", help="skip the editable page-embedded HTML export")
    ap.add_argument("--max-mb", type=float, default=8, help="size budget for the editable HTML (Canva import); default 8")
    ap.add_argument("--png-only", action="store_true", help="posters/social: deliver PNGs + editable HTML, no PDF (implies --single; use --dpi 300 for print)")
    ap.add_argument("--canva", action="store_true", help=argparse.SUPPRESS)  # legacy flag; editable export is now default
    render(ap.parse_args())
