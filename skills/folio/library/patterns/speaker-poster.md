---
id: speaker-poster
family: poster
registers: [event, magazine]
loud: true
seen_in: ["house-03 weekly service and anniversary posters (≈20 finals)", "ref-10 sports magazine cover (figure in front of masthead)"]
---
# Speaker poster

**Why it works:** An event poster has three reads: what, who, when/where. A giant event name, one person cut out in front of it and a single information block give each read its own place, so the poster works from across a hall and up close.

**Anatomy**
```
┌─────────────────────┐
│ rail: tagline  logo │   fixed series rail (series-rail)
│ WORSHIP             │   event name, full width, top third
│   NIGHT  ┌──────┐   │   figure overlaps the lower letters
│          │figure│   │   cut-out 40–55% of height,
│ THU 9 OCT│      │   │   grounded on the bottom edge or a band
│ 6:30 PM  │      │   │   one info block opposite the figure
│ Hall, 1F └──────┘   │
│ GOD'S WORD BY  Name │   credit chip at the figure's shoulder
│ rail: signatory  CTA│
└─────────────────────┘
```

**Rules**
- The event name is the biggest thing on the sheet; the face is second; the info block third.
- The figure stands on something (page edge, a band, a torn-paper strip); never fade a body out at the waist.
- Date, time and venue in one block with one date format for the whole series.
- Credit as a small label + a heavy name ("GOD'S WORD BY" / name) on a tab or chip.
- Two typefaces: the display and the body. Script, if any, only for one short word and never laid over caps.

**Goes generic when**
- Bokeh blobs, glow text, 3D bubble letters or white swooshes stand in for a photo.
- Five or six faces on one poster.
- Date, time and venue scattered to three corners.

**Build notes:** Cut-out PNG with clean alpha (`.ph.cutout`, `data-allow-overlap` on the headline); info block as a real element (not `::before`) so it survives the editable export. Viewing-distance sizes in `reference/formats.md`.
