---
id: quote-cover
family: cover
registers: [catalog]
loud: true
seen_in: ["house-10 turf quotation: PROJECT title, 3-cell spec row, prepared-for band"]
---
# Quotation cover

**Why it works:** A quotation is read by one client. Putting their name, their project and its three key numbers on page 1 makes the document theirs before a price appears.

**Anatomy**
```
┌─────────────────────┐
│ LOGO   company      │  logo band
│ [site photo 40%]    │  one of the company's own projects
│ PROJECT             │  eyebrow
│ Artificial Turf     │  2-line title, line 2 in accent
│ Construction        │
│ SIZE │ AREA │ STD   │  3-cell spec row on hairlines
├─────────────────────┤
│ Prepared for: Name, │  dark footer band:
│ City · Ref · Date · │  client, ref no, date, validity
│ Valid until         │
└─────────────────────┘
```

**Rules**
- Client name, reference number, date and validity on the cover.
- Three numbers that define the job (size, area, standard or capacity), each with its unit.
- The photo is one of the company's own completed projects.

**Goes generic when**
- Clip-art figures or swooshes around the photo.
- The same cover for every client with only the name changed and no project numbers.

**Build notes:** `band-stack` skeleton; spec row as a 3-column grid with `.label` over `.stat-n`; footer band on `var(--accent)`.
