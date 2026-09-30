---
id: numeral-window
family: device
registers: [corporate, event]
loud: true
seen_in: ["house-03 anniversary poster: the hall photo inside the 0 of 30"]
---
# Numeral window

**Why it works:** A milestone number with a photo of the place inside its counter says "how long" and "where" in one mark, and turns an anniversary badge into an image.

**Anatomy**
```
  ┌──┐ ┌────┐
  │  │ │▓▓▓▓│  ← photo clipped to the counter of the 0
  ┴──┘ └────┘
  YEARS OF GRACE   tracked caps under the numeral
```

**Rules**
- Only for a real milestone (years, editions, a 100th event).
- The numeral is heavy (800–900) so the counter is big; the photo is the organisation's own place.
- One numeral per book or series; repeat it small on the back cover.

**Goes generic when**
- A stock image in the counter, or photos in every letter.

**Build notes:** SVG `<text>` as a `<clipPath>` over an `<image>`. It survives the editable HTML; `background-clip:text` may not.
