---
id: photo-strip
family: gallery
registers: [catalog, corporate]
loud: false
seen_in: ["ref-03 marine buoyancy airbags bottom strip"]
---
# Photo strip

**Why it works:** A row of 4–6 same-size thumbnails sitting on (or bleeding out of) a brand band at the page foot shows applications or variants without breaking the main layout.

**Anatomy**
```
│ … main content …    │
│█▭█▭█▭█▭█▭███████████│   brand band 30–45mm, bleeds sides
└─────────────────────┘
```

**Rules**
- Thumbnails equal size, equal gaps, aligned to grid columns.
- Band colour = brand; thumbnails may break out of the band top by a few mm.

**Goes generic when**
- Thumbnails of mixed aspect ratios.

**Build notes:** Band `.box` `inset: auto var(--b0) var(--b0) var(--b0); height:38mm`; flex row of `.ph`.
