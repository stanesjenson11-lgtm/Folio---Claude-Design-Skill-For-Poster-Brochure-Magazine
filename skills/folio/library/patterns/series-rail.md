---
id: series-rail
family: poster
registers: [event, magazine]
loud: false
seen_in: ["house-03 weekly service series with a fixed tagline rail", "house-05 kids virtue poster set with a refrain word and series tag"]
---
# Series rail

**Use only when the user asks for a consistent series.** The poster default is 4 unique variants (`reference/formats.md`).

**Why it works:** A weekly or themed series stays recognisable when the edges never change: the reader learns the frame, and each new poster only has to carry its own picture and words.

**Anatomy**
```
┌─────────────────────┐
│ TAGLINE · · ·   logo│   top rail: fixed position, size, face
│                     │
│   body varies:      │   photo, headline, colour lane
│   photo + headline  │   (2–3 lanes for the whole series)
│                     │
│ date/venue module   │   same module, same place every time
│ signatory  CTA  spon│   bottom rail: fixed
└─────────────────────┘
```

**Rules**
- Lock before poster 1: rails, logo corner, type pair, date format, info module, 2–3 colour lanes.
- A refrain (a repeated word or line, "… வேண்டும்", "Thursday Service") gives a set its voice; set it the same way every time.
- The series tag sits in one slot at one size; don't move it from poster to poster.
- For a book of posters, add furniture: number, date or lesson number, a verse or source slot, and a back cover.
- Check each new poster beside the previous three.

**Goes generic when**
- A new font or a new logo corner every week.
- Rails set so small (≈8pt on A3) they read as noise.

**Build notes:** One HTML file per series with `.rail-top` / `.rail-bottom` components and one `<section class="page">` per poster; tokens for the lanes (`--lane-a`, `--lane-b`).
