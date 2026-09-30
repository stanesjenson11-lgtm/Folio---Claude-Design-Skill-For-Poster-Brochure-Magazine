---
id: circle-portraits
family: profile
registers: [corporate]
loud: false
seen_in: ["ref-04 organizational structure", "ref-01 director portrait"]
---
# Circle portraits

**Why it works:** Leadership or team shown as a grid of same-size circular portraits with name + role underneath. Circles unify photos shot in different places.

**Anatomy**
```
◯   ◯   ◯     portraits Ø 22–32mm on A4
 NAME NAME NAME   name 8–9pt bold caps / role 7–7.5pt
 role role role
```

**Rules**
- All portraits cropped identically (eyes at the same height, ~40% from top).
- Backgrounds desaturated or replaced with the tint for consistency.
- Hierarchy by position (chair first/centre), not by size differences.

**Goes generic when**
- Mixed square and circle crops.
- Faces at different scales.

**Build notes:** `.ph.mask-circle` with `--fy` set per photo so eyes align; for a proper org chart add 0.5pt connector lines.
