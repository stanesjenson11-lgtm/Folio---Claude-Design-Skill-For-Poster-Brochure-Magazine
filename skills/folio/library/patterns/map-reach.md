---
id: map-reach
family: data
registers: [corporate, catalog]
loud: false
seen_in: ["ref-02 world map with pins A–F", "ref-04 nationwide coverage map"]
---
# Map reach

**Why it works:** A single-colour map with a few labelled pins turns 'we operate in six regions' into a picture. Callout labels with thin leader lines keep it precise.

**Anatomy**
```
┌─────────────────────┐
│ NATIONWIDE          │
│ COVERAGE   ▓▓▓▓▓    │   map in brand colour, flat
│        ▓▓▓▓●▓▓▓▓──label  leader lines 0.5pt
│   ▓▓▓▓▓●▓▓▓▓        │
│ ◔ donut + legend    │
└─────────────────────┘
```

**Rules**
- Map is flat, one colour, no gradients or 3D.
- Pins mark only real locations provided by the client.
- For India/Tamil Nadu clients use an accurate, officially acceptable map outline.

**Goes generic when**
- Clip-art globe.
- Pins on places the client doesn't serve.

**Build notes:** Inline SVG map (from a trusted source such as Natural Earth, simplified); labels as HTML positioned over it.
