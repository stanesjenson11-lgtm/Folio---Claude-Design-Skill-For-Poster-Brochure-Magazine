---
id: band-stack
family: opener
registers: [catalog, corporate]
loud: true
seen_in: ["ref-03 marine airbag catalog (every product family)"]
---
# Band stack

**Why it works:** The page is sliced horizontally: a full-bleed photo band on top (40–55%), a title band, then the content zone. Repeated for every section it turns a catalog into a system — the reader knows where they are by the band alone.

**Anatomy**
```
┌─────────────────────┐
│░░░░░ PHOTO ░░░░░░░░░│   top 40–55%, bleeds top + sides
│░░░░░░░░░░░░░░░░░░░░░│
│ MARINE BUOYANCY  ◀──│   title on photo bottom-left or in
│ AIRBAGS  second-lang│   a brand band; bilingual as 2 sizes
├─────────────────────┤
│ ◉ feature  ◉ feature│   content: 2–3 cols, icons as
│ ≈≈≈≈≈≈≈   ≈≈≈≈≈≈≈   │   small line glyphs only
│ ▭ ▭ ▭ ▭ ▭ (strip)   │   optional photo strip at bottom
└─────────────────────┘
```

**Rules**
- Band height identical on every section opener.
- Title always in the same position and size.
- Second-language line smaller and lighter, same left edge.

**Goes generic when**
- Band heights vary by section.
- Title moves around.
- Content zone becomes a card grid.

**Build notes:** Photo `.ph` with `inset: var(--b0) var(--b0) 50% var(--b0)`; title `.box` at the band edge; content in `.live` rows 9–16.
