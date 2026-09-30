---
id: numbered-index
family: contents
registers: [corporate, catalog, magazine]
loud: true
seen_in: ["ref-02 contents spread (navy)", "ref-03 contents band 01–07", "ref-06 table of contents (dark)", "ref-08 contents with brand column"]
---
# Numbered index

**Why it works:** Contents pages become graphics when page numbers are set as display numerals and the list is short. The reader sees the structure of the whole book in one glance.

**Anatomy**
```
┌─────────────────────┐
│ TABLE OF            │   title in two weights
│ CONTENTS            │
│ 04        07        │   numerals 40–70pt (accent or white)
│ EDITOR'S  ELITE     │   entry title 9–12pt bold caps
│ note…     note…     │   one-line description 7.5–8.5pt
│ 05        08        │
│ FEATURE   SKILL     │
└─────────────────────┘
```

**Rules**
- 5–9 entries; group sub-items under them if more.
- Numerals are real page numbers of the section openers — preflight/polish verifies they match.
- Set on a loud page (drench, dark, or a photo with a quiet side).
- Vertical 'CONTENT(S)' title along the spine or outer edge is a strong variant (vertical-title).

**Goes generic when**
- A dotted-leader list at body size.
- Page numbers that don't match the rendered PDF.

**Build notes:** Grid of blocks in `.live`; numerals `font: 800 58pt/.85 var(--font-display)`; verify against `out/pages`.
