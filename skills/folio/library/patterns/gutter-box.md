---
id: gutter-box
family: device
registers: [magazine, corporate, catalog]
loud: false
seen_in: ["ref-12 business newsletter: green boxes that start under a photo on the left page and carry a quote or photo on the right", "ref-11 sport news: yellow panels running across the spread", "user brief 2026-09-29"]
---
# Gutter box

**Why it works:** A note box that starts on the left page and keeps going across the spine binds the two pages into one spread. The reader follows the colour, so the facts in it read as one thought: a note on the left, its proof (a small photo and a second line) on the right.

**Anatomy**
```
┌─────────── left page ───────────┬─────────── right page ──────────┐
│                                  │                                  │
│   ┌──────────────────────────────┼─────────────────────┐           │
│   │ NOTE  From first sketch      │  [small photo]  Mon–│           │
│   │ to deploy: one team…         │                 Sat…│           │
│   └──────────────────────────────┼─────────────────────┘           │
│                                  │                                  │
└──────────────────────────────────┴──────────────────────────────────┘
```

**Rules**
- One box per spread, in a support or accent colour from the palette.
- Its ground is one `.cross` element on both pages (same spread coordinates), so the halves meet exactly at the spine; the text and the photo sit in their own page's box.
- Keep text and the photo at least 9mm from the fold (preflight `spine`).
- Left half: a label and one sentence. Right half: a small rectangular photo or a sketch plus one or two facts.
- Prefer the centre spread for anything that must line up perfectly (it prints on one sheet); on other spreads a flat ground is forgiving.

**Goes generic when**
- Every spread has one; boxes with rounded shadows; a box that only carries decoration.

**Build notes:** `<div class="cross gbox" style="left:120mm; top:190mm; width:210mm; height:58mm">` on both pages; text in page-local elements with `z-index` above it. In Canva the two halves import as two shapes on consecutive pages (Canva has no facing pages).
