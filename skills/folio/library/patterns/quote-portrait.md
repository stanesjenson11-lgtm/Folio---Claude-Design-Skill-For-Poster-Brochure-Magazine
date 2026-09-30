---
id: quote-portrait
family: text
registers: [corporate, magazine]
loud: false
seen_in: ["ref-01 message from the director", "ref-04 CEO leadership insight", "ref-02 message from the CEO", "ref-08 editor's letter"]
---
# Quote + portrait

**Why it works:** A leader's message becomes human when a large pull quote, a portrait and a signature share the page. The portrait's mask comes from the book's motif (circle, arc), and a ghost word ('CEO') can add scale.

**Anatomy**
```
┌─────────────────────┐
│ Message from   “    │   title 28–40pt, 2 weights
│ the Director   quote│   pull quote 18–24pt
│ ░░ photo ░░  ≈≈≈≈≈≈ │   letter: 2 cols at body size
│ ░░░░░░░░░░░  ≈≈≈≈≈≈ │
│ caption box  ≈≈≈≈≈≈ │
│              Sign.  │   signature (image/script) + name,
│           (◯portrait│   title; portrait masked, on the
└─────────────────────┘   OUTER edge, may bleed off it
```

**Rules**
- Portrait sits on the outer edge (never the spine), eyes toward the text.
- Letter stays at body size in 2 columns; the quote carries the scale.
- Signature line: name bold, title regular, 7.5–8.5pt.

**Goes generic when**
- Portrait small and square next to the heading like a profile card.
- Letter set at 12pt across the full width.

**Build notes:** Portrait `.ph.mask-circle`; place with `right: -20mm` on a recto / `left:-20mm` on a verso. Preflight's spine-mask check catches wrong-side placement.
