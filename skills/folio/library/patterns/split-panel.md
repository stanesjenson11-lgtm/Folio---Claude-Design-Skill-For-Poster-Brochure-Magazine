---
id: split-panel
family: opener
registers: [corporate, catalog]
loud: true
seen_in: ["ref-03 company introduction spread", "ref-05 agriculture about spread", "ref-02 content spread"]
---
# Split panel

**Why it works:** One half (or third) of the page is a solid brand panel holding the title, the rest is photo or text. It's the quickest way to make a text-heavy page loud and to give a spread a clear left-to-right order.

**Anatomy**
```
┌───────┬─────────────┐     variants:
│ BRAND │░░ PHOTO ░░░░│     · panel 1/3 + photo 2/3
│ PANEL │░░░░░░░░░░░░░│     · panel with photo inset crossing
│ TITLE │░░░░░░░░░░░░░│       its edge (offset-block)
│ deck  │░░░░░░░░░░░░░│     · panel on verso + text recto
│       │ caption     │
│ 01 ── │             │
└───────┴─────────────┘
```

**Rules**
- Panel edge sits on a grid column line and runs off the trim (top, bottom and outer edge).
- Title in brand-ink (white) or deep shade; never grey on colour.
- When a photo crosses the panel edge, it crosses by a clear amount (≥ 12mm) — tentative overlaps look like mistakes.

**Goes generic when**
- Panel width is arbitrary (e.g. 37%).
- Panel used on every page.

**Build notes:** `.box` panel `inset: var(--b0) 66% var(--b0) var(--b0)` (verso outer side); photo `.ph` for the rest.
