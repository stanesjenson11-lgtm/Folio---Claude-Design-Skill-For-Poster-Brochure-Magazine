---
id: two-tone-headline
family: device
registers: [magazine, corporate, catalog]
loud: false
seen_in: ["ref-06 FEATURE STORY / TRAINING FOCUS / ELITE PLAYERS", "ref-08 WORKOUT TIPS / HEALTHY SOLUTIONS / HUSTLE FOR THAT MUSCLE", "ref-05 ABOUT AGRICULTURE"]
---
# Two-tone headline

**Why it works:** Two lines, two voices: a small light or neutral line and a huge heavy line in the accent colour. It creates instant scale contrast and a repeatable headline system.

**Anatomy**
```
WORKOUT            ← 18–30pt, regular/medium, ink
 TIPS               ← 60–120pt, 800–900, accent, tight tracking
```

**Rules**
- The big word is the meaningful one; ratio between lines ≥ 2.5×.
- Same system for every feature headline in the book; vary only the words.
- Both lines share a left edge (optically aligned).

**Goes generic when**
- Three or more colours in one headline.
- Both lines the same size.
- Used on every heading in the book: accenting one word per headline is the commonest generated-design tell (frontend-design). Keep it to feature openers.

**Build notes:** Two spans in an h2, second with `display:block; font-size: var(--fs-display); color: var(--accent)`; nudge the big line `margin-left:-0.05em`.
