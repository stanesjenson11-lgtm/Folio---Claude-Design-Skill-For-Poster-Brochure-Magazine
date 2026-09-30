#!/usr/bin/env python3
"""
folio kits — the style catalogue: finished, signed-off pieces saved as reusable magazine/brochure styles.

  list                          print the catalogue (kits/INDEX.md)
  new <id> <project> [--brand #hex] [--accent #hex] [--name mag]
                                start a piece from a kit: copies the pages, styles and vector assets, fetches the fonts,
                                swaps the kit's theme colours for the client's, marks every sample text and photo
                                data-kit-sample (preflight ERRORs until each is replaced) and writes SLOTS.md
  save <project> <id> [--name "Pop Stripe"] [--family pop] [--html x.html]
                                turn a finished build into a kit: pages + css + svg assets (photos become slot frames),
                                preview.jpg from out/contact.png, KIT.md skeleton, INDEX.md row
  gallery                       rebuild GALLERY.png from every preview
  home                          print the folio home (user kits, TASTE.md, saved client brands in clients/<slug>/)

Where kits live: the shipped catalogue is <skill>/kits. Kits a user saves go to their folio home (FOLIO_HOME, else the
plugin's data folder $CLAUDE_PLUGIN_DATA, else ~/.folio) so plugin updates never wipe them; their commands go to
~/.claude/commands/folio-<name>.md. Working from the git checkout (the maintainer), or with --builtin, save writes into
<skill>/kits and <plugin>/commands instead, so the public plugin learns the style.

A kit is kits/<id>/: KIT.md (front matter: id, name, family, size, pages, render, fonts, theme), kit.html, kit.css,
assets/*.svg (+ small textures), preview.jpg. No client photos ship with a kit.
"""
import argparse, os, re, shutil, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KITS = ROOT / "kits"
HOME = Path(os.environ.get("FOLIO_HOME") or os.environ.get("CLAUDE_PLUGIN_DATA") or Path.home() / ".folio")
USER_KITS = HOME / "kits"
SCRIPTS = ROOT / "scripts"
TEXT_TAGS = "p|h1|h2|h3|h4|h5|h6|li|span|figcaption|a|td|th|blockquote|dt|dd"
# ponytail: the Simple Icons slugs folio has used; a kit with other logos lists them in KIT.md
LOGOS = ("react|angular|vuedotjs|nextdotjs|nodedotjs|python|openjdk|dotnet|php|flutter|swift|android|apple|amazonwebservices|"
         "microsoftazure|googlecloud|docker|kubernetes|postgresql|mongodb|mysql|astro|tailwindcss|wordpress|woocommerce|shopify|stripe|firebase")
SLOT = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" preserveAspectRatio="xMidYMid slice"><rect width="400" height="300" fill="#D9DBE0"/>'
        '<g fill="none" stroke="#A9ADB6" stroke-width="6"><rect x="150" y="105" width="100" height="72" rx="10"/><circle cx="200" cy="141" r="20"/>'
        '<path d="M175 105l8-14h34l8 14"/></g></svg>')


def meta(kit):
    """Front matter of KIT.md as a dict.
    >>> import tempfile; d = Path(tempfile.mkdtemp()); _ = (d / "KIT.md").write_text("---\\nid: x\\nfonts: A:400; B:700\\n---\\n# X")
    >>> meta(d)["fonts"]
    'A:400; B:700'
    """
    m = re.match(r"---\n(.*?)\n---", (Path(kit) / "KIT.md").read_text(encoding="utf-8"), re.S)
    return dict(re.findall(r"^(\w[\w-]*):\s*(.*)$", m.group(1), re.M)) if m else {}


def mark(html):
    """Mark every element that carries sample text, and every slot photo, with data-kit-sample.
    >>> mark('<li><span class="n">04</span></li><p class="a">Hi<br>there</p><div class="x"></div><img src="assets/slot-photo.svg" alt="robot"><img src="assets/logo-placeholder-w.svg">')
    '<li><span class="n" data-kit-sample>04</span></li><p class="a" data-kit-sample>Hi<br>there</p><div class="x"></div><img src="assets/slot-photo.svg" alt="robot" data-kit-sample><img src="assets/logo-placeholder-w.svg" data-kit-sample>'
    """
    html = re.sub(rf"<({TEXT_TAGS})(\s[^>]*)?>(?=\s*[^<\s])", lambda m: m.group(0)[:-1] + " data-kit-sample>", html)
    # slot photos, the logo placeholder and the client's technology logos are sample content too
    return re.sub(rf'<img([^>]*src="assets/(?:slot-photo|logo-placeholder-[wk]|{LOGOS})\.svg"[^>]*)>', r"<img\1 data-kit-sample>", html)


def is_texture(name):
    """A paper or grain overlay (shipped as a recipe), not a photo that happens to say 'paper'.
    >>> [is_texture(n) for n in ("paper.png", "paper-ivory.png", "grain-espresso.png", "team-papers.jpg", "paper.svg")]
    [True, True, True, False, False]
    """
    return bool(re.search(r"(?:^|[-_])(?:paper|grain)(?=[-_.])", name, re.I)) and not name.lower().endswith(".svg")


def swap(text, theme, new):
    """Replace the kit's theme colours with the client's; variants (brand-2, accent-2…) keep their lightness offset.
    >>> swap("a{c:#FFC20E} b{c:#FFD84A}", {"brand": "#FFC20E", "brand-2": "#FFD84A"}, {"brand": "#1F3FB0"})
    'a{c:#1f3fb0} b{c:#2d50b8}'
    """
    sys.path.insert(0, str(SCRIPTS)); from palette import hex2rgb, rgb2oklch, lch
    for key, old in theme.items():
        base = key.split("-")[0]
        if base not in new: continue
        if key == base:
            rep = new[base].lower()
        else:   # derived variant: same OKLCH offset from its base as in the kit
            L0, C0, H0 = rgb2oklch(hex2rgb(theme[base])); L1, C1, H1 = rgb2oklch(hex2rgb(old)); Ln, Cn, Hn = rgb2oklch(hex2rgb(new[base]))
            rep = lch(max(0, min(1, Ln + L1 - L0)), max(0, Cn + C1 - C0), Hn).lower()
        text = re.sub(re.escape(old), rep, text, flags=re.I)
    return text


def parse_theme(s):
    """'brand #FFC20E; accent #C2410C' → {'brand': '#FFC20E', 'accent': '#C2410C'}"""
    return dict(p.split() for p in s.split(";") if p.strip())


def save_home(builtin=False, root=ROOT):
    """Where `save` writes: the shipped kits/ from the git checkout or with --builtin, else the user's folio home.
    >>> import tempfile; r = Path(tempfile.mkdtemp()) / "skills" / "folio"
    >>> save_home(False, r) == USER_KITS, save_home(True, r) == r / "kits"
    (True, True)
    >>> (r.parent.parent / ".git").mkdir(parents=True); save_home(False, r) == r / "kits"
    True
    """
    return root / "kits" if builtin or (root.parent.parent / ".git").exists() else USER_KITS


def find_kit(kid):
    """A kit by id: the shipped catalogue first, then the user's own saved kits."""
    return next((b / kid for b in (KITS, USER_KITS) if (b / kid / "KIT.md").exists()), None)


def cmd_list(a):
    for idx in (KITS / "INDEX.md", USER_KITS / "INDEX.md"):
        if idx.exists(): print(idx.read_text(encoding="utf-8"))


def cmd_new(a):
    kit = find_kit(a.id)
    if not kit: sys.exit(f"no kit '{a.id}' — run: kit.py list")
    m = meta(kit); dest = Path(a.project); dest.mkdir(parents=True, exist_ok=True); name = a.name or a.id
    theme = parse_theme(m.get("theme", "")); new = {k: v for k, v in (("brand", a.brand), ("accent", a.accent)) if v}
    shutil.copytree(kit / "assets", dest / "assets", dirs_exist_ok=True)
    shutil.copy(ROOT / "assets" / "folio.css", dest / "folio.css")
    html = (kit / "kit.html").read_text(encoding="utf-8").replace('href="kit.css"', f'href="{name}.css"')
    css = (kit / "kit.css").read_text(encoding="utf-8")
    if new:
        html, css = swap(html, theme, new), swap(css, theme, new)
        for svg in (dest / "assets").glob("*.svg"): svg.write_text(swap(svg.read_text(encoding="utf-8"), theme, new), encoding="utf-8")
        from palette import on_colour, hex2rgb, rgb2oklch   # text that reads on the client's colours
        css += "\n/* kit.py: text colours for the client's brand / accent fields; use var(--on-brand) / var(--on-accent) */\n:root {" + \
               "".join(f" --on-{k}: {on_colour(v, rgb2oklch(hex2rgb(v))[2])};" for k, v in new.items()) + " }\n"
    html = mark(html)
    (dest / f"{name}.html").write_text(html, encoding="utf-8"); (dest / f"{name}.css").write_text(css, encoding="utf-8")
    slots = re.findall(r'<img[^>]*alt="([^"]*)"[^>]*data-kit-sample', html)
    n = len(re.findall(r"data-kit-sample", html)) - len(slots)
    (dest / "SLOTS.md").write_text(f"# Slots to fill ({a.id})\n\nReplace every element marked `data-kit-sample` (preflight ERRORs until you do), "
                                   f"then delete the attribute.\n\n- {n} text elements: write the client's copy (reference/copy.md, premium from thin input)\n"
                                   + "".join(f"- photo: {s}\n" for s in slots), encoding="utf-8")
    recipe = dest / "assets" / "textures.txt"
    for line in (recipe.read_text(encoding="utf-8").splitlines() if recipe.exists() else []):
        tname, kind, tone = line.split()
        subprocess.run([sys.executable, str(SCRIPTS / "imagery.py"), "texture", "--kind", kind, "--tone", tone, "--out", str(dest / "assets" / tname)], check=False)
    if m.get("fonts"):
        subprocess.run([sys.executable, str(SCRIPTS / "fonts.py"), *[f.strip() for f in m["fonts"].split(";")], "--out", str(dest / "fonts")], check=False)
    if new:
        from palette import roles, audit
        r = roles(new.get("brand", theme.get("brand")), new.get("accent")); issues = [i for i in audit(r) if i["level"] == "fix"]
        for i in issues: print(f"palette: {i['issue']} → {i['fix']}")
    print(f"kit {a.id} → {dest / (name + '.html')}  ({n} texts, {len(slots)} photos to replace; render with: render.py {name}.html {m.get('render', '')})")


def cmd_save(a):
    base = save_home(a.builtin); src = Path(a.project); kit = base / a.id; (kit / "assets").mkdir(parents=True, exist_ok=True)
    page = Path(a.html) if a.html else next(p for p in src.glob("*.html") if p.parent == src)
    html = page.read_text(encoding="utf-8")
    css_href = re.search(r'<link rel="stylesheet" href="((?!fonts/|folio\.css)[^"]+\.css)"', html).group(1)
    shutil.copy(src / css_href, kit / "kit.css"); html = html.replace(f'href="{css_href}"', 'href="kit.css"')
    (kit / "assets" / "slot-photo.svg").write_text(SLOT, encoding="utf-8")
    recipes = {}
    def asset(mt):   # vector art ships; noise textures ship as a recipe (kit.py new regenerates them); photos become slots
        path = mt.group(1); name = Path(path).name
        if is_texture(name):
            from PIL import Image, ImageStat
            im = Image.open(src / path).convert("RGBA"); tone = ImageStat.Stat(im.convert("RGB"), mask=im.getchannel("A").point(lambda v: 255 * (v > 20))).mean
            recipes[name] = f"{name} {'grain' if 'grain' in name.lower() else 'paper'} #{''.join(f'{round(c):02X}' for c in tone)}"
            return f'src="assets/{name}"'
        if path.lower().endswith(".svg") or re.search(r"newsprint|glow|texture", name, re.I):
            shutil.copy(src / path, kit / "assets" / name); return f'src="assets/{name}"'
        return 'src="assets/slot-photo.svg"'
    html = re.sub(r'src="((?!assets/)[^"]+\.(?:svg|png|jpe?g|webp))"', asset, html)
    css = (kit / "kit.css").read_text(encoding="utf-8")
    for u in set(re.findall(r'url\(["\']?((?!data:)[^"\')]+)["\']?\)', css)):   # css background images → assets
        if (src / u).exists(): shutil.copy(src / u, kit / "assets" / Path(u).name); css = css.replace(u, "assets/" + Path(u).name)
    (kit / "kit.css").write_text(css, encoding="utf-8"); (kit / "kit.html").write_text(html, encoding="utf-8")
    if recipes: (kit / "assets" / "textures.txt").write_text("\n".join(recipes.values()) + "\n", encoding="utf-8")
    else: (kit / "assets" / "textures.txt").unlink(missing_ok=True)   # re-saves drop a stale recipe list
    if (src / "out" / "contact.png").exists():
        from PIL import Image
        im = Image.open(src / "out" / "contact.png"); im.thumbnail((1400, 1400)); im.convert("RGB").save(kit / "preview.jpg", quality=82, optimize=True)
    fonts = sorted(set(re.findall(r"font-family: '([^']+)'", (src / "fonts" / "fonts.css").read_text(encoding="utf-8")))) if (src / "fonts" / "fonts.css").exists() else []
    if not (kit / "KIT.md").exists():
        (kit / "KIT.md").write_text(f"---\nid: {a.id}\nname: {a.name or a.id}\nfamily: {a.family or 'magazine'}\nbest_for: …\nsize: A4\npages: {html.count('class=\"page')}\n"
                                    f"render: --bleed 3\nfonts: {'; '.join(f + ':400,700' for f in fonts)}\ntheme: brand #000000; accent #000000\n---\n"
                                    f"# {a.name or a.id}\n\n**Looks like:** …\n\n**Page archetypes:** …\n\n**Image slots:** …\n\n**Deviations from the reference:** …\n", encoding="utf-8")
    idx = base / "INDEX.md"
    rows = idx.read_text(encoding="utf-8") if idx.exists() else "# Kits\n\n| id | Name | Family | Pages | Looks like |\n|---|---|---|---|---|\n"
    if f"| `{a.id}` |" not in rows:
        idx.write_text(rows + f"| `{a.id}` | {a.name or a.id} | {a.family or 'magazine'} | {html.count('class=\"page')} | see kits/{a.id}/KIT.md |\n", encoding="utf-8")
    # every kit gets its own command: /folio:<name> in the plugin (builtin), /folio-<name> as a personal command (user kits)
    cmd = ROOT.parent.parent / "commands" / f"{a.slash or a.id}.md" if base == KITS else Path.home() / ".claude" / "commands" / f"folio-{a.slash or a.id}.md"
    if base != KITS: cmd.parent.mkdir(parents=True, exist_ok=True)
    taken = cmd.parent.exists() and any(f"Kit: `{a.id}`" in c.read_text(encoding="utf-8") for c in cmd.parent.glob("*.md"))
    if cmd.parent.exists() and not cmd.exists() and not taken:   # re-saving a kit keeps its existing command
        cmd.write_text(f"---\ndescription: Make a piece in the {a.id} style ({a.name or a.id}) from any content\nargument-hint: \"[content / website / brief]\"\n---\n"
                       f"Use the folio skill to make a {a.name or a.id} piece from: $ARGUMENTS\n\nKit: `{a.id}`. Follow `reference/kit-flow.md` step by step with this kit.\n", encoding="utf-8")
    slash = f"/folio:{a.slash or a.id}" if base == KITS else f"/folio-{a.slash or a.id}"
    note = f"new command {slash}" if not taken and cmd.exists() else "existing command kept"
    print(f"saved kit {a.id} → {kit}  (edit KIT.md: looks, archetypes, image slots, theme colours; {note})")


def cmd_gallery(a):
    from PIL import Image, ImageDraw
    out = save_home(a.builtin)   # the shipped gallery shows only shipped kits; a user's gallery shows both
    kits = [k for b in ((KITS,) if out == KITS else (KITS, USER_KITS)) if b.exists() for k in sorted(b.iterdir()) if (k / "preview.jpg").exists()]
    W, T, cols = 700, 60, 3; tiles = []
    for k in kits:
        im = Image.open(k / "preview.jpg").convert("RGB"); im.thumbnail((W - 20, 420)); tiles.append((meta(k).get("name", k.name), meta(k).get("family", ""), im))
    H = max(t[2].height for t in tiles) + T; rows = (len(tiles) + cols - 1) // cols
    sheet = Image.new("RGB", (W * cols, H * rows), (236, 237, 240)); d = ImageDraw.Draw(sheet)
    for i, (name, fam, im) in enumerate(tiles):
        x, y = (i % cols) * W, (i // cols) * H
        sheet.paste(im, (x + (W - im.width) // 2, y + 10)); d.text((x + 16, y + H - T + 12), f"{i + 1}. {name}  ·  {fam}", fill=(20, 20, 24))
    out.mkdir(parents=True, exist_ok=True); sheet.save(out / "GALLERY.png", optimize=True); print(f"gallery → {out / 'GALLERY.png'} ({len(tiles)} kits)")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list")
    n = sub.add_parser("new"); n.add_argument("id"); n.add_argument("project"); n.add_argument("--brand"); n.add_argument("--accent"); n.add_argument("--name")
    s = sub.add_parser("save"); s.add_argument("project"); s.add_argument("id"); s.add_argument("--name"); s.add_argument("--family"); s.add_argument("--html")
    s.add_argument("--cmd", dest="slash", help="slash-command name, default: the kit id")
    s.add_argument("--builtin", action="store_true", help="save into the shipped catalogue (maintainers; automatic in the git checkout)")
    g = sub.add_parser("gallery"); g.add_argument("--builtin", action="store_true")
    sub.add_parser("home")   # the folio home: user kits, TASTE.md, clients/<slug>/ brands
    a = ap.parse_args()
    {"list": cmd_list, "new": cmd_new, "save": cmd_save, "gallery": cmd_gallery, "home": lambda a: print(HOME)}[a.cmd](a)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
