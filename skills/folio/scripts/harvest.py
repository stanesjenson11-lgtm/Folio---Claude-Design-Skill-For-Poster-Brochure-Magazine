#!/usr/bin/env python3
"""
folio harvest — pull everything reusable out of an existing brochure PDF for a redesign.

Usage
  python harvest.py old.pdf --out harvest
  python harvest.py old.pdf --out harvest --overrides harvest/crops.json   # re-crop after QA

Writes
  harvest/native/p03-02.jpg   the embedded photo at its native resolution, UNCLIPPED
                              (the whole original photo — best source for a fresh crop)
  harvest/visible/p03-02.jpg  what the old layout actually showed (page render ∩ placement box)
  harvest/crops.png           contact sheet of every visible crop, labelled — LOOK AT IT
  harvest/text/p03.txt        text per page, reading order
  harvest/manifest.json       per image: page, placement box (mm), native px, effective ppi
  harvest/tokens.json         most-used fill colours and fonts (a starting point for extract)

Why both native and visible: a placement box is not the visible area. Old layouts clip photos
with masks, so a box-based crop can drag in captions, GPS watermarks or slivers of the
neighbouring photo, while the native image may contain things the old designer hid.
Look at crops.png, then decide per image: re-crop the native file (preferred) or keep the
visible crop. Record decisions in crops.json: {"p03-02": {"source": "native", "box_pct": [x0, y0, x1, y1]}}.
"""
import argparse, json
from collections import Counter
from pathlib import Path

PT_MM = 25.4 / 72


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pdf")
    ap.add_argument("--out", default="harvest")
    ap.add_argument("--dpi", type=int, default=300)
    ap.add_argument("--min-mm", type=float, default=12, help="skip images smaller than this on the page (icons)")
    ap.add_argument("--overrides")
    a = ap.parse_args()

    import pypdfium2 as pdfium
    import pypdfium2.raw as raw
    import pdfplumber
    from PIL import Image, ImageDraw

    out = Path(a.out)
    for d in ("native", "visible", "text"):
        (out / d).mkdir(parents=True, exist_ok=True)
    overrides = json.loads(Path(a.overrides).read_text()) if a.overrides else {}

    doc = pdfium.PdfDocument(a.pdf)
    manifest, colours, fonts = [], Counter(), Counter()
    scale = a.dpi / 72

    with pdfplumber.open(a.pdf) as plumb:
        for pi, page in enumerate(doc):
            pno = pi + 1
            W, H = page.get_size()
            render = None
            k = 0
            for obj in page.get_objects(filter=[raw.FPDF_PAGEOBJ_IMAGE], max_depth=4):
                l, b, r, t = obj.get_bounds()
                # clip to page
                l, b, r, t = max(l, 0), max(b, 0), min(r, W), min(t, H)
                if (r - l) * PT_MM < a.min_mm or (t - b) * PT_MM < a.min_mm:
                    continue
                k += 1
                key = f"p{pno:02d}-{k:02d}"
                nat_path, npx = None, None
                try:
                    obj.extract(str(out / "native" / key), fb_render=False)
                    nat_path = next((out / "native").glob(key + ".*"))
                    npx = Image.open(nat_path).size
                except Exception:
                    try:
                        bm = obj.get_bitmap(render=False).to_pil().convert("RGB")
                        nat_path = out / "native" / f"{key}.png"; bm.save(nat_path); npx = bm.size
                    except Exception:
                        pass
                if render is None:
                    render = page.render(scale=scale).to_pil().convert("RGB")
                box = (round(l * scale), round((H - t) * scale), round(r * scale), round((H - b) * scale))
                ov = overrides.get(key)
                vis = render.crop(box)
                if ov and ov.get("source") == "native" and nat_path and ov.get("box_pct"):
                    im = Image.open(nat_path); x0, y0, x1, y1 = ov["box_pct"]
                    vis = im.crop((int(x0 * im.width), int(y0 * im.height), int(x1 * im.width), int(y1 * im.height)))
                elif ov and ov.get("box_pct"):
                    x0, y0, x1, y1 = ov["box_pct"]
                    vis = vis.crop((int(x0 * vis.width), int(y0 * vis.height), int(x1 * vis.width), int(y1 * vis.height)))
                vis_path = out / "visible" / f"{key}.jpg"
                vis.convert("RGB").save(vis_path, quality=92)
                w_mm, h_mm = (r - l) * PT_MM, (t - b) * PT_MM
                manifest.append({
                    "key": key, "page": pno,
                    "box_mm": [round(l * PT_MM, 1), round((H - t) * PT_MM, 1), round(w_mm, 1), round(h_mm, 1)],
                    "native": str(nat_path) if nat_path else None, "native_px": npx,
                    "effective_ppi_in_old_layout": round(npx[0] / (w_mm / 25.4)) if npx else None,
                    "max_print_mm_at_250ppi": [round(npx[0] / 250 * 25.4), round(npx[1] / 250 * 25.4)] if npx else None,
                    "visible": str(vis_path),
                })
            pp = plumb.pages[pi]
            (out / "text" / f"p{pno:02d}.txt").write_text(pp.extract_text() or "", encoding="utf-8")
            for rect in pp.rects:
                c = rect.get("non_stroking_color")
                if c and isinstance(c, (list, tuple)) and len(c) in (1, 3, 4):
                    area = (rect["x1"] - rect["x0"]) * (rect["bottom"] - rect["top"])
                    colours[hexify(c)] += int(area)
            for ch in pp.chars[:4000]:
                fonts[ch.get("fontname", "?").split("+")[-1]] += 1

    (out / "manifest.json").write_text(json.dumps(manifest, indent=2))
    (out / "tokens.json").write_text(json.dumps({
        "fill_colours_by_area": colours.most_common(12),
        "fonts_by_glyph_count": fonts.most_common(10)}, indent=2))
    sheet(manifest, out / "crops.png")
    print(json.dumps({"images": len(manifest), "pages": len(doc), "out": str(out),
                      "look_at": str(out / "crops.png")}, indent=2))


def hexify(c):
    if len(c) == 1:
        v = round(c[0] * 255); return f"#{v:02x}{v:02x}{v:02x}"
    if len(c) == 4:
        C, M, Y, K = c; rgb = [round(255 * (1 - x) * (1 - K)) for x in (C, M, Y)]
    else:
        rgb = [round(x * 255) for x in c]
    return "#" + "".join(f"{max(0, min(255, v)):02x}" for v in rgb)


def sheet(manifest, dest, th=220, cols=6):
    from PIL import Image, ImageDraw
    if not manifest:
        return
    rows = (len(manifest) + cols - 1) // cols
    S = Image.new("RGB", (cols * (th + 20) + 20, rows * (th + 44) + 20), (235, 236, 239))
    d = ImageDraw.Draw(S)
    for i, m in enumerate(manifest):
        im = Image.open(m["visible"]); im.thumbnail((th, th))
        x = 20 + (i % cols) * (th + 20); y = 20 + (i // cols) * (th + 44)
        S.paste(im, (x, y))
        d.text((x, y + th + 4), f"{m['key']}  {m['native_px'][0] if m['native_px'] else '?'}px", fill=(40, 40, 40))
    S.save(dest)


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")  # Windows consoles default to cp1252 and crash on ■ — “
    main()
