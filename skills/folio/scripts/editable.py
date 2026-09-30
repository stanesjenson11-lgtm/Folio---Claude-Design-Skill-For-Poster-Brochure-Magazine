#!/usr/bin/env python3
"""
folio editable — turn a folio document into editable, page-embedded HTML (the FD-brochure format).

Every page becomes a fixed-size <div data-document-role="page"> (A4 = 794 × 1123 px) holding a FLAT
list of absolutely positioned elements, measured from the browser's rendered layout:
  text   → one text box per paragraph / heading (runs keep their weight, colour, size);
           text flowing across columns is split into one box per column
  shape  → colour fields, rules, circles (backgrounds, borders, radius)
  image  → photos cropped exactly as they appear (object-fit, focal point, page clipping),
           at native resolution, with circle/ellipse/polygon/radius masks baked into PNG alpha
  svg    → charts and diagrams, styles inlined, embedded as vector SVG images
Images and fonts are base64-embedded; a Google Fonts <link> is added as well so tools that
prefer hosted fonts (Canva import) resolve them. No grid, flex, columns or pseudo-elements remain,
so every element is individually editable after import.

Usage
  python editable.py brochure.html                   # → out/brochure.editable.html + fidelity check
  python editable.py brochure.html --out build --no-check
  python editable.py brochure.html --fonts link|embed|both   (default both)

render.py runs this automatically (disable with --no-editable).

Fidelity check: every editable page is screenshotted and compared with the original render;
pages under 97% similarity are listed so you can look at out/editable-diff.png.

Approach adapted from huashu-design's pptx_from_rendered.py (MIT, alchaincyf): measure the
rendered DOM instead of constraining how the HTML is written. See CREDITS.md.
"""
import argparse, base64, io, json, math, mimetypes, re, sys
from pathlib import Path
from urllib.parse import unquote, urlparse
from urllib.request import url2pathname

JS = r"""
() => {
  const INLINE = new Set(['a','abbr','b','bdi','bdo','br','cite','code','data','dfn','em','i','kbd','mark','q','s','samp',
                          'small','span','strong','sub','sup','time','u','var','wbr']);
  const px = v => parseFloat(v) || 0;
  // corner radii in css px, [tl, tr, br, bl]; '50%' is a share of the box, not 50px
  const radii = (cs, r) => ['TopLeft', 'TopRight', 'BottomRight', 'BottomLeft'].map(c => {
    const v = (cs[`border${c}Radius`] || '0').split(' ')[0];
    return v.endsWith('%') ? parseFloat(v) / 100 * Math.min(r.width, r.height) : px(v); });
  const painted = c => c && c !== 'transparent' && !/rgba\([^)]*,\s*0\)$/.test(c);
  const warn = [];
  const pages = [...document.querySelectorAll('.page')];
  const r2 = n => Math.round(n * 100) / 100;

  // --- text helpers ------------------------------------------------------------------
  const TEXT_PROPS = ['font-family','font-size','font-weight','font-style','font-stretch','color','letter-spacing',
                      'text-transform','text-decoration-line','font-variant-caps','font-variant-numeric','font-feature-settings','-webkit-text-stroke'];
  const styleOf = (el, props) => { const cs = getComputedStyle(el);
    return props.map(p => `${p}:${cs.getPropertyValue(p).replace(/"/g, "'")}`).join(';'); };
  // serialise inline content with computed styles baked in (whitespace collapsed like the browser does)
  const serial = (node) => {
    let html = '';
    for (const n of node.childNodes) {
      if (n.nodeType === 3) html += n.textContent.replace(/\s+/g, ' ').replace(/&/g,'&amp;').replace(/</g,'&lt;');
      else if (n.nodeType === 1) {
        const t = n.tagName.toLowerCase();
        if (t === 'br') { html += '<br>'; continue; }
        const inner = serial(n);
        if (!inner.trim()) continue;
        html += `<span style="${styleOf(n, TEXT_PROPS)}">${inner}</span>`;
      }
    }
    return html;
  };
  // text nodes + global char offsets, for splitting a paragraph that flows across columns
  const textIndex = (el) => {
    const nodes = []; let total = 0;
    const w = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
    while (w.nextNode()) { const n = w.currentNode; nodes.push({n, start: total}); total += n.textContent.length; }
    return {nodes, total};
  };
  const charRect = (idx, i) => {
    for (let k = idx.nodes.length - 1; k >= 0; k--) {
      const {n, start} = idx.nodes[k];
      if (i >= start && i < start + n.textContent.length) {
        const r = document.createRange(); r.setStart(n, i - start); r.setEnd(n, i - start + 1);
        const q = r.getClientRects(); return q.length ? q[0] : null;
      }
    }
    return null;
  };
  const lineRects = el => { const r = document.createRange(); r.selectNodeContents(el);
    return [...r.getClientRects()].filter(q => q.width > .5 && q.height > .5); };

  // --- clip-path parsing is done in python; here we only report it ------------------
  return pages.map((pg, pi) => {
    pg.scrollIntoView({block: 'start'});
    const trim = pg.querySelector('.trim') || pg;
    const T = trim.getBoundingClientRect();
    const out = [];
    const rel = r => ({x: r2(r.left - T.left), y: r2(r.top - T.top), w: r2(r.width), h: r2(r.height)});
    const inter = (a, b) => ({left: Math.max(a.left, b.left), top: Math.max(a.top, b.top),
                              right: Math.min(a.right, b.right), bottom: Math.min(a.bottom, b.bottom)});
    const pageClip = {left: T.left, top: T.top, right: T.right, bottom: T.bottom};

    // pseudo-elements are not exportable — report them
    const pseudoCheck = el => ['::before', '::after'].forEach(ps => {
      const c = getComputedStyle(el, ps);
      if (c.content && c.content !== 'none' && c.content !== 'normal' &&
          (painted(c.backgroundColor) || c.content.replace(/["']/g, '').trim()))
        warn.push(`p${pi + 1}: ${el.tagName.toLowerCase()}.${[...el.classList].join('.')}${ps} is visible but pseudo-elements cannot be exported — use a real element`);
    });

    // transformed boxes (a tilted band, a rotated word): measure the subtree untransformed, then give every exported
    // piece the box's transform with its origin expressed in the piece's own coordinates, so tilted groups stay together
    // ponytail: one level of transform; a transformed box inside another transformed box keeps only its own
    const walk = (el, clip, opacity, zIn = []) => {
      const tcs = getComputedStyle(el), tfm = tcs.transform !== 'none' ? tcs.transform : null;
      if (!tfm) return walkInner(el, clip, opacity, zIn);
      const o = tcs.transformOrigin.split(' ').map(parseFloat), prev = el.style.getPropertyValue('transform');
      el.style.setProperty('transform', 'none', 'important');
      const r0 = el.getBoundingClientRect(), ax = r0.left + o[0] - T.left, ay = r0.top + o[1] - T.top, start = out.length;
      walkInner(el, clip, opacity, zIn);
      el.style.removeProperty('transform'); if (prev) el.style.setProperty('transform', prev);
      for (const it of out.slice(start)) if (!it.transform) {
        const bx = it.vis ? it.vis.x : it.x, by = it.vis ? it.vis.y : it.y;
        it.transform = tfm; it.origin = `${r2(ax - bx)}px ${r2(ay - by)}px`;
      }
    };
    const walkInner = (el, clip, opacity, zIn = []) => {
      const cs = getComputedStyle(el);
      // stacking path: the z-indexes of every positioned ancestor; the flat export is sorted by it (nested
      // stacking contexts compare like tuples, so a z:5 child of a z:1 box stays under a z:2 sibling)
      const zNow = cs.position !== 'static' && cs.zIndex !== 'auto' ? [...zIn, parseInt(cs.zIndex)] : zIn;
      if (cs.display === 'none' || cs.visibility === 'hidden') return;
      const op = opacity * parseFloat(cs.opacity);
      if (op < 0.01) return;
      const tag = el.tagName.toLowerCase();
      const r = el.getBoundingClientRect();
      pseudoCheck(el);
      const clips = ['hidden','clip'].includes(cs.overflowX) || ['hidden','clip'].includes(cs.overflowY);
      const myClip = clips ? inter(clip, r) : clip;

      if (tag === 'img') {
        if (!el.naturalWidth) { warn.push(`p${pi + 1}: image failed to load ${el.getAttribute('src')}`); return; }
        const holder = el.parentElement;
        const hcs = getComputedStyle(holder);
        const vis = inter(clip, r);
        if (vis.right - vis.left < 1 || vis.bottom - vis.top < 1) return;
        const pos = cs.objectPosition.split(' ');
        out.push({z: zNow, kind: 'img', src: el.currentSrc || el.src, ...rel(r), vis: rel({left: vis.left, top: vis.top, width: vis.right - vis.left, height: vis.bottom - vis.top}),
                  nw: el.naturalWidth, nh: el.naturalHeight, fit: cs.objectFit, pos,
                  mask: (cs.clipPath !== 'none' ? cs.clipPath : (hcs.clipPath !== 'none' ? hcs.clipPath : null)),
                  maskBox: rel(cs.clipPath !== 'none' ? r : holder.getBoundingClientRect()),
                  radius: (radii(cs, r).some(v => v > 0) ? radii(cs, r) : radii(hcs, holder.getBoundingClientRect())), opacity: op, alt: el.alt || '',
                  texture: !!el.closest('[data-texture]')});
        return;
      }
      if (tag === 'svg') {
        const clone = el.cloneNode(true);
        const src = [el, ...el.querySelectorAll('*')], dst = [clone, ...clone.querySelectorAll('*')];
        src.forEach((s, i) => { const c = getComputedStyle(s);
          ['fill','stroke','stroke-width','opacity','font-family','font-size','font-weight'].forEach(p => dst[i].setAttribute(p, c.getPropertyValue(p))); });
        clone.setAttribute('width', r.width); clone.setAttribute('height', r.height);
        clone.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
        clone.removeAttribute('style'); clone.removeAttribute('class');
        clone.removeAttribute('opacity');  // the root's opacity is already in op; keeping both applied it twice
        out.push({z: zNow, kind: 'svg', svg: new XMLSerializer().serializeToString(clone), ...rel(r), opacity: op});
        return;
      }
      // shape: painted background / border / gradient
      const bgImg = cs.backgroundImage !== 'none' ? cs.backgroundImage : null;
      const sides = ['Top','Right','Bottom','Left'].map(s => ({w: px(cs[`border${s}Width`]), s: cs[`border${s}Style`], c: cs[`border${s}Color`]}));
      const hasBorder = sides.some(b => b.w > 0 && b.s !== 'none');
      if ((painted(cs.backgroundColor) || bgImg || hasBorder) && el !== pg && el !== trim && r.width > 0 && r.height > 0) {
        if (cs.clipPath !== 'none') warn.push(`p${pi + 1}: ${el.tagName.toLowerCase()}.${[...el.classList].join('.')} is a colour field with a clip-path — Canva imports it as a rectangle; draw curved fields as SVG (imagery.py motif)`);
        out.push({z: zNow, kind: 'shape', ...rel(r), bg: painted(cs.backgroundColor) ? cs.backgroundColor : null,
                  bgImg: bgImg && /gradient/.test(bgImg) ? bgImg : null,
                  borders: sides.map(b => b.w > 0 && b.s !== 'none' ? `${b.w}px ${b.s} ${b.c}` : 'none'),
                  radius: cs.borderRadius, clipPath: cs.clipPath !== 'none' ? cs.clipPath : null,
                  opacity: op, blend: cs.mixBlendMode, transform: cs.transform !== 'none' ? cs.transform : null});
      }
      // text leaf: has own text and only inline children
      const kids = [...el.children];
      const isLayout = /flex|grid|table/.test(cs.display) && kids.length > 0;
      if (isLayout && ![...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim())) { for (const k of kids) walk(k, myClip, op, zNow); return; }
      const hasText = [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim()) || (el.textContent.trim() && kids.every(k => INLINE.has(k.tagName.toLowerCase())));
      if (hasText && kids.every(k => INLINE.has(k.tagName.toLowerCase()))) {
        const lines = lineRects(el);
        if (!lines.length) return;
        const base = {kind: 'text', tag, style: styleOf(el, TEXT_PROPS), lh: cs.lineHeight, lhpx: px(cs.lineHeight) || px(cs.fontSize) * 1.2,
                      align: cs.textAlign, wmode: cs.writingMode, transform: cs.transform !== 'none' ? cs.transform : null,
                      opacity: op, indent: cs.textIndent, hyph: cs.hyphens, wrap: cs.textWrap || cs.textWrapStyle || ''};
        // group line boxes into columns
        const cols = [];
        lines.sort((a, b) => a.left - b.left || a.top - b.top).forEach(q => {
          const c = cols.find(c => Math.abs(c.left - q.left) < Math.max(12, r.width * 0.25) || (q.left < c.right - 2 && q.right > c.left + 2 && cs.writingMode.startsWith('horizontal')));
          if (c) { c.left = Math.min(c.left, q.left); c.right = Math.max(c.right, q.right); c.top = Math.min(c.top, q.top); c.bottom = Math.max(c.bottom, q.bottom); }
          else cols.push({left: q.left, right: q.right, top: q.top, bottom: q.bottom});
        });
        if (cols.length === 1 || !cs.writingMode.startsWith('horizontal')) {
          // use the container width (keeps alignment semantics) and the ink height
          const bl = px(cs.borderLeftWidth) + px(cs.paddingLeft), bt = px(cs.borderTopWidth) + px(cs.paddingTop);
          const br = px(cs.borderRightWidth) + px(cs.paddingRight), bb = px(cs.borderBottomWidth) + px(cs.paddingBottom);
          const box = {left: r.left + bl, top: r.top + bt, width: r.width - bl - br, height: Math.max(1, r.height - bt - bb)};
          out.push({z: zNow, ...base, ...rel(box), html: serial(el)});
        } else {
          // paragraph broken across columns: split the text at each column start
          cols.sort((a, b) => a.left - b.left);
          const idx = textIndex(el), txt = el.textContent;
          let prev = 0;
          const colW = r.width / cols.length;
          cols.forEach((c, ci) => {
            let end = txt.length;
            if (ci < cols.length - 1) {
              const next = cols[ci + 1].left - 1;
              let lo = prev, hi = txt.length - 1;
              while (lo < hi) { const mid = (lo + hi) >> 1; const q = charRect(idx, mid);
                if (q && q.left >= next) hi = mid; else lo = mid + 1; }
              end = lo;
            }
            const piece = txt.slice(prev, end).replace(/\s+/g, ' ').trim();
            if (piece) out.push({z: zNow, ...base, x: r2(c.left - T.left), y: r2(c.top - T.top), w: r2(Math.max(c.right - c.left, colW - 2)), h: r2(c.bottom - c.top),
                                 html: piece.replace(/&/g,'&amp;').replace(/</g,'&lt;'), split: true});
            prev = end;
          });
        }
        return;
      }
      for (const k of kids) walk(k, myClip, op, zNow);
    };
    for (const k of [...pg.children]) walk(k, pageClip, 1);
    return {w: r2(T.width), h: r2(T.height), bg: getComputedStyle(pg).backgroundColor, els: out,
            fonts: [...new Set([...document.fonts].filter(f => f.status === 'loaded').map(f => `${f.family.replace(/["']/g,'')}|${f.weight}|${f.style}`))]};
  }).concat([{warnings: warn}]);
}
"""

MASK_RE = {
    "circle": re.compile(r"circle\(\s*([\d.]+)(%|px)?\s*(?:at\s+([\d.]+)(%|px)\s+([\d.]+)(%|px))?\s*\)"),
    "ellipse": re.compile(r"ellipse\(\s*([\d.]+)(%|px)\s+([\d.]+)(%|px)\s*(?:at\s+([\d.]+)(%|px)\s+([\d.]+)(%|px))?\s*\)"),
    "polygon": re.compile(r"polygon\((.+)\)"),
}


def _len(v, unit, ref):
    v = float(v)
    return v / 100 * ref if unit in (None, "%") else v


def mask_image(size, mask, radius, box, vis):
    """Build an L-mode alpha mask (size = output px) for a clip-path/border-radius defined on `box`
    (css px), when the output shows the region `vis` (css px) of the page. Drawn supersampled so
    curved edges (wave and blob frames) come out anti-aliased.
    >>> box = {"x": 0, "y": 0, "w": 100, "h": 100}
    >>> m = mask_image((100, 100), "polygon(evenodd, -10% 0%, 50% 0%, 50% 100%, -10% 100%, bad)", None, box, box)
    >>> m.getpixel((0, 50)), m.getpixel((45, 50)), m.getpixel((55, 50))
    (255, 255, 0)
    >>> mask_image((100, 100), None, [40, 0, 0, 0], box, box).getpixel((1, 1)), mask_image((100, 100), None, [40, 0, 0, 0], box, box).getpixel((98, 1))
    (0, 255)
    """
    from PIL import Image, ImageDraw
    size0 = size
    ss = max(1, min(4, 8000 // max(size)))  # 4x for small frames, capped so full pages stay in memory
    W, H = size = (size[0] * ss, size[1] * ss)
    sx, sy = W / vis["w"], H / vis["h"]
    m = Image.new("L", size, 0)
    d = ImageDraw.Draw(m)
    bx, by = (box["x"] - vis["x"]) * sx, (box["y"] - vis["y"]) * sy
    bw, bh = box["w"] * sx, box["h"] * sy
    if mask and mask.startswith("circle"):
        g = MASK_RE["circle"].search(mask)
        if not g:
            return None
        ref = math.hypot(box["w"], box["h"]) / math.sqrt(2)
        rad = _len(g.group(1), g.group(2), ref)
        cx = _len(g.group(3) or 50, g.group(4) or "%", box["w"]); cy = _len(g.group(5) or 50, g.group(6) or "%", box["h"])
        d.ellipse([bx + (cx - rad) * sx, by + (cy - rad) * sy, bx + (cx + rad) * sx, by + (cy + rad) * sy], fill=255)
    elif mask and mask.startswith("ellipse"):
        g = MASK_RE["ellipse"].search(mask)
        if not g:
            return None
        rx = _len(g.group(1), g.group(2), box["w"]); ry = _len(g.group(3), g.group(4), box["h"])
        cx = _len(g.group(5) or 50, g.group(6) or "%", box["w"]); cy = _len(g.group(7) or 50, g.group(8) or "%", box["h"])
        d.ellipse([bx + (cx - rx) * sx, by + (cy - ry) * sy, bx + (cx + rx) * sx, by + (cy + ry) * sy], fill=255)
    elif mask and mask.startswith("polygon"):
        pts = []
        body = re.sub(r"^\s*(evenodd|nonzero)\s*,", "", MASK_RE["polygon"].search(mask).group(1))
        for p in body.split(","):
            try:  # keep minus signs; skip calc() and anything else we can't place
                xs, ys = p.strip().split()[-2:]
                fx = _len(float(re.sub(r"[^\d.-]", "", xs)), "%" if xs.endswith("%") else "px", box["w"])
                fy = _len(float(re.sub(r"[^\d.-]", "", ys)), "%" if ys.endswith("%") else "px", box["h"])
            except ValueError:
                continue
            pts.append((bx + fx * sx, by + fy * sy))
        if len(pts) < 3:
            return None
        d.polygon(pts, fill=255)
    elif radius and (max(radius) if isinstance(radius, list) else radius) > 0:
        rs = radius if isinstance(radius, list) else [radius] * 4  # tl, tr, br, bl
        d.rectangle([bx, by, bx + bw, by + bh], fill=255)
        for (cx, cy, sgx, sgy), r in zip(((bx, by, 1, 1), (bx + bw, by, -1, 1), (bx + bw, by + bh, -1, -1), (bx, by + bh, 1, -1)), rs):
            r = min(r, box["w"] / 2, box["h"] / 2) * sx
            if r <= 0:
                continue
            ox, oy = cx + sgx * r, cy + sgy * r  # corner square cleared, then its quarter-circle redrawn
            d.rectangle([min(cx, ox), min(cy, oy), max(cx, ox), max(cy, oy)], fill=0)
            d.ellipse([ox - r, oy - r, ox + r, oy + r], fill=255)
    else:
        return None
    return m.resize(size0, Image.BOX) if ss > 1 else m  # BOX = coverage average, no ringing


def load_image(src, base):
    from PIL import Image
    if src.startswith("data:"):
        return Image.open(io.BytesIO(base64.b64decode(src.split(",", 1)[1])))
    return Image.open(src_path(src, base))


def src_path(src, base):
    """file:///C:/x.png becomes C:/x.png on Windows; Path(u.path) used to give a broken '/C:/x.png'."""
    u = urlparse(src)
    return Path(url2pathname(u.path)) if u.scheme == "file" else (base / src)


def to_srgb(im):
    """Convert a photo with an embedded non-sRGB colour profile (ProPhoto, Adobe RGB, Display P3) to sRGB, as the
    browser does when it renders the page; re-encoding without this washes the colours out in the editable file.
    >>> from PIL import Image, ImageCms
    >>> im = Image.new("RGB", (4, 4), (200, 40, 40)); to_srgb(im).getpixel((0, 0))
    (200, 40, 40)
    >>> im.info["icc_profile"] = ImageCms.ImageCmsProfile(ImageCms.createProfile("LAB")).tobytes(); to_srgb(im).mode
    'RGB'
    """
    icc = im.info.get("icc_profile")
    if not icc:
        return im
    from PIL import ImageCms
    try:
        prof = ImageCms.ImageCmsProfile(io.BytesIO(icc))
        if "srgb" in ImageCms.getProfileDescription(prof).lower().replace(" ", ""):
            return im
        alpha = im.getchannel("A") if im.mode in ("RGBA", "LA") else None
        out = ImageCms.profileToProfile(im.convert("RGB"), prof, ImageCms.createProfile("sRGB"), outputMode="RGB")
        if alpha is not None:
            out.putalpha(alpha)
        return out
    except Exception:
        return im   # a broken profile: keep the pixels as they are


def crop_image(e, base, scale_cap=4.0, q=None):
    """Reproduce object-fit / object-position cropping and page clipping at native resolution.
    q = encoding level (see LEVELS): scale cap in CSS px, JPEG quality, and whether transparent images use a palette."""
    q = q or LEVELS[0]
    from PIL import Image
    im = to_srgb(load_image(e["src"], base))
    # transparent noise textures at 10–25% opacity need little resolution; faint background photos keep more
    scale_cap = min(scale_cap, q["scale"], (0.5 if im.mode in ("RGBA", "LA", "P") else 2.0) if e.get("texture") else 99)
    im.load()
    nw, nh = im.size
    w, h = e["w"], e["h"]
    fit = e["fit"]
    if fit == "contain":
        s = min(w / nw, h / nh)
    elif fit in ("fill",):
        s = None
    else:  # cover / none / scale-down treated as cover
        s = max(w / nw, h / nh)
    def pct(v, free):
        return float(v[:-1]) / 100 * free if v.endswith("%") else float(re.sub(r"[^\d.-]", "", v) or 0)
    if s is None:
        sx_, sy_ = w / nw, h / nh; ox = oy = 0
    else:
        sx_ = sy_ = s
        ox = pct(e["pos"][0], w - nw * s); oy = pct(e["pos"][1] if len(e["pos"]) > 1 else "50%", h - nh * s)
    v = e["vis"]
    # visible region in source pixels
    x0 = (v["x"] - e["x"] - ox) / sx_; y0 = (v["y"] - e["y"] - oy) / sy_
    x1 = x0 + v["w"] / sx_; y1 = y0 + v["h"] / sy_
    src_box = [max(0, x0), max(0, y0), min(nw, x1), min(nh, y1)]
    if src_box[2] - src_box[0] < 1 or src_box[3] - src_box[1] < 1:
        return None, None
    crop = im.convert("RGBA" if im.mode in ("RGBA", "LA", "P") else "RGB").crop([round(c) for c in src_box])
    # the visible rect may be larger than the image (contain): place into canvas of v size
    out_w = max(1, round(v["w"] / sx_)); out_h = max(1, round(v["h"] / sy_))
    cap = scale_cap * 96 / 25.4 * 25.4  # keep ≤ ~4× css px (≈ 380 ppi) to bound file size
    k = min(1.0, (v["w"] * scale_cap) / out_w)
    out_w, out_h = max(1, round(out_w * k)), max(1, round(out_h * k))
    canvas = Image.new("RGBA", (out_w, out_h), (0, 0, 0, 0))
    dx = round((max(0, x0) - x0) * k); dy = round((max(0, y0) - y0) * k)
    cw = round((src_box[2] - src_box[0]) * k); ch = round((src_box[3] - src_box[1]) * k)
    canvas.paste(crop.resize((max(1, cw), max(1, ch)), Image.LANCZOS).convert("RGBA"), (dx, dy))
    alpha = mask_image((out_w, out_h), e.get("mask"), e.get("radius"), e.get("maskBox") or v, v)
    if alpha is not None:
        from PIL import ImageChops
        canvas.putalpha(ImageChops.multiply(canvas.getchannel("A"), alpha))
    has_alpha = (alpha is not None or crop.mode == "RGBA" or fit == "contain") and canvas.getchannel("A").getextrema()[0] < 255
    uri = encode(canvas, has_alpha, q, texture=e.get("texture"))
    if has_alpha and not e.get("texture"):
        ALPHA.append((uri, canvas))   # full-colour transparent image: a palette candidate if the file is over budget
    return uri, (out_w, out_h)


# size-budget ladder: every element and style is kept; only the image encoding steps down until the file fits.
# At each level transparent images start as full PNG; the largest are palette-encoded first, only as far as needed.
LEVELS = [{"scale": 4.0, "jpeg": 88, "palette": False}, {"scale": 3.2, "jpeg": 86, "palette": False},
          {"scale": 2.6, "jpeg": 84, "palette": False}, {"scale": 2.2, "jpeg": 82, "palette": False},
          {"scale": 2.0, "jpeg": 80, "palette": False}]   # last resort: 192 ppi, still sharp for editing in Canva
ALPHA = []


def fit_budget(doc, budget):
    """Palette-encode the largest full-colour transparent images, biggest first, until doc fits the budget (bytes)."""
    size = len(doc.encode("utf-8"))
    for uri, canvas in sorted(ALPHA, key=lambda t: -len(t[0])):
        if size <= budget:
            break
        new = encode(canvas, True, {"palette": True, "jpeg": 0})
        if len(new) < len(uri):
            doc = doc.replace(uri, new); size -= (len(uri) - len(new)) * doc.count(new)
    return doc


def encode(im, has_alpha, q, texture=False):
    """Image → data URI. Opaque → JPEG. Transparent → PNG; with q["palette"] (and always for low-opacity textures)
    a palette PNG with alpha (undithered: dithering multiplies PNG size).
    >>> from PIL import Image
    >>> im = Image.new("RGBA", (40, 30), (200, 30, 30, 255)); im.putpixel((0, 0), (0, 0, 0, 0))
    >>> [encode(im, a, LEVELS[1])[:14] for a in (True, False)]
    ['data:image/png', 'data:image/jpe']
    """
    from PIL import Image
    buf = io.BytesIO()
    if has_alpha:
        if q["palette"] or texture:
            im = im.quantize(colors=8 if texture else 256, method=Image.Quantize.FASTOCTREE,
                             dither=Image.Dither.NONE)   # undithered palettes stay small; pencil texture and photo detail hide banding
        im.save(buf, "PNG", optimize=True); mime = "image/png"
    else:
        im.convert("RGB").save(buf, "JPEG", quality=q["jpeg"], optimize=True, progressive=True); mime = "image/jpeg"
    return f"data:{mime};base64," + base64.b64encode(buf.getvalue()).decode()


def font_links(families):
    """Google Fonts css2 link for the families/weights actually used."""
    fam = {}
    for f in families:
        name, wt, st = f.split("|")
        if name.lower() in ("serif", "sans-serif", "monospace", "system-ui"):
            continue
        for w in (wt.split() if " " in wt else [wt]):
            if w.isdigit():
                fam.setdefault(name, set()).add((1 if st == "italic" else 0, int(w)))
    parts = []
    for name, axes in sorted(fam.items()):
        axes = sorted(axes)
        spec = ("ital,wght@" + ";".join(f"{i},{w}" for i, w in axes)) if any(i for i, _ in axes) \
            else ("wght@" + ";".join(str(w) for _, w in axes))
        parts.append(f"family={name.replace(' ', '+')}:{spec}")
    return f'<link rel="stylesheet" href="https://fonts.googleapis.com/css2?{"&".join(parts)}&display=swap">' if parts else ""


def _covers(face, chars):
    """Does this @font-face block's unicode-range cover any character the document uses?
    >>> _covers("unicode-range: U+0000-00FF, U+0131;", {65}), _covers("unicode-range: U+0400-045F;", {65}), _covers("src: x;", set())
    (True, False, True)
    """
    m = re.search(r"unicode-range:\s*([^;]+);", face)
    if not m:
        return True
    for part in m.group(1).split(","):
        a, _, b = part.strip()[2:].partition("-")
        lo, hi = (int(a.replace("?", "0"), 16), int(a.replace("?", "F"), 16)) if "?" in a else (int(a, 16), int(b, 16) if b else int(a, 16))
        if any(lo <= c <= hi for c in chars):
            return True
    return False


def embedded_fonts(html_path, chars=None):
    """Inline the project's local @font-face files (from fonts.css) as base64 — only the unicode subsets the text uses."""
    base = html_path.parent
    css_out = []
    for link in re.findall(r'<link[^>]+href=["\']([^"\']+\.css)["\']', html_path.read_text(encoding="utf-8")):
        p = (base / link)
        if not p.exists() or "fonts" not in p.name and "font" not in p.read_text(encoding="utf-8")[:2000]:
            continue
        css = p.read_text(encoding="utf-8")
        if "@font-face" not in css:
            continue
        def rep(m):
            f = (p.parent / m.group(2)).resolve()
            if not f.exists():
                return m.group(0)
            mime = "font/woff2" if f.suffix == ".woff2" else (mimetypes.guess_type(str(f))[0] or "font/ttf")
            return f"url('data:{mime};base64,{base64.b64encode(f.read_bytes()).decode()}')"
        css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
        if chars is not None:   # drop subsets (vietnamese, cyrillic…) the document never uses
            css = re.sub(r"@font-face\s*\{[^}]*\}", lambda m: m.group(0) if _covers(m.group(0), chars) else "", css)
        css_out.append(re.sub(r"url\((['\"]?)([^)'\"]+)\1\)", rep, css))
    return "\n".join(css_out)


def build(pages, html_path, fonts_mode="both", q=None):
    base = html_path.parent
    warnings = pages[-1]["warnings"]; pages = pages[:-1]
    families = sorted({f for p in pages for f in p["fonts"]})
    head = []
    if fonts_mode in ("link", "both"):
        head.append(font_links(families))
    style = ["*{box-sizing:border-box;margin:0;padding:0}",
             "body{background:#d9dadd;padding:24px 0}",
             ".page{position:relative;overflow:hidden;margin:0 auto 24px;box-shadow:0 2px 10px rgba(0,0,0,.25)}",
             ".page>*{position:absolute;margin:0}",
             ".page>p{white-space:normal;overflow-wrap:normal}",
             "@media print{body{background:none;padding:0}.page{margin:0;box-shadow:none;break-after:page}}"]
    if fonts_mode in ("embed", "both"):
        used = {ord(c) for p in pages for e in p["els"] if e.get("kind") == "text" for c in re.sub("<[^>]+>", "", e["html"])} | set(range(32, 127))
        style.append(embedded_fonts(html_path, used))
    body = []
    stats = {"text": 0, "shape": 0, "img": 0, "svg": 0}
    for pi, p in enumerate(pages):
        W, H = round(p["w"]), round(p["h"])
        els = []
        for e in sorted(p["els"], key=lambda e: tuple(e.get("z") or (0,))):  # unpositioned = level 0, so negative z sorts below  # z-index order (stable: DOM order breaks ties)
            k = e["kind"]; stats[k] += 1
            pos = f'left:{e["x"]}px;top:{e["y"]}px;width:{e["w"]}px;height:{e["h"]}px'
            op = f';opacity:{round(e["opacity"], 3)}' if e.get("opacity", 1) < 0.999 else ""
            if k == "shape":
                st = [pos]
                if e["bg"]: st.append(f'background-color:{e["bg"]}')
                if e["bgImg"]: st.append(f'background-image:{e["bgImg"]}')
                t, r_, b, l = e["borders"]
                for side, v in zip(("top", "right", "bottom", "left"), (t, r_, b, l)):
                    if v != "none": st.append(f"border-{side}:{v}")
                if e["radius"] and e["radius"] not in ("0px", "0px 0px 0px 0px"): st.append(f'border-radius:{e["radius"]}')
                if e["clipPath"]: st.append(f'clip-path:{e["clipPath"]}')
                if e["blend"] and e["blend"] != "normal": st.append(f'mix-blend-mode:{e["blend"]}')
                if e["transform"]: st.append((f'transform:{e["transform"]}' + (f';transform-origin:{e["origin"]}' if e.get("origin") else '')))
                els.append(f'<div data-kind="shape" style="{";".join(st)}{op}"></div>')
            elif k == "img":
                if re.search(r"\.svg([?#]|$)", e["src"], re.I):  # PIL can't open SVG: embed the vector as-is
                    uri = "data:image/svg+xml;base64," + base64.b64encode(src_path(e["src"], base).read_bytes()).decode()
                    els.append(f'<img data-kind="graphic" style="{pos};object-fit:{e["fit"]};'
                               f'object-position:{" ".join(e["pos"])}{op}" src="{uri}">')
                    continue
                uri, px_ = crop_image(e, base, q=q)
                if not uri:
                    continue
                v = e["vis"]
                tfs = (";" + (f'transform:{e["transform"]}' + (f';transform-origin:{e["origin"]}' if e.get("origin") else ''))) if e.get("transform") else ""
                els.append(f'<img data-kind="image" alt="{e["alt"].replace(chr(34), "")}" '
                           f'style="left:{v["x"]}px;top:{v["y"]}px;width:{v["w"]}px;height:{v["h"]}px{tfs}{op}" src="{uri}">')
            elif k == "svg":
                uri = "data:image/svg+xml;base64," + base64.b64encode(e["svg"].encode()).decode()
                tfs = (";" + (f'transform:{e["transform"]}' + (f';transform-origin:{e["origin"]}' if e.get("origin") else ''))) if e.get("transform") else ""
                els.append(f'<img data-kind="graphic" style="{pos}{tfs}{op}" src="{uri}">')
            elif k == "text":
                st = [f'left:{e["x"]}px;top:{e["y"]}px;width:{e["w"] + 1:.2f}px', e["style"],
                      f'line-height:{e["lh"]}', f'text-align:{e["align"]}']
                if e["wmode"] and not e["wmode"].startswith("horizontal"):
                    st.append(f'writing-mode:{e["wmode"]};height:{e["h"]}px')
                if e["transform"]: st.append((f'transform:{e["transform"]}' + (f';transform-origin:{e["origin"]}' if e.get("origin") else '')))
                if e.get("indent") and e["indent"] not in ("0px",): st.append(f'text-indent:{e["indent"]}')
                if e.get("hyph") == "auto": st.append("hyphens:auto")
                for wv in ("balance", "pretty"):
                    if wv in (e.get("wrap") or ""): st.append(f"text-wrap:{wv}")
                tag = "h2" if e["tag"] in ("h1", "h2", "h3") else "p"
                els.append(f'<{tag} data-kind="text" style="{";".join(st)}{op}">{e["html"]}</{tag}>')
        body.append(f'<div class="page" data-document-role="page" data-page="{pi + 1}" '
                    f'style="width:{W}px;height:{H}px;background:{p["bg"]}">\n' + "\n".join(els) + "\n</div>")
    title = re.search(r"<title>(.*?)</title>", html_path.read_text(encoding="utf-8"), re.S)
    doc = ("<!doctype html>\n<html lang=\"en\"><head><meta charset=\"utf-8\">"
           f"<title>{title.group(1).strip() if title else html_path.stem} — editable</title>\n"
           + "\n".join(head) + "\n<style>\n" + "\n".join(style) + "\n</style></head>\n<body>\n"
           + "\n".join(body) + "\n</body></html>\n")
    return doc, stats, warnings


def fidelity(original_html, editable_path, out_dir, dpi=60):
    """Screenshot both versions page by page and compare."""
    from playwright.sync_api import sync_playwright
    from PIL import Image, ImageChops, ImageStat
    scores, pairs = [], []
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        shots = {}
        for label, path, sel in (("orig", original_html, ".page .trim"), ("edit", editable_path, ".page")):
            pg = b.new_page(device_scale_factor=dpi / 96)
            pg.goto(Path(path).resolve().as_uri(), wait_until="load")
            pg.evaluate("document.fonts.ready.then(() => true)")
            pg.add_style_tag(content=".page{box-shadow:none!important}")
            shots[label] = [Image.open(io.BytesIO(el.screenshot())).convert("L") for el in pg.query_selector_all(sel)]
        b.close()
    for i, (a, e) in enumerate(zip(shots["orig"], shots["edit"])):
        from PIL import ImageFilter
        e = e.resize(a.size)
        # blur first so sub-pixel anti-aliasing and JPEG noise don't count as layout differences, and compare at the
        # best alignment within one device pixel: the original's pages sit on fractional device pixels, the editable's on whole ones
        A = a.resize((a.width * 2, a.height * 2), Image.BILINEAR).filter(ImageFilter.GaussianBlur(3))
        E = e.resize(A.size, Image.BILINEAR).filter(ImageFilter.GaussianBlur(3))
        m, diff = min(((ImageStat.Stat(d).mean[0], d) for d in (ImageChops.difference(A, ImageChops.offset(E, dx, dy))
                        for dx in (-2, -1, 0, 1, 2) for dy in (-2, -1, 0, 1, 2))), key=lambda t: t[0])
        diff = diff.resize(a.size)
        s = 100 - m / 255 * 100 * 4   # mean abs diff, amplified
        scores.append(round(max(0, s), 1))
        pairs.append((a, e, diff))
    # diff sheet: original | editable | difference for each page
    if pairs:
        w, h = pairs[0][0].size
        sheet = Image.new("L", (w * 3 + 40, (h + 20) * len(pairs)), 200)
        for i, (a, e, d) in enumerate(pairs):
            y = i * (h + 20)
            sheet.paste(a, (0, y)); sheet.paste(e, (w + 20, y)); sheet.paste(ImageChops.invert(d.point(lambda v: min(255, v * 4))), (2 * w + 40, y))
        sheet.save(Path(out_dir) / "editable-diff.png")
    return scores


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("html")
    ap.add_argument("--out")
    ap.add_argument("--fonts", choices=["link", "embed", "both"], default="both")
    ap.add_argument("--no-check", action="store_true")
    ap.add_argument("--max-mb", type=float, default=8, help="size budget for the editable file (Canva import); image encoding steps down until it fits")
    a = ap.parse_args()
    from playwright.sync_api import sync_playwright
    html = Path(a.html).resolve()
    out = Path(a.out) if a.out else html.parent / "out"
    out.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        p = b.new_page(viewport={"width": 1600, "height": 1800})
        p.goto(html.as_uri(), wait_until="load")
        p.evaluate("document.fonts.ready.then(() => true)")
        p.wait_for_function("Array.from(document.images).every(i => i.complete)", timeout=60000)
        p.add_style_tag(content=":root{--bleed:0mm!important}")
        pages = p.evaluate(JS)
        b.close()
    dest = out / f"{html.stem}.editable.html"
    # exact colours first: step resolution down to 250 ppi; only then palette-encode the largest transparent images
    plan = [(0, False), (1, False), (2, False), (2, True), (3, True), (4, True)]
    for li, pal in plan:   # every element and style is kept; only image encoding steps down
        ALPHA.clear()
        doc, stats, warnings = build(pages[:-1] + [{**pages[-1], "warnings": list(pages[-1]["warnings"])}], html, a.fonts, LEVELS[li])
        if pal:
            doc = fit_budget(doc, a.max_mb * 1e6)
        if len(doc.encode("utf-8")) <= a.max_mb * 1e6:
            break
    dest.write_text(doc, encoding="utf-8")
    mb = round(dest.stat().st_size / 1e6, 2)
    if mb > a.max_mb:
        warnings.append(f"editable file is {mb} MB, over the {a.max_mb} MB budget even at the lightest encoding: split the document or place fewer large photos")
    res = {"editable": str(dest), "pages": len(pages) - 1, "elements": stats, "size_mb": mb,
           "encoding": {**LEVELS[li], "palette": pal, "photo_ppi": round(LEVELS[li]["scale"] * 96)}, "warnings": warnings}
    if not a.no_check:
        sc = fidelity(html, dest, out)
        res["fidelity_pct"] = sc
        low = [i + 1 for i, s in enumerate(sc) if s < 97]
        if low:
            res["check_pages"] = low
            res["diff_sheet"] = str(out / "editable-diff.png")
    print(json.dumps(res, indent=2))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")  # Windows consoles default to cp1252 and crash on ■ — “
    main()
