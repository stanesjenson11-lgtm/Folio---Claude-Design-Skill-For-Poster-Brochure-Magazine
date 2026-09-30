---
id: drench-cover
family: cover
registers: [corporate, catalog]
loud: true
seen_in: ["ref-04 insurance annual report (front + back)"]
---
# Drench cover

**Why it works:** The whole surface is the brand colour and the type does all the work: a huge year in a second accent colour, a big two-line title, small supporting copy. Faint tonal geometry keeps the colour from feeling flat. It signals confidence and suits finance, insurance and institutions whose photography is weak.

**Anatomy**
```
┌─────────────────────┐
│ logo     tagline    │
│                     │
│ ANNUAL              │   title 56–72pt, white
│ REPORT              │
│ 2035                │   year 90–130pt in accent
│ subline + 3 lines   │
│      (tonal arcs)   │   2–3 big shapes at ±4% lightness
│              motto  │
│ COMPANY LTD  reg no │
└─────────────────────┘
```

**Rules**
- Background is one flat brand colour; texture only from 2–3 very large tonal shapes (±3–5% lightness).
- Exactly one accent colour, used on the year/numeral and repeated inside (chart highlights, numerals).
- Back cover: same colour, only company, report name, URL, QR code, fine print.
- Section dividers reuse the cover ground with the section number and title, so colour marks the chapters (house-01).
- Title block hangs from the same left margin as interior text.

**Goes generic when**
- A gradient replaces the flat colour.
- The accent appears in five places on the cover.
- Title centred with symmetric padding.

**Build notes:** `.page` background var(--brand); tonal shapes as `.box` circles with `background: color-mix(in oklch, var(--brand) 92%, white)`; title uses `--fs-display` for the year.
