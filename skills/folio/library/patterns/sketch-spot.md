---
id: sketch-spot
family: device
registers: [corporate, catalog, magazine]
loud: false
seen_in: ["user review 2026-09-29: images as little pencil sketches, not full rectangles"]
---
# Sketch spot

**Why it works:** A small coloured-pencil drawing beside the text it belongs to feels made by hand for this document; a full rectangular photo feels pasted in. Sketches share the palette, so they tie pages together.

**Rules**
- Make them with `imagery.py sketch photo.jpg --out s.png --palette "<dark>,<support>,<accent>,<paper>"`: espresso lines, support and accent strokes, paper shows through, soft irregular edge.
- Size: small to medium (a quarter to a third of the page), next to its text, never boxed, never with a border or shadow.
- One sketch may cross the gutter per spread (`.cross`), preferably on the centre spread.
- Keep sketches on light grounds; on dark grounds use a lighter tint or a photo instead.
- Size them for about 300 ppi at the placed size (`--max`), since noisy transparent PNGs are heavy.

**Goes generic when**
- Every image on the page is a sketch at the same size; sketches boxed in frames.
