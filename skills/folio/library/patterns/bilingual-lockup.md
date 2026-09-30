---
id: bilingual-lockup
family: device
registers: [corporate, magazine, event, catalog]
loud: false
seen_in: ["house-05 Tamil/English virtue titles (NEED over வேண்டும்)", "ref-03 bilingual catalog headings"]
---
# Bilingual lockup

**Why it works:** Two scripts at similar sizes compete as two titles. Giving one script the lead and the other a clear supporting role (kicker above or gloss below) turns two titles into one lockup.

**Anatomy**
```
  NEED              ← kicker: minor script, caps, accent colour,
வேண்டும்             ← sits on the hero's top-left shoulder
  ~~~~~~~~            hero: lead script, 100%; optional swash under

  HAVE WISDOM       ← or: hero 100%
  ஞானம் வேண்டும்      ← gloss 35–45%, regular weight, directly under
```

**Rules**
- The minor line is 30–45% of the hero; never the same size.
- One accent colour, on the minor line only.
- Tamil is never letter-spaced or skewed. Set it about 1.1× the Latin size optically (it reads smaller at the same point size) with leading of 1.2 or more so vowel signs don't collide.
- Unicode fonts only (Hind Madurai, Mukta Malar, Catamaran, Noto Sans Tamil, Anek Tamil). Legacy encodings (Bamini, TAM) break search, copy and the PDF's text layer.
- The English comes from a published source where one exists (scripture, statute, the client's approved text), never a word-for-word back-translation.

**Goes generic when**
- Both lines in the same weight and size, stacked and centred.
- A different font pairing on every page.

**Build notes:** `fonts.py "Hind Madurai:600,700" --subsets latin,tamil`; `lang="ta"` on the Tamil span so line-breaking behaves.
