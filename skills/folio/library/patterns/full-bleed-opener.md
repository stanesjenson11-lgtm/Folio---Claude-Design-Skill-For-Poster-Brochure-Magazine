---
id: full-bleed-opener
family: opener
registers: [corporate, magazine, catalog]
loud: true
seen_in: ["ref-06 editor's note spread", "ref-04 financial highlights spread", "ref-08 lifestyle spread"]
---
# Full-bleed opener

**Why it works:** A section or feature opens with one photograph covering a whole page (or a whole spread) and the headline set into the photo's quiet area. The reader feels a chapter change without a single rule or box.

**Anatomy**
```
┌──────────────┬──────────────┐
│░░░░ PHOTO ░░░│ Welcome to   │   verso: photo bleeds 3 sides,
│░░░░░░░░░░░░░░│ the Heart…   │   headline in the calm area
│░░░(subject)░░│ body text    │   (lower left / sky)
│░░░░░░░░░░░░░░│ 2 cols       │   recto: text page or
│ EDITOR'S    ░│              │   continuation of the photo
│ NOTE ░░░░░░░░│  — Name      │
└──────────────┴──────────────┘
```

**Rules**
- Choose the photo for its empty area; the headline goes there, never over faces.
- Headline two-tone: first line light/white, key word heavy in accent.
- Folio may be omitted on the photo page; keep it on the text page.
- Across the gutter: keep faces and key detail ≥ 15mm away from the spine.

**Goes generic when**
- A dark overlay flattens the whole photo to make the text readable — instead pick a better photo area or use a local gradient only behind the type.
- Photo shrunk into a box with a margin.

**Build notes:** `.fill` or `.spread-img`; headline block `.box` positioned in mm; optional local scrim `linear-gradient(to top, rgba(0,0,0,.55), transparent 45%)` on a `.box` behind the type only.
