---
id: cutout-masthead
family: cover
registers: [magazine]
loud: true
seen_in: ["ref-06 basketball magazine cover", "ref-07 sport news cover", "ref-08 fitness magazine cover"]
---
# Cut-out masthead cover

**Why it works:** A cut-out figure overlaps the masthead — the head sits in front of the letters — which creates depth and says 'magazine' instantly. Cover lines stack on the free side of the figure in two weights and the accent colour.

**Anatomy**
```
┌─────────────────────┐
│ MAGAZINE NAME ██    │   masthead 100–160pt, heavy, caps
│ MAG(▲head)INE  ██   │   figure's head overlaps letters
│ cover    ███████    │
│ lines    ████████   │   cover lines: 3–5, big number first
│ 28+      ████████   │   ("28+", "20 MIN")
│ THE BIG  ████████   │
│ LINE     ████  ▌▌▌  │   barcode + issue/date
└─────────────────────┘
```

**Rules**
- Figure needs a clean alpha cut-out; face and eyes stay clear of all type.
- Masthead behind the figure (z-order: bg → masthead → figure → cover lines).
- One accent colour for key cover-line words; the rest white on dark.
- A circular badge ('20 MIN WORKOUT TIPS') at most once.

**Goes generic when**
- Cover lines everywhere, including over the face.
- Halo edges on the cut-out.
- Masthead in a thin or generic font.

**Build notes:** `.ph.cutout` with PNG; masthead `.display` with `data-allow-overlap`; z-index via DOM order. Background often a dark or saturated flat field with subtle texture.
