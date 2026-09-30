#!/usr/bin/env python3
"""
folio fonts — fetch webfonts as local files so the PDF never falls back to a system font.

Usage
  python fonts.py "Archivo:400,600,800" "Source Serif 4:400,400i,600" --out project/fonts
  python fonts.py "Hind Madurai:400,600" --subsets latin,tamil --out project/fonts

Writes <out>/*.woff2 and <out>/fonts.css (@font-face rules). Link fonts.css before tokens.css.
Source order: npm @fontsource (works offline-ish, reproducible) → Google Fonts CSS API.
Weights: 400, 700; add 'i' for italic (400i). Subsets default to latin (+latin-ext).
"""
import argparse, io, re, shutil, subprocess, sys, tarfile, tempfile, urllib.request
from pathlib import Path


def slug(family):
    return re.sub(r"[^a-z0-9]+", "-", family.lower()).strip("-")


def from_fontsource(family, weights, subsets, out):
    got = []
    with tempfile.TemporaryDirectory() as td:
        try:
            r = subprocess.run([shutil.which("npm") or "npm", "pack",  # Windows: npm is npm.CMD, needs the full path
                                f"@fontsource/{slug(family)}", "--silent"],
                               cwd=td, capture_output=True, text=True, timeout=120)
        except FileNotFoundError:
            return got
        tgz = next(Path(td).glob("*.tgz"), None)
        if not tgz:
            return got
        with tarfile.open(tgz) as tf:
            names = tf.getnames()
            for w in weights:
                style = "italic" if w.endswith("i") else "normal"
                wt = w.rstrip("i")
                cssname = f"package/{wt}{'-italic' if style == 'italic' else ''}.css"
                ranges = {}
                if cssname in names:
                    css = tf.extractfile(cssname).read().decode()
                    for sub, body in re.findall(r"/\*\s*[\w-]+?-([a-z-]+)-\d+-(?:normal|italic)\s*\*/\s*@font-face\s*{([^}]+)}", css):
                        m = re.search(r"unicode-range:\s*([^;]+);", body)
                        if m:
                            ranges[sub] = m.group(1).strip()
                for sub in subsets:
                    n = f"package/files/{slug(family)}-{sub}-{wt}-{style}.woff2"
                    if n in names:
                        dest = out / Path(n).name
                        dest.write_bytes(tf.extractfile(n).read())
                        got.append((family, wt, style, sub, dest.name, ranges.get(sub)))
    return got


def from_google(family, weights, out):
    ital = any(w.endswith("i") for w in weights)
    axes = sorted({(1 if w.endswith("i") else 0, int(w.rstrip("i"))) for w in weights})
    spec = ("ital,wght@" + ";".join(f"{i},{w}" for i, w in axes)) if ital else ("wght@" + ";".join(str(w) for _, w in axes))
    url = f"https://fonts.googleapis.com/css2?family={family.replace(' ', '+')}:{spec}&display=swap"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"})
    css = urllib.request.urlopen(req, timeout=30).read().decode()
    got = []
    for block in re.findall(r"/\*\s*([\w-]+)\s*\*/\s*@font-face\s*{([^}]+)}", css):
        sub, body = block
        style = re.search(r"font-style:\s*(\w+)", body).group(1)
        wt = re.search(r"font-weight:\s*(\d+)", body).group(1)
        src = re.search(r"url\((https:[^)]+)\)", body).group(1)
        ur = re.search(r"unicode-range:\s*([^;]+);", body)
        name = f"{slug(family)}-{sub}-{wt}-{style}.woff2"
        (out / name).write_bytes(urllib.request.urlopen(src, timeout=30).read())
        got.append((family, wt, style, sub, name, ur.group(1).strip() if ur else None))
    return got


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("specs", nargs="+", help='"Family Name:400,700,400i"')
    ap.add_argument("--out", default="fonts")
    ap.add_argument("--subsets", default="latin,latin-ext")
    a = ap.parse_args()
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    subsets = [s.strip() for s in a.subsets.split(",")]
    faces = []
    for spec in a.specs:
        family, _, ws = spec.partition(":")
        weights = [w.strip() for w in (ws or "400,700").split(",")]
        got = from_fontsource(family, weights, subsets, out)
        if not got:
            try:
                got = from_google(family, weights, out)
            except Exception as e:
                print(f"!! could not fetch {family}: {e}", file=sys.stderr)
        if not got:
            print(f"!! {family}: nothing downloaded — check the name on fonts.google.com / fontsource.org", file=sys.stderr)
        faces += got
        print(f"{family}: {len(got)} files")
    css = [f"@font-face {{ font-family: '{f}'; font-style: {st}; font-weight: {w}; font-display: block; "
           f"src: url('{n}') format('woff2');" + (f" unicode-range: {ur};" if ur else "") + " }"
           for f, w, st, sub, n, ur in faces]
    (out / "fonts.css").write_text("\n".join(css) + "\n")
    print(f"wrote {out/'fonts.css'} ({len(css)} faces)")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")  # Windows consoles default to cp1252 and crash on ■ — “
    main()
