---
id: arc-stage
register: magazine
seen_in: ["thursday-service variant 'Arc' — loved by the user 2026-09-29 (library/TASTE.md)", "thursday-service arc family: teal, night, cream, ember"]
---
# Arc Stage

**Essence:** A stage at night. One deep ground with a soft glow and faint concentric arcs, the speaker in a plain rectangular photo like a lit doorway, and one enormous condensed word crossing the photo's edge. Everything else is small, centred or tucked into the bottom corners.

**Colour strategy:** Drenched ground (teal, navy→plum, burgundy, or a light cream variant), one light headline colour (cream, amber, rose, or deep plum on cream) and one warm accent for the sub-line, CTA and info card. Every variant in a set gets its own ground and headline colour (preflight `variant-clash`).

**Type:** A heavy condensed display for the one big word (Sofia Sans Extra Condensed 900, Big Shoulders Display 900, League Gothic; a high-contrast serif such as Gloock for the light variant), set 160–215pt on A3; a clean sans for the rest; the sub-line in widely spaced caps (0.55–0.6em); Tamil gloss in the matching companion from `typography.md`. Headlines are always horizontal.

**Anatomy (A3)**
```
┌───────────────────────────┐
│ logo                  r   │  r = tiny vertical slogan rail
│      ┌─────────────┐  a   │
│      │   photo     │  i   │  plain rectangle, portrait, centred
│      │ (rectangle) │  l   │
│  T H U R S D A Y ──────── │  huge word crossing the photo's foot
│         S E R V I C E     │  (or its top edge, or its side)
│        Tamil gloss        │
│      COME AND BE BLESSED  │  centred CTA + Tamil
│ credit          ╭──────╮  │
│ Name            │ 09   │  │  rounded accent card: day numeral,
│ signatory       │ JULY │  │  month, time, venue, sponsor
└─────────────────╰──────╯──┘
```

**Refinements from the web study** (`library/references/web/NOTES.md`, 6 Behance references, 2026-09):
- Centre the rings on the speaker's head, not the page, in low-opacity accent.
- Duotone the rectangular portrait into the ground hue; keep the accent for headline, card and CTA.
- An accent hairline rectangle, larger than the photo and offset up behind it (it stays rectangular).
- Track the sub-line to the headline's width between hairlines: "— S E R V I C E —".
- Where the headline crosses the photo it may turn translucent (the photo shows faintly through); over the ground it stays solid. Legibility first.
- Paper grain at about 5% over everything, type included (`imagery.py texture --kind grain`).
- Further variant ideas: **Keyline** (photo in an offset keyline, two or three arcs only), **Lockup** (no corner card: venue and date badges flank the headline as one bar across the photo's foot), **Monotone** (ground, photo and rings in one hue, paper-white headline, accent only on card and CTA).

**Variants inside the family:** move the crossing (photo foot · top edge · left edge · under the photo), swap the card corner or turn it into pill chips, change the texture (arcs · rings centred on the photo · arcs from a corner · soft blobs), change the display face and the ground.

**Motif:** concentric arcs or rings (`imagery.py motif --type arcs|rings --at x,y`), 35–55% opacity, never busy.

**Photography:** one real photo of the person, plain rectangle; bottom-weighted crop so the headline can cross it without covering the face.

**Pattern set:** speaker-poster, bilingual-lockup, numeral-window (anniversaries), back-cover

**Fits:** church and ministry events, talks and speaker series, concerts, conferences, sports nights, launches.

**Watch out:** the headline must never cover the face; keep the crossing to the shoulders or the foot. Keep the rail tiny and reading top-to-bottom.
