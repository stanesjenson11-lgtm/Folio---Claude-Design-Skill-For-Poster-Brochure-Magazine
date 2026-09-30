#!/usr/bin/env python3
"""
folio promo — launch assets for a finished book (inspired by latent-spaces/brag).

  python promo.py out/                       # stills + reel from out/pages/*.png
  python promo.py out/ --bg "#eef1fb" --accent "#1f3fb0" --format square|vertical|landscape --seconds 16

Writes to out/promo/:
  mock-cover.png, mock-spread-NN.png   presentation mockups (pages on a tinted ground, soft shadow, spine shading)
  social-square.png (1080²) · social-story.png (1080×1920) · linkedin.png (1200×627)
  reel.mp4   page-flip reel: cover hold → spreads, gentle push-in, transitions dip through the ground
             colour (never a muddy crossfade of two busy spreads); frame 0 is the poster frame
  poster.jpg the strongest settled frame (the cover mockup)
Write share-copy.txt yourself (see reference/promo.md) — specific, from the book's own content.
Needs ffmpeg for the reel.
"""
import argparse, subprocess, sys
from pathlib import Path


def hex2rgb(h):
    h = h.lstrip("#"); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def load_pages(out):
    from PIL import Image
    files = sorted((Path(out) / "pages").glob("p-*.png"))
    if not files:
        sys.exit("no out/pages/p-*.png — run render.py first")
    return [Image.open(f).convert("RGB") for f in files]


def spread_image(pages, i, h):
    """page index i (0-based) → the reader's view: cover alone, else verso+recto"""
    from PIL import Image, ImageDraw
    w1 = round(pages[0].width * h / pages[0].height)
    if i == 0:
        return [pages[0].resize((w1, h), Image.LANCZOS)]
    v = i if i % 2 == 1 else i - 1
    group = [pages[k].resize((w1, h), Image.LANCZOS) for k in (v, v + 1) if k < len(pages)]
    return group


def mockup(group, W, H, bg, scale=0.78, tilt=0):
    """place 1–2 pages centred on a ground with a soft shadow and spine shading"""
    from PIL import Image, ImageDraw, ImageFilter
    canvas = Image.new("RGB", (W, H), bg)
    ph = round(H * scale) if len(group) == 1 else None
    pw0 = group[0].width; ph0 = group[0].height
    total_w = pw0 * len(group)
    k = min(W * 0.86 / total_w, H * scale / ph0)
    pages = [g.resize((round(g.width * k), round(g.height * k)), Image.LANCZOS) for g in group]
    tw = sum(p.width for p in pages); th = pages[0].height
    x0, y0 = (W - tw) // 2, (H - th) // 2
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rectangle([x0 + 6, y0 + 14, x0 + tw + 6, y0 + th + 18], fill=(0, 0, 0, 90))
    sh = sh.filter(ImageFilter.GaussianBlur(max(6, W // 90)))
    canvas.paste(sh, (0, 0), sh)
    x = x0
    for p in pages:
        canvas.paste(p, (x, y0)); x += p.width
    if len(pages) == 2:
        g = Image.new("L", (40, th), 0)
        for gx in range(40):
            g.paste(int(70 * (1 - abs(gx - 20) / 20) ** 1.5), (gx, 0, gx + 1, th))
        canvas.paste((0, 0, 0), (x0 + pages[0].width - 20, y0, x0 + pages[0].width + 20, y0 + th), g)
    return canvas


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("out"); ap.add_argument("--bg", default="#e7e8eb"); ap.add_argument("--accent", default="#111111")
    ap.add_argument("--format", choices=["square", "vertical", "landscape"], default="square")
    ap.add_argument("--seconds", type=float, default=16); ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--no-reel", action="store_true")
    a = ap.parse_args()
    from PIL import Image
    pages = load_pages(a.out)
    dest = Path(a.out) / "promo"; dest.mkdir(exist_ok=True)
    bg = hex2rgb(a.bg)
    idx = [0] + list(range(1, len(pages), 2))
    groups = [spread_image(pages, i, 1400) for i in idx]
    mockup(groups[0], 1600, 1600, bg, 0.8).save(dest / "mock-cover.png")
    for n, g in enumerate(groups[1:], 1):
        mockup(g, 2200, 1500, bg, 0.8).save(dest / f"mock-spread-{n:02d}.png")
    mockup(groups[0], 1080, 1080, bg, 0.82).save(dest / "social-square.png")
    mockup(groups[0], 1080, 1920, bg, 0.62).save(dest / "social-story.png")
    mockup(groups[1] if len(groups) > 1 else groups[0], 1200, 627, bg, 0.84).save(dest / "linkedin.png")
    poster = mockup(groups[0], *{"square": (1080, 1080), "vertical": (1080, 1920), "landscape": (1920, 1080)}[a.format], bg, 0.8)
    poster.save(dest / "poster.jpg", quality=92)
    res = {"stills": sorted(str(p) for p in dest.glob("*.png")), "poster": str(dest / "poster.jpg")}

    if not a.no_reel:
        W, H = {"square": (1080, 1080), "vertical": (1080, 1920), "landscape": (1920, 1080)}[a.format]
        fps = a.fps
        cover_s = 2.6; dip = 0.35
        per = max(1.4, (a.seconds - cover_s) / max(1, len(groups) - 1))
        scenes = [(g, cover_s if i == 0 else per) for i, g in enumerate(groups)]
        # pre-render each scene slightly oversize for a push-in
        frames_src = [mockup(g, int(W * 1.08), int(H * 1.08), bg, 0.8 if W <= H else 0.86) for g, _ in scenes]
        cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(fps), "-i", "-",
               "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", "-movflags", "+faststart", str(dest / "reel.mp4")]
        try:
            ff = subprocess.Popen(cmd, stdin=subprocess.PIPE)
        except FileNotFoundError:
            sys.exit("ffmpeg not found — stills were written; install ffmpeg for the reel")
        ground = Image.new("RGB", (W, H), bg)
        ff.stdin.write(poster.resize((W, H)).tobytes())          # frame 0 = poster frame
        for si, ((g, dur), big) in enumerate(zip(scenes, frames_src)):
            n = int(dur * fps)
            for f in range(n):
                t = f / max(1, n - 1)
                z = 1.08 - 0.06 * (t * t * (3 - 2 * t))            # smooth push-in 1.08 → 1.02 of oversize
                cw, ch = int(W * 1.08 / z * (1 / 1.0)), int(H * 1.08 / z)
                cw, ch = min(cw, big.width), min(ch, big.height)
                l, tp = (big.width - cw) // 2, (big.height - ch) // 2
                fr = big.crop((l, tp, l + cw, tp + ch)).resize((W, H), Image.BILINEAR)
                # dip through the ground colour at scene edges (stagger, no double exposure)
                edge = min(f / (dip * fps), (n - 1 - f) / (dip * fps), 1)
                if si == 0: edge = min(1, (n - 1 - f) / (dip * fps))
                if si == len(scenes) - 1: edge = min(1, f / (dip * fps))
                if edge < 1: fr = Image.blend(ground, fr, max(0, edge))
                ff.stdin.write(fr.tobytes())
        ff.stdin.close(); ff.wait()
        res["reel"] = str(dest / "reel.mp4")
        res["reel_seconds"] = round(sum(d for _, d in scenes), 1)
    import json
    print(json.dumps(res, indent=2))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")  # Windows consoles default to cp1252 and crash on ■ — “
    main()
