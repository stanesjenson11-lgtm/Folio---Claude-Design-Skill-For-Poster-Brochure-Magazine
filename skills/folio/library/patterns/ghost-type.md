---
id: ghost-type
family: device
registers: [corporate, magazine]
loud: false
seen_in: ["ref-04 CEO ghost word", "ref-03 CONTENTS ghost", "ref-08 stacked outline FITNESS"]
---
# Ghost type

**Why it works:** A very large word or number at low contrast (outline, or 5–8% tint) behind content adds scale and texture without adding information.

**Anatomy**
```
┌─────────────────────┐
│ ▒▒▒▒▒▒▒▒ CEO ▒▒▒▒▒  │   120–240pt, outline or 5–8% tint
│  LEADERSHIP INSIGHT │   real heading sits on top
└─────────────────────┘
```

**Rules**
- Only on 1 in ~5 pages; it's a spice.
- Ghost word repeats a real word on the page (section name, year, number).
- Mark it `data-allow-edge data-allow-overlap` when it bleeds or sits behind text.

**Goes generic when**
- Ghost text behind body copy, hurting legibility.
- Used on every page.

**Build notes:** `.ghost` (outline via -webkit-text-stroke) or `.ghost-fill`; stacked outline variant: 3 copies with decreasing opacity.
