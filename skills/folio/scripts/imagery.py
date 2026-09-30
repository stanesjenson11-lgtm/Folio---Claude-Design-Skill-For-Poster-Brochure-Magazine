#!/usr/bin/env python3
"""
folio imagery — make visuals from the project's own context.

  grade   unify a client's mixed photos (phone + DSLR, different light) into one "shoot":
          auto-levels, gentle white balance, optional set-wide colour match, and a book-wide
          treatment: natural | duotone | bw | tint
            python imagery.py grade img/ --out img/graded --treatment duotone --brand "#1f3fb0" --ink "#10131f"
  motif   generate the direction's motif as print-ready vector SVG (textures, opener
          backgrounds, dividers), chosen from the brief's context when --type is omitted
            python imagery.py motif --context "football turf academy" --brand "#0e1210" --accent "#b6f23a" --out img/motif.svg
            types: arcs rings halftone slabs grid pitch contour track · liquid blob pencil (Flow style) · dots glow (layered grounds)
  sketch  photo -> coloured-pencil sketch on transparent paper, soft irregular edge, palette wash
            python imagery.py sketch img/raw/laptop.jpg --out img/laptop-sketch.png --palette "#3B2A20,#7D8B6A,#C9A96E,#F6F1E7"
  texture paper or grain overlay PNG for a tactile, printed ground
            python imagery.py texture --kind paper --tone "#ffffff" --out img/paper.png
            python imagery.py motif --type liquid --colors "#0e2a47,#1d5a86,#f4b04a" --bg none --w 303 --h 426 --out img/waves.svg
  mask    a curved photo frame as a clip-path polygon (Canva export keeps it)
            python imagery.py mask --shape wave-top|wave-bottom|blob --seed 3 --amp 8
  prompt  write an image-generation prompt from the context (for the Canva generate-image or
          Adobe Firefly connectors, or any model) — for textures, backgrounds, objects and
          settings; never for invented people or places that stand in for a real organisation
            python imagery.py prompt --context "organic farm produce brochure" --role opener --palette "#7cb518,#2d5a27"
  cutout  remove a photo's background for magazine cut-outs (needs `pip install rembg`)
            python imagery.py cutout img/player.jpg --out img/player-cut.png --person   (--person keeps held props)
  screenshot / mockup   the client's own site on a device (Device mockup pattern)
            python imagery.py screenshot https://example.in --device phone --out img/site-phone.png
            python imagery.py mockup --device phone --screen img/site-phone.png --out img/phone.png
  hatch   hatched circle / rounded square / bracket / half-disc / triangle, or chevrons, as SVG
  divide  a colour field with one flowing edge for colour areas that cross a spread
  reflect circle / rounded / rect photo crop with a faded mirror reflection
  logos   single-colour technology logos from Simple Icons (only tools the client really uses)
            python imagery.py logos react,nextdotjs,flutter,docker --color "#2B1D16" --out img/logos
"""
import argparse, math, random, re, sys
from pathlib import Path


def open_srgb(path):
    """Open a photo and convert an embedded non-sRGB profile (ProPhoto, Adobe RGB, P3) to sRGB, as browsers do;
    without this, grades, crops and cut-outs of such photos come out washed out."""
    from PIL import Image
    sys.path.insert(0, str(Path(__file__).parent))
    from editable import to_srgb
    return to_srgb(Image.open(path))


def hex2rgb(h):
    h = h.lstrip("#"); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


# ------------------------------------------------------------------ grade
def grade(a):
    from PIL import Image, ImageOps, ImageStat, ImageEnhance
    src = Path(a.src); out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    files = [p for p in sorted(src.iterdir()) if p.suffix.lower() in (".jpg", ".jpeg", ".png", ".webp", ".tif", ".tiff")]
    ims = []
    for p in files:
        im = ImageOps.exif_transpose(open_srgb(p)).convert("RGB")
        im = ImageOps.autocontrast(im, cutoff=0.5, preserve_tone=True)
        # gentle grey-world white balance (50%) — fixes yellow indoor / blue shade casts without killing mood
        r, g, b = ImageStat.Stat(im).mean; m = (r + g + b) / 3
        gains = [1 + 0.5 * (m / max(c, 1) - 1) for c in (r, g, b)]
        im = Image.merge("RGB", [ch.point(lambda v, k=k: min(255, v * k)) for ch, k in zip(im.split(), gains)])
        ims.append((p, im))
    if a.match and ims:   # pull every photo's mean brightness/saturation toward the set average
        stats = [(ImageStat.Stat(im.convert("L")).mean[0], ImageStat.Stat(im.convert("HSV").split()[1]).mean[0]) for _, im in ims]
        tb = sum(s[0] for s in stats) / len(stats); ts = sum(s[1] for s in stats) / len(stats)
        ims = [(p, ImageEnhance.Color(ImageEnhance.Brightness(im).enhance(0.5 + 0.5 * tb / max(sb, 1))).enhance(0.5 + 0.5 * ts / max(ss, 1)))
               for (p, im), (sb, ss) in zip(ims, stats)]
    for p, im in ims:
        if a.treatment == "bw":
            im = ImageOps.autocontrast(im.convert("L"), cutoff=1).convert("RGB")
        elif a.treatment == "duotone":
            im = ImageOps.colorize(ImageOps.autocontrast(im.convert("L"), cutoff=1), black=a.ink or "#111111",
                                   white=a.paper or "#ffffff", mid=a.brand or "#1f3fb0")
        elif a.treatment == "tint" and a.brand:
            im = Image.blend(im, Image.new("RGB", im.size, hex2rgb(a.brand)), 0.12)
        dest = out / (p.stem + ".jpg")
        im.save(dest, quality=93, subsampling=0)
        print(f"{p.name} → {dest}  {im.size[0]}×{im.size[1]}px  (max {im.size[0] / 250 * 25.4:.0f}mm wide at 250ppi)")


# ------------------------------------------------------------------ motif
CONTEXT_MOTIF = [
    (r"football|soccer|turf|pitch|futsal", "pitch"), (r"athlet|running|track|marathon|race", "track"),
    (r"farm|agri|land|plot|real estate|villa|layout|terrain|tea|estate", "contour"),
    (r"school|college|universit|institut|hospital|clinic|welfare|ngo|foundation", "arcs"),
    (r"magazine|sport|fitness|gym|music|event|festival", "halftone"),
    (r"industr|pipe|pump|valve|foundry|engineer|manufactur|logistic|construction", "slabs"),
    (r"tech|software|it |data|research|lab|pharma", "grid"), (r"bank|insurance|finance|invest|coop", "rings"),
]


# ------------------------------------------------------------------ curves (liquid, blob, pencil, masks)
def _cr(pts, closed, i):
    n = len(pts)
    P = (lambda j: pts[j % n]) if closed else (lambda j: pts[max(0, min(n - 1, j))])
    return P(i - 1), P(i), P(i + 1), P(i + 2)


def catmull(pts, closed=False, k=8):
    """Sample a Catmull-Rom spline through pts, k points per segment (masks, pencil strokes).
    >>> len(catmull([(0, 0), (10, 5), (20, 0)], k=4)), catmull([(0, 0), (10, 5), (20, 0)], k=4)[-1]
    (9, (20.0, 0.0))
    >>> len(catmull([(0, 0), (10, 0), (10, 10), (0, 10)], closed=True, k=5))
    20
    """
    out = []
    for i in range(len(pts) if closed else len(pts) - 1):
        p0, p1, p2, p3 = _cr(pts, closed, i)
        for s in range(k):
            t = s / k
            out.append(tuple(0.5 * (2 * p1[j] + (p2[j] - p0[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t * t
                                    + (3 * p1[j] - p0[j] - 3 * p2[j] + p3[j]) * t ** 3) for j in (0, 1)))
    return out if closed else out + [tuple(float(v) for v in pts[-1])]


def bezier(pts, closed=False):
    """The same spline as exact cubic Bézier path data (smooth fills at any print size).
    >>> d = bezier([(0, 0), (10, 5), (20, 0)]); d.startswith("M0.0 0.0C"), d.count("C")
    (True, 2)
    >>> bezier([(0, 0), (10, 0), (10, 10), (0, 10)], closed=True).endswith("Z")
    True
    """
    d = f"M{pts[0][0]:.1f} {pts[0][1]:.1f}"
    for i in range(len(pts) if closed else len(pts) - 1):
        p0, p1, p2, p3 = _cr(pts, closed, i)
        d += (f"C{p1[0] + (p2[0] - p0[0]) / 6:.1f} {p1[1] + (p2[1] - p0[1]) / 6:.1f} "
              f"{p2[0] - (p3[0] - p1[0]) / 6:.1f} {p2[1] - (p3[1] - p1[1]) / 6:.1f} {p2[0]:.1f} {p2[1]:.1f}")
    return d + ("Z" if closed else "")


def wavefn(rnd, amp, waves):
    """A smooth seeded wave over u ∈ [0, 1]: three sines, the sum stays within ±amp."""
    comps = [(amp / 1.84 * rnd.uniform(0.6, 1) / (i + 1), waves * (i + 1) * rnd.uniform(0.85, 1.15), rnd.uniform(0, math.tau)) for i in range(3)]
    return lambda u: sum(a_ * math.sin(u * f * math.tau + ph) for a_, f, ph in comps)


def ink_stroke(line, w, rnd):
    """A hand-drawn stroke as a filled outline: tapered at both ends, width wobbling, so it
    reads as pencil or ink and stays a plain vector shape in the Canva export."""
    L, R, n = [], [], len(line)
    for i, (x, y) in enumerate(line):
        (x0, y0), (x1, y1) = line[max(0, i - 1)], line[min(n - 1, i + 1)]
        dx, dy = x1 - x0, y1 - y0; ln = math.hypot(dx, dy) or 1
        hw = w / 2 * (0.3 + 0.7 * math.sin(math.pi * i / (n - 1))) * rnd.uniform(0.8, 1.15)
        L.append((x - dy / ln * hw, y + dx / ln * hw)); R.append((x + dy / ln * hw, y - dx / ln * hw))
    pts = L + R[::-1]
    return "M" + "L".join(f"{x:.2f} {y:.2f}" for x, y in pts) + "Z"


def mask(a):
    """clip-path for a curved photo frame: plain % pairs clamped to 0–100, the form editable.py rebuilds.
    >>> class A: shape, seed, amp, waves = "wave-top", 3, 8.0, 1.5
    >>> m = mask(A); m.startswith("clip-path: polygon("), m.count("%,") + 1
    (True, 67)
    >>> A.shape = "blob"; all(0 <= float(v) <= 100 for v in re.findall(r"(-?[\\d.]+)%", mask(A)))
    True
    """
    rnd = random.Random(a.seed)
    if a.shape in ("wave-top", "wave-bottom"):
        f = wavefn(rnd, a.amp, a.waves)
        edge = [(100 * i / 64, a.amp + f(i / 64)) for i in range(65)]
        pts = edge + [(100, 100), (0, 100)] if a.shape == "wave-top" else [(0, 0), (100, 0)] + [(x, 100 - y) for x, y in edge[::-1]]
    else:  # blob
        ring = [(50 + 47 * rnd.uniform(0.86, 1) * math.cos(i / 10 * math.tau), 50 + 47 * rnd.uniform(0.86, 1) * math.sin(i / 10 * math.tau)) for i in range(10)]
        pts = catmull(ring, closed=True, k=8)
    clamp = lambda v: min(100.0, max(0.0, v))
    return "clip-path: polygon(" + ", ".join(f"{clamp(x):.2f}% {clamp(y):.2f}%" for x, y in pts) + ");"


def motif(a):
    t = a.type
    if not t:
        ctx = (a.context or "").lower()
        t = next((m for pat, m in CONTEXT_MOTIF if re.search(pat, ctx)), "arcs")
    W, H = a.w, a.h
    rnd = random.Random(a.seed)
    B, A = a.brand, a.accent or "#ffffff"
    bg = a.bg or B
    el = []
    sw = a.stroke
    if t == "arcs":
        cx, cy = (W * a.at[0], H * a.at[1]) if a.at else (W * 1.05, H * 0.2)
        for i in range(9):
            r = W * (0.35 + i * 0.13)
            el.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="none" stroke="{A}" stroke-opacity="{0.10 + 0.02 * (i % 3):.2f}" stroke-width="{sw * (1 + (i % 2))}"/>')
    elif t == "rings":
        rx, ry = (W * a.at[0], H * a.at[1]) if a.at else (W * 0.5, H * 0.62)
        for i in range(14):
            el.append(f'<circle cx="{rx:.1f}" cy="{ry:.1f}" r="{W * (0.08 + i * 0.07):.1f}" fill="none" stroke="{A}" stroke-opacity="{0.22 - i * 0.012:.3f}" stroke-width="{sw}"/>')
    elif t == "halftone":
        step = W / 42
        for yi in range(int(H / step) + 2):
            for xi in range(int(W / step) + 2):
                x, y = xi * step + (step / 2 if yi % 2 else 0), yi * step
                d = math.hypot(x - W * 0.85, y - H * 0.15) / math.hypot(W, H)
                r = max(0, step * 0.46 * (1 - d * 1.5))
                if r > 0.08: el.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.2f}" fill="{A}"/>')
    elif t == "slabs":
        x = W * 0.08
        while x < W:
            w = rnd.choice([0.02, 0.035, 0.06, 0.11]) * W
            el.append(f'<rect x="{x:.1f}" y="{-1}" width="{w:.1f}" height="{H + 2}" fill="{A}" fill-opacity="{rnd.choice([0.06, 0.1, 0.16])}"/>')
            x += w + rnd.choice([0.04, 0.07, 0.12]) * W
    elif t == "grid":
        s = W / 12
        for i in range(13): el.append(f'<line x1="{i * s:.1f}" y1="0" x2="{i * s:.1f}" y2="{H}" stroke="{A}" stroke-opacity=".14" stroke-width="{sw}"/>')
        for j in range(int(H / s) + 1): el.append(f'<line x1="0" y1="{j * s:.1f}" x2="{W}" y2="{j * s:.1f}" stroke="{A}" stroke-opacity=".14" stroke-width="{sw}"/>')
        for _ in range(7):
            i, j = rnd.randrange(12), rnd.randrange(int(H / s))
            el.append(f'<rect x="{i * s:.1f}" y="{j * s:.1f}" width="{s:.1f}" height="{s:.1f}" fill="{A}" fill-opacity=".22"/>')
    elif t == "pitch":   # football pitch markings seen from above, cropped
        m, pw, ph = W * 0.06, W * 0.88, H * 0.9
        o = f'fill="none" stroke="{A}" stroke-opacity=".35" stroke-width="{sw * 2}"'
        el += [f'<rect x="{m}" y="{H * 0.05}" width="{pw}" height="{ph}" {o}/>',
               f'<line x1="{m}" y1="{H / 2}" x2="{m + pw}" y2="{H / 2}" {o}/>',
               f'<circle cx="{W / 2}" cy="{H / 2}" r="{W * 0.14}" {o}/>',
               f'<rect x="{W / 2 - W * 0.25}" y="{H * 0.05}" width="{W * 0.5}" height="{H * 0.16}" {o}/>',
               f'<rect x="{W / 2 - W * 0.25}" y="{H * 0.79}" width="{W * 0.5}" height="{H * 0.16}" {o}/>',
               f'<rect x="{W / 2 - W * 0.11}" y="{H * 0.05}" width="{W * 0.22}" height="{H * 0.06}" {o}/>',
               f'<rect x="{W / 2 - W * 0.11}" y="{H * 0.89}" width="{W * 0.22}" height="{H * 0.06}" {o}/>',
               f'<circle cx="{W / 2}" cy="{H / 2}" r="{sw * 3}" fill="{A}" fill-opacity=".5"/>']
        for i in range(10):   # mowing stripes
            el.insert(0, f'<rect x="0" y="{i * H / 10:.1f}" width="{W}" height="{H / 20:.1f}" fill="#ffffff" fill-opacity=".03"/>')
    elif t == "track":
        for i in range(8):
            r = W * (0.3 + i * 0.05)
            el.append(f'<ellipse cx="{W * 0.5}" cy="{H * 1.02}" rx="{r:.1f}" ry="{r * 0.62:.1f}" fill="none" stroke="{A}" stroke-opacity=".3" stroke-width="{sw * 1.5}"/>')
    elif t == "contour":   # topographic lines via marching squares over a smooth random field
        seeds = [(rnd.uniform(-0.1, 1.1) * W, rnd.uniform(-0.1, 1.1) * H, rnd.uniform(0.6, 1.2), rnd.uniform(0.15, 0.3) * W) for _ in range(6)]
        def f(x, y): return sum(k * math.exp(-((x - sx) ** 2 + (y - sy) ** 2) / (2 * sd * sd)) for sx, sy, k, sd in seeds)
        nx, ny = 90, int(90 * H / W); dx, dy = W / nx, H / ny
        grid = [[f(i * dx, j * dy) for i in range(nx + 1)] for j in range(ny + 1)]
        lo = min(min(r) for r in grid); hi = max(max(r) for r in grid)
        for li in range(1, 13):
            lvl = lo + (hi - lo) * li / 13
            segs = []
            for j in range(ny):
                for i in range(nx):
                    v = [grid[j][i], grid[j][i + 1], grid[j + 1][i + 1], grid[j + 1][i]]
                    c = [(i * dx, j * dy), ((i + 1) * dx, j * dy), ((i + 1) * dx, (j + 1) * dy), (i * dx, (j + 1) * dy)]
                    pts = []
                    for e in range(4):
                        a0, a1 = v[e], v[(e + 1) % 4]
                        if (a0 < lvl) != (a1 < lvl):
                            k = (lvl - a0) / (a1 - a0); p0, p1 = c[e], c[(e + 1) % 4]
                            pts.append((p0[0] + k * (p1[0] - p0[0]), p0[1] + k * (p1[1] - p0[1])))
                    for q in range(0, len(pts) - 1, 2):
                        segs.append(f"M{pts[q][0]:.1f} {pts[q][1]:.1f}L{pts[q + 1][0]:.1f} {pts[q + 1][1]:.1f}")
            if segs:
                el.append(f'<path d="{"".join(segs)}" fill="none" stroke="{A}" stroke-opacity="{0.16 + 0.02 * (li % 3):.2f}" stroke-width="{sw * (1.6 if li % 4 == 0 else 1)}" stroke-linecap="round"/>')
    elif t == "liquid":   # layered wave bands rising from the foot (--edge top: hanging from the top)
        cols = a.colors.split(",") if a.colors else [A]
        n = len(cols)
        for k, col in enumerate(cols):
            base, f = H * (a.level - 0.075 * (n - 1 - k)), wavefn(rnd, H * a.amp, rnd.uniform(0.9, 1.6))
            pts = [(W * (i / 8 * 1.1 - 0.05), base + f(i / 8)) for i in range(9)]
            if a.edge == "top":
                pts = [(x, H - y) for x, y in pts]
            foot = -2 if a.edge == "top" else H + 2
            el.append(f'<path d="{bezier(pts)}L{W * 1.05:.1f} {foot}L{-W * 0.05:.1f} {foot}Z" fill="{col.strip()}"/>')
    elif t == "blob":     # organic colour fields, largest first
        cols = a.colors.split(",") if a.colors else [A]
        for k, col in enumerate(cols):
            r = min(W, H) * (0.4 - 0.1 * k)
            m = r * 1.12  # widest the jittered ring can reach: keep it inside the canvas, never sliced flat
            cx, cy = rnd.uniform(min(m, W / 2), max(W - m, W / 2)), rnd.uniform(min(m, H / 2), max(H - m, H / 2))
            ring = [(cx + r * rnd.uniform(0.82, 1.12) * math.cos(i / 9 * math.tau), cy + r * rnd.uniform(0.82, 1.12) * math.sin(i / 9 * math.tau)) for i in range(9)]
            el.append(f'<path d="{bezier(ring, closed=True)}" fill="{col.strip()}"/>')
    elif t == "pencil":   # hand-drawn water lines: a shared current, each line two jittered ink strokes, pencil lifts
        g = wavefn(rnd, H * 0.06, rnd.uniform(0.7, 1.2))
        for li in range(a.lines):
            y0 = H * (0.06 + 0.88 * li / max(1, a.lines - 1))
            own = wavefn(rnd, H * 0.012, rnd.uniform(1.5, 3))
            line = [(W * (u / 60 * 1.06 - 0.03), y0 + g(u / 60) + own(u / 60)) for u in range(61)]
            cuts = sorted(rnd.sample(range(8, 53), rnd.choice([0, 0, 1, 2])))
            pieces, s = [], 0
            for c in cuts:
                pieces.append(line[s:c]); s = c + rnd.randint(2, 4)
            pieces.append(line[s:])
            for piece in (p for p in pieces if len(p) > 4):
                for pas, op in ((0, 0.8), (1, 0.35)):
                    j = [(x, y + rnd.gauss(0, sw * 0.35) * pas) for x, y in piece]
                    el.append(f'<path d="{ink_stroke(j, sw * (1.4 if li % 5 == 0 else 1), rnd)}" fill="{A}" fill-opacity="{op}"/>')
    elif t == "dots":     # small scattered dots, densest around --at (default: upper right), for layered grounds
        cx0, cy0 = (W * a.at[0], H * a.at[1]) if a.at else (W * 0.8, H * 0.2)
        step = max(W, H) / 60
        for yi in range(int(H / step) + 1):
            for xi in range(int(W / step) + 1):
                x, y = xi * step + rnd.uniform(-0.4, 0.4) * step, yi * step + rnd.uniform(-0.4, 0.4) * step
                near = max(0.0, 1 - math.hypot(x - cx0, y - cy0) / (0.75 * max(W, H)))
                if rnd.random() < 0.15 + 0.7 * near:
                    el.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{sw * rnd.uniform(0.35, 0.9):.2f}" fill="{A}" fill-opacity="{0.2 + 0.45 * near:.2f}"/>')
    elif t == "glow":     # soft light blooms: radial gradients (vector, so Canva keeps them; CSS blur would be lost)
        cols = a.colors.split(",") if a.colors else [A]
        defs = []
        for k in range(len(cols) + 1):
            col = cols[k % len(cols)].strip()
            defs.append(f'<radialGradient id="g{k}"><stop offset="0" stop-color="{col}" stop-opacity="{rnd.uniform(0.35, 0.55):.2f}"/>'
                        f'<stop offset="1" stop-color="{col}" stop-opacity="0"/></radialGradient>')
            cx, cy, r = W * rnd.uniform(0.1, 0.9), H * rnd.uniform(0.1, 0.9), min(W, H) * rnd.uniform(0.25, 0.45)
            el.append(f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{r:.1f}" ry="{r * rnd.uniform(0.7, 1.1):.1f}" fill="url(#g{k})"/>')
        el.insert(0, "<defs>" + "".join(defs) + "</defs>")
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}mm" height="{H}mm" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice">'
           f'<rect width="{W}" height="{H}" fill="{bg}"/>' + "".join(el) + "</svg>")
    Path(a.out).write_text(svg)
    print(f"{t} motif → {a.out} ({W}×{H}mm vector). Use as <img> in a .fill/.box, or as a CSS background.")


# ------------------------------------------------------------------ sketch
def sketch(a):
    """Photo -> coloured-pencil sketch on transparent paper: pencil lines (colour dodge + a light hatch)
    over a wash of the photo's tones mapped onto the palette (dark -> light), with a soft, irregular
    hand-finished edge instead of a rectangle. Every sketch in a piece shares the palette.
    >>> import os, tempfile
    >>> from PIL import Image, ImageDraw
    >>> d = tempfile.mkdtemp(); src = os.path.join(d, "s.png")
    >>> im = Image.new("RGB", (160, 120), (235, 230, 220)); ImageDraw.Draw(im).ellipse((40, 30, 120, 90), fill=(90, 60, 40)); im.save(src)
    >>> class A: pass
    >>> a = A(); a.src, a.out, a.palette, a.wash, a.edge, a.max, a.seed, a.tint = src, os.path.join(d, "o.png"), "#3B2A20,#A3AD95,#C9A96E,#F6F1E7", 0.6, "soft", 400, 3, "#3B2A20"
    >>> sketch(a)
    >>> o = Image.open(a.out); o.mode, o.getpixel((0, 0))[3], o.getpixel((80, 60))[3] > 100
    ('RGBA', 0, True)
    >>> al = o.getchannel("A"); [al.crop(b).getextrema()[1] for b in ((0, 0, 160, 1), (0, 119, 160, 120), (0, 0, 1, 120), (159, 0, 160, 120))]
    [0, 0, 0, 0]
    """
    from PIL import Image, ImageOps, ImageFilter, ImageChops, ImageMath, ImageDraw
    rnd = random.Random(a.seed)
    im = open_srgb(a.src).convert("RGB")
    if getattr(a, "crop", None):   # frame the subject first: x0,y0,x1,y1 as fractions of the photo
        x0, y0, x1, y1 = a.crop; im = im.crop((int(x0 * im.width), int(y0 * im.height), int(x1 * im.width), int(y1 * im.height)))
    im.thumbnail((a.max, a.max))
    W, H = im.size
    g = ImageOps.autocontrast(ImageOps.grayscale(im), cutoff=1)
    # graphite: colour-dodge lines + firm outlines from the edges of a softened copy
    blur = ImageOps.invert(g).filter(ImageFilter.GaussianBlur(max(1.5, max(W, H) / 260)))
    lines = ImageMath.lambda_eval(lambda e: e["convert"](e["min"](e["a"] * 255 / (256 - e["b"]), 255), "L"), a=g, b=blur)
    lines = lines.point(lambda v: 255 - min(255, int((255 - v) * 2.2)))
    outline = g.filter(ImageFilter.GaussianBlur(max(1.0, max(W, H) / 900))).filter(ImageFilter.FIND_EDGES)
    lines = ImageChops.multiply(lines, outline.point(lambda v: 255 - min(200, max(0, v - 18) * 4)))
    # directional strokes: stretched noise, rotated, used both as graphite hatch and as the colour's tooth
    def strokes(seed_shift):
        n = Image.effect_noise((W, max(2, H // 26)), 90 + seed_shift).resize((W * 2, H * 2)).rotate(-32 - seed_shift, resample=Image.BICUBIC)
        return n.crop((W // 2, H // 2, W // 2 + W, H // 2 + H))
    shade = ImageOps.invert(g).point(lambda v: min(255, v * 2))                     # hatch only where the photo has tone
    lines = ImageChops.multiply(lines, Image.composite(strokes(0).point(lambda v: 226 + v * 29 // 255), Image.new("L", (W, H), 255), shade))
    # coloured pencil: palette gradient map laid down in strokes, with white paper between them
    stops = [hex2rgb(c.strip()) for c in a.palette.split(",")]
    stops = stops[1:-1] if len(stops) >= 4 else stops[1:] if len(stops) > 2 else stops   # darkest draws the lines, lightest is the paper
    lut = []
    for ch in range(3):
        for v in range(256):
            t = v / 255 * (len(stops) - 1); i = min(int(t), len(stops) - 2); f = t - i
            lut.append(round(stops[i][ch] * (1 - f) + stops[i + 1][ch] * f))
    tones = ImageOps.equalize(g).filter(ImageFilter.GaussianBlur(max(W, H) / 150))
    colour = Image.merge("RGB", [tones] * 3).point(lut)
    tooth = strokes(7).point(lambda v: min(255, max(0, int((v - 55) * 2.3))))            # 0 = paper, 255 = pencil pressure
    depth = ImageOps.invert(g).point(lambda v: min(255, v * 2))                    # pressure from real brightness: white paper stays white
    mask = ImageChops.multiply(tooth, depth).point(lambda v: int(v * a.wash))
    wash = Image.composite(colour, Image.new("RGB", (W, H), (255, 255, 255)), mask)
    ink = ImageOps.colorize(lines, black=hex2rgb(a.tint), white=(255, 255, 255))
    rgb = ImageChops.multiply(wash, ink)
    # colour-to-alpha against white: the paper disappears, every stroke and wash keeps its colour
    import numpy as np
    c = np.asarray(rgb, dtype=np.float32)
    a_ = 255 - c.min(axis=2)
    un = 255 - (255 - c) * 255 / np.maximum(a_, 1)[..., None]
    # hand-finished edge: a soft ellipse whose rim (only the rim) is broken up by smooth noise
    edge = Image.new("L", (W, H), 0)
    ImageDraw.Draw(edge).ellipse((W * 0.06, H * 0.06, W * 0.94, H * 0.94), fill=255)
    edge = edge.filter(ImageFilter.GaussianBlur(max(W, H) / (12 if a.edge == "soft" else 26)))
    noise = Image.effect_noise((max(2, W // 30), max(2, H // 30)), 80).resize((W, H), Image.BICUBIC)
    noise = noise.filter(ImageFilter.GaussianBlur(max(W, H) / 120))
    rim = np.clip((np.asarray(edge, np.float32) - 0.35 * np.asarray(noise, np.float32) - 38) * 3, 0, 255)
    fade = lambda n: np.clip(np.minimum(np.arange(n), np.arange(n)[::-1]) / (0.05 * n), 0, 1)
    rim *= np.outer(fade(H), fade(W))   # the blur leaks to the canvas edge on wide crops: fade the outer 5% so no straight cut line shows
    out =Image.fromarray(np.dstack([np.clip(un, 0, 255), a_ * rim / 255]).astype(np.uint8), "RGBA")
    out.save(a.out, optimize=True)


# ------------------------------------------------------------------ texture
def texture(a):
    """Paper or grain overlay as a PNG with alpha: lay it over a ground at 20–45% opacity for a printed,
    tactile feel. The colour stays the ground's own; only the specks and fibres show."""
    from PIL import Image, ImageFilter, ImageDraw
    rnd = random.Random(a.seed)
    W, H = a.px
    noise = Image.effect_noise((W, H), 64 if a.kind == "grain" else 38).filter(ImageFilter.GaussianBlur(0.6 if a.kind == "grain" else 1.2))
    alpha = noise.point(lambda v: min(255, abs(v - 128) * (3 if a.kind == "grain" else 2)))
    if a.kind == "paper":  # fibres: short soft strokes
        d = ImageDraw.Draw(alpha)
        for _ in range(int(W * H / 9000)):
            x, y, ang, ln = rnd.uniform(0, W), rnd.uniform(0, H), rnd.uniform(0, math.tau), rnd.uniform(6, 26)
            d.line([(x, y), (x + ln * math.cos(ang), y + ln * math.sin(ang))], fill=rnd.randint(40, 110), width=1)
        alpha = alpha.filter(ImageFilter.GaussianBlur(0.5))
    out = Image.new("RGBA", (W, H), hex2rgb(a.tone) + (0,))
    out.putalpha(alpha)
    out.save(a.out, optimize=True)
    print(f"{a.kind} texture → {a.out} ({W}×{H}px). Lay it over the ground at opacity .12–.4 in a container marked data-texture "
          f"(preflight then treats it as texture, not a photo): <div class=\"fill\" data-texture><img src=… alt=\"\"></div>")


# ------------------------------------------------------------------ prompt
ROLES = {
    "hero": "a single decisive photograph that can carry a full page; strong subject, generous quiet area for a headline",
    "opener": "a section-opener photograph with a clear horizon or empty band for type, calm edges",
    "texture": "a close-up material texture, evenly lit, no focal subject, tileable feel",
    "spot": "a small still-life object shot, isolated, on a plain background",
    "background": "an out-of-focus environmental background with soft light, no subject",
}
LIGHT = ["soft overcast daylight", "low golden-hour side light", "clean studio softbox light", "cool blue-hour ambient light", "hard noon sun with crisp shadows"]
LENS = ["35mm documentary framing", "50mm natural perspective", "85mm shallow depth of field", "wide 24mm environmental view", "top-down flat lay"]
ANCHOR = ["subject in the right third, empty left two-thirds", "subject low in frame, open sky above", "subject in the left third, negative space right",
          "centred subject, symmetrical, quiet corners", "diagonal composition from lower left to upper right"]


def prompt(a):
    rnd = random.Random(a.seed)
    ctx = a.context.strip().rstrip(".")
    pal = ", ".join(a.palette.split(",")) if a.palette else "the brand palette"
    p = (f"Photograph for a printed {a.piece}: {ctx}. {ROLES[a.role].capitalize()}. "
         f"{rnd.choice(LIGHT).capitalize()}, {rnd.choice([l for l in LENS if 'flat lay' not in l])}, {rnd.choice(ANCHOR)}. "
         f"Colour grade harmonised with {pal}; natural skin and material tones; realistic, unstaged, editorial documentary quality. "
         f"Portrait orientation for an A4 page." if a.role in ("hero", "opener") else
         f"Image for a printed {a.piece}: {ctx}. {ROLES[a.role].capitalize()}. {rnd.choice(LIGHT).capitalize()}, colours from {pal}.")
    negative = ("no text, no letters, no logos, no watermarks, no brand names, no UI, no frames or borders, no collage, "
                "no fantasy glow, no lens flare, no purple-blue gradient, no extra fingers or distorted hands")
    print("PROMPT:\n" + p + "\n\nAVOID:\n" + negative)
    print("\nRules: use generated images only for textures, backgrounds, objects and generic settings. Never generate people, "
          "buildings, products or events presented as the client's own. Keep a credit line ('Illustrative image') when the "
          "client's policy requires it. Check resolution: generated images are often ~1–2 MP — fine for a small frame, not a full page.")


# ------------------------------------------------------------------ cutout
def cutout(a):
    try:
        from rembg import remove, new_session
    except ImportError:
        sys.exit("rembg not installed: pip install \"rembg[cpu]\" (downloads its model from GitHub on first use). "
                 "Alternatives: Canva remove-background or the Adobe connector.")
    from PIL import Image, ImageChops
    src = open_srgb(a.src)
    im = remove(src, session=new_session("u2net"))
    if a.person:   # human-seg keeps the whole body but drops held props (a laptop lid); u2net keeps props but fades legs → union
        body = remove(src, session=new_session("u2net_human_seg")).getchannel("A")
        im.putalpha(ImageChops.lighter(im.getchannel("A"), body))
    box = im.getchannel("A").getbbox()
    (im.crop(box) if box else im).save(a.out)   # trimmed to the figure
    print(f"cut-out → {a.out}; check edges (hair, fingers) at 200% before placing.")


# ------------------------------------------------------------------ screens, devices, logos
DEVICES = {"desktop": (1440, 900), "tablet": (820, 1180), "phone": (390, 844)}


def screenshot(a):
    """Capture a live page at a device viewport, e.g. the client's own site for a device mockup."""
    from playwright.sync_api import sync_playwright
    w, h = DEVICES[a.device]
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": w, "height": h}, device_scale_factor=2, is_mobile=a.device == "phone")
        pg.goto(a.url, wait_until="networkidle", timeout=90000); pg.wait_for_timeout(1500)
        if a.scroll: pg.evaluate(f"window.scrollTo(0, {a.scroll})"); pg.wait_for_timeout(1200)
        pg.screenshot(path=a.out); b.close()
    print(f"screenshot → {a.out} ({w}×{h} @2x)")


def mockup(a):
    """Put a screenshot into a flat device frame (no shadow) on a transparent PNG.
    >>> import os, tempfile
    >>> from PIL import Image
    >>> d = tempfile.mkdtemp(); s = os.path.join(d, "s.png"); Image.new("RGB", (390, 844), "red").save(s)
    >>> class A: pass
    >>> a = A(); a.device, a.screen, a.out, a.px, a.color = "phone", s, os.path.join(d, "m.png"), 200, "#1d1d1f"
    >>> mockup(a); m = Image.open(a.out); m.mode, m.getpixel((0, 0))[3], m.getpixel((m.width // 2, m.height // 2))[:3]  # doctest: +ELLIPSIS
    mockup → ...
    ('RGBA', 0, (255, 0, 0))
    """
    from PIL import Image, ImageDraw, ImageOps
    S = 2                                                     # draw at 2x, downsample for smooth corners
    sw, sh = DEVICES[a.device]; W = a.px * S; H = round(W * sh / sw)
    body, silver = hex2rgb(a.color) + (255,), (216, 217, 221, 255)
    b, bot, r, ri = {"phone": (.05, .05, .17, .13), "tablet": (.07, .13, .08, .02), "desktop": (.025, .025, .02, .004)}[a.device]
    bx, bb = round(W * b), round(W * bot); FW, FH = W + 2 * bx, H + bx + bb
    chin, neck, base = (round(W * .07), round(W * .12), round(W * .018)) if a.device == "desktop" else (0, 0, 0)
    im = Image.new("RGBA", (FW, FH + chin + neck + base), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    if chin:
        d.rounded_rectangle((0, 0, FW - 1, FH + chin - 1), radius=round(W * r), fill=silver)
        d.rounded_rectangle((0, 0, FW - 1, FH - 1), radius=round(W * r), fill=body); d.rectangle((0, FH - round(W * r), FW - 1, FH - 1), fill=body)
        cx, y0 = FW // 2, FH + chin
        d.polygon([(cx - W * .07, y0), (cx + W * .07, y0), (cx + W * .09, y0 + neck), (cx - W * .09, y0 + neck)], fill=(196, 197, 202, 255))
        d.rounded_rectangle((cx - W * .17, y0 + neck, cx + W * .17, y0 + neck + base - 1), radius=base // 2, fill=silver)
    else:
        d.rounded_rectangle((0, 0, FW - 1, FH - 1), radius=round(W * r), fill=body)
    if a.device == "tablet":
        cx, cy, rr = FW // 2, FH - bb // 2, round(bb * .26); d.ellipse((cx - rr, cy - rr, cx + rr, cy + rr), outline=(84, 84, 90, 255), width=max(2, rr // 5))
    shot = ImageOps.fit(Image.open(a.screen).convert("RGB"), (W, H), centering=(0.5, 0))
    m = Image.new("L", (W, H), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, W - 1, H - 1), radius=round(W * ri), fill=255)
    im.paste(shot, (bx, bx), m)
    im.resize((im.width // S, im.height // S), Image.LANCZOS).save(a.out)
    print(f"mockup → {a.out}")


def hatch(a):
    """Hatched shape as vector SVG (stripes clipped to a circle, rounded square, corner bracket, half-disc or
    triangle), or a row of chevrons. Stripes are diagonal unless --angle 0."""
    c, sw, g = a.color, a.width, a.gap
    shapes = {"circle": ("0 0 100 100", '<circle cx="50" cy="50" r="50"/>'), "rounded": ("0 0 100 100", '<rect width="100" height="100" rx="18"/>'),
              "bracket": ("0 0 100 100", '<path d="M0 0H80A20 20 0 0 1 100 20V100H74V26H0Z"/>'),
              "half": ("0 0 100 50", '<path d="M0 0H100A50 50 0 0 1 0 0Z"/>'), "triangle": ("0 0 100 86", '<path d="M0 0H100L50 86Z"/>')}
    if a.shape == "chevrons":
        body = f'<g fill="none" stroke="{c}" stroke-width="{sw * 2}" stroke-linejoin="miter">' + "".join(
            f'<path d="M{4 + i * 22} 4L{20 + i * 22} 22L{4 + i * 22} 40"/>' for i in range(3)) + "</g>"
        vb = "0 0 72 44"
    else:
        vb, clip = shapes[a.shape]
        lines = "".join(f'<line x1="-10" y1="{y}" x2="110" y2="{y}"/>' for y in range(0, 101, g)) if a.angle == 0 else \
            "".join(f'<line x1="{x}" y1="-5" x2="{x - 110}" y2="105"/>' for x in range(0, 221, g))
        body = f'<defs><clipPath id="h">{clip}</clipPath></defs><g clip-path="url(#h)" stroke="{c}" stroke-width="{sw}">{lines}</g>'
    Path(a.out).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}">{body}</svg>', encoding="utf-8")
    print(f"hatch → {a.out}")


def divide(a):
    """A colour field with one flowing edge, for colour areas that cross a spread (no straight divide line).
    >>> class A: pass
    >>> import os, tempfile; a = A(); a.w, a.h, a.color, a.edge, a.amp, a.waves, a.seed = 420, 90, "#7D8B6A", "top", .07, 1.2, 3
    >>> a.out = os.path.join(tempfile.mkdtemp(), "d.svg"); divide(a); open(a.out).read().count("<path")  # doctest: +ELLIPSIS
    divide → ...
    1
    """
    rnd = random.Random(a.seed); amp = a.h * a.amp; f = wavefn(rnd, amp, a.waves)
    pts = [(a.w * i / 24, amp + f(i / 24)) for i in range(25)]
    if a.edge == "bottom": pts = [(x, a.h - y) for x, y in pts]
    if a.edge == "both":   # a band: flowing top and bottom, different phase
        g = wavefn(rnd, amp, a.waves); low = [(a.w * i / 24, a.h - amp - g(i / 24)) for i in range(24, -1, -1)]
        d = bezier(pts) + "L" + bezier(low)[1:] + "Z"
    else:
        d = bezier(pts) + (f"L{a.w} {a.h}L0 {a.h}Z" if a.edge == "top" else f"L{a.w} 0L0 0Z")
    Path(a.out).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {a.w} {a.h}" preserveAspectRatio="none">'
                           f'<path d="{d}" fill="{a.color}"/></svg>', encoding="utf-8")
    print(f"divide → {a.out}")


def reflect(a):
    """Crop a photo to a rectangle, rounded square or circle and add a faded mirror reflection below (Pop Stripe)."""
    from PIL import Image, ImageDraw, ImageOps, ImageChops
    im = open_srgb(a.src).convert("RGB")
    if a.size: im = ImageOps.fit(im, tuple(a.size), centering=(0.5, 0.5))
    W, H = im.size; m = Image.new("L", (W * 4, H * 4), 0); d = ImageDraw.Draw(m)
    if a.shape == "circle": d.ellipse((0, 0, W * 4 - 1, H * 4 - 1), fill=255)
    elif a.shape == "rounded": d.rounded_rectangle((0, 0, W * 4 - 1, H * 4 - 1), radius=round(min(W, H) * 4 * a.radius), fill=255)
    else: d.rectangle((0, 0, W * 4, H * 4), fill=255)
    src = im.convert("RGBA"); src.putalpha(m.resize((W, H), Image.LANCZOS))
    rh = round(H * a.depth); out = Image.new("RGBA", (W, H + a.gap + rh), (0, 0, 0, 0)); out.paste(src, (0, 0))
    if rh:
        fl = ImageOps.flip(src).crop((0, 0, W, rh))
        fade = Image.linear_gradient("L").resize((W, rh)).point(lambda v: int((255 - v) * a.strength))
        fl.putalpha(ImageChops.multiply(fl.getchannel("A"), fade)); out.alpha_composite(fl, (0, H + a.gap))
    out.save(a.out); print(f"reflect → {a.out}")


def logos(a):
    """Download technology / brand logos as single-colour SVGs (Simple Icons, CC0 icon data; the marks remain
    their owners' trademarks: use them only to name tools the client really uses)."""
    import urllib.request
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True); miss = []
    for slug in a.slugs.split(","):
        slug = slug.strip()
        try:
            svg = urllib.request.urlopen(f"https://cdn.jsdelivr.net/npm/simple-icons@latest/icons/{slug}.svg", timeout=30).read().decode()
            (out / f"{slug}.svg").write_text(svg.replace("<path ", f'<path fill="{a.color}" ', 1), encoding="utf-8")
        except Exception:
            miss.append(slug)
    print(f"logos → {out}  ({len(a.slugs.split(',')) - len(miss)} saved)" + (f"; not in Simple Icons: {', '.join(miss)}" if miss else ""))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    g = sub.add_parser("grade"); g.add_argument("src"); g.add_argument("--out", default="img/graded")
    g.add_argument("--treatment", choices=["natural", "duotone", "bw", "tint"], default="natural")
    g.add_argument("--brand"); g.add_argument("--ink"); g.add_argument("--paper"); g.add_argument("--match", action="store_true")
    m = sub.add_parser("motif"); m.add_argument("--type", choices=["arcs", "rings", "halftone", "slabs", "grid", "pitch", "contour", "track", "liquid", "blob", "pencil", "dots", "glow"])
    m.add_argument("--context"); m.add_argument("--brand", default="#1f3fb0"); m.add_argument("--accent"); m.add_argument("--bg")
    m.add_argument("--w", type=float, default=210); m.add_argument("--h", type=float, default=297); m.add_argument("--stroke", type=float, default=0.6)
    m.add_argument("--seed", type=int, default=7); m.add_argument("--out", default="img/motif.svg")
    m.add_argument("--colors", help="liquid/blob: comma list, back to front"); m.add_argument("--level", type=float, default=0.72, help="liquid: front band height (0–1)")
    m.add_argument("--amp", type=float, default=0.05, help="liquid: wave depth as a share of height"); m.add_argument("--edge", choices=["bottom", "top"], default="bottom"); m.add_argument("--lines", type=int, default=16, help="pencil: number of lines")
    m.add_argument("--at", type=lambda v: [float(x) for x in v.split(",")], help="arcs/rings: centre as x,y fractions of the page, e.g. -0.05,0.75")
    sk = sub.add_parser("sketch"); sk.add_argument("src"); sk.add_argument("--out", required=True)
    sk.add_argument("--palette", default="#3B2A20,#7D8B6A,#C9A96E,#F6F1E7", help="wash colours, dark to light")
    sk.add_argument("--wash", type=float, default=0.8, help="0 = graphite only, 1 = full palette wash")
    sk.add_argument("--edge", choices=["soft", "torn"], default="soft"); sk.add_argument("--max", type=int, default=2400, help="longest side, px")
    sk.add_argument("--tint", default="#3B2A20", help="pencil colour"); sk.add_argument("--seed", type=int, default=7)
    sk.add_argument("--crop", type=lambda v: [float(x) for x in v.split(",")], help="x0,y0,x1,y1 fractions to frame the subject")
    tx = sub.add_parser("texture"); tx.add_argument("--kind", choices=["paper", "grain"], default="paper")
    tx.add_argument("--px", type=lambda v: [int(x) for x in v.split("x")], default=[1600, 2260], help="WxH pixels")
    tx.add_argument("--tone", default="#ffffff", help="speck colour: white on dark grounds, ink on light")
    tx.add_argument("--seed", type=int, default=7); tx.add_argument("--out", default="img/paper.png")
    k = sub.add_parser("mask"); k.add_argument("--shape", choices=["wave-top", "wave-bottom", "blob"], required=True)
    k.add_argument("--seed", type=int, default=7); k.add_argument("--amp", type=float, default=6, help="wave depth in %%"); k.add_argument("--waves", type=float, default=1.5)
    p = sub.add_parser("prompt"); p.add_argument("--context", required=True); p.add_argument("--role", choices=list(ROLES), default="opener")
    p.add_argument("--palette"); p.add_argument("--piece", default="brochure"); p.add_argument("--seed", type=int)
    c = sub.add_parser("cutout"); c.add_argument("src"); c.add_argument("--out", required=True)
    c.add_argument("--person", action="store_true", help="use the human-segmentation model")
    sc = sub.add_parser("screenshot"); sc.add_argument("url"); sc.add_argument("--device", choices=list(DEVICES), default="desktop")
    sc.add_argument("--scroll", type=int, default=0, help="scroll down this many CSS px first"); sc.add_argument("--out", required=True)
    mk = sub.add_parser("mockup"); mk.add_argument("--device", choices=list(DEVICES), required=True); mk.add_argument("--screen", required=True)
    mk.add_argument("--px", type=int, default=1400, help="screen width in px"); mk.add_argument("--color", default="#1d1d1f"); mk.add_argument("--out", required=True)
    h = sub.add_parser("hatch"); h.add_argument("--shape", choices=["circle", "rounded", "bracket", "half", "triangle", "chevrons"], required=True)
    h.add_argument("--color", default="#ffffff"); h.add_argument("--width", type=float, default=2.2); h.add_argument("--gap", type=int, default=7)
    h.add_argument("--angle", type=int, choices=[0, 45], default=45); h.add_argument("--out", required=True)
    dv = sub.add_parser("divide"); dv.add_argument("--w", type=float, default=420); dv.add_argument("--h", type=float, default=90)
    dv.add_argument("--color", required=True); dv.add_argument("--edge", choices=["top", "bottom", "both"], default="top")
    dv.add_argument("--amp", type=float, default=.07); dv.add_argument("--waves", type=float, default=1.2); dv.add_argument("--seed", type=int, default=7); dv.add_argument("--out", required=True)
    rf = sub.add_parser("reflect"); rf.add_argument("src"); rf.add_argument("--out", required=True)
    rf.add_argument("--shape", choices=["rect", "rounded", "circle"], default="rounded"); rf.add_argument("--radius", type=float, default=.14)
    rf.add_argument("--size", type=lambda v: [int(x) for x in v.split("x")], help="WxH px crop"); rf.add_argument("--depth", type=float, default=.3)
    rf.add_argument("--strength", type=float, default=.35); rf.add_argument("--gap", type=int, default=6)
    lg = sub.add_parser("logos"); lg.add_argument("slugs", help="comma list of Simple Icons slugs, e.g. react,nextdotjs,flutter")
    lg.add_argument("--color", default="#2B1D16"); lg.add_argument("--out", default="img/logos")
    a = ap.parse_args()
    {"grade": grade, "motif": motif, "prompt": prompt, "cutout": cutout, "texture": texture, "sketch": sketch, "mask": lambda a: print(mask(a)),
     "screenshot": screenshot, "mockup": mockup, "hatch": hatch, "divide": divide, "reflect": reflect, "logos": logos}[a.cmd](a)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")  # Windows consoles default to cp1252 and crash on ■ — “
    main()
