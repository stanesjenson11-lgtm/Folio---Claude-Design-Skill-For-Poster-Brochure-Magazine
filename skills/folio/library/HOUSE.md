# House style: what this studio already does

Distilled from 15 of the user's own delivered pieces (house-01 … house-15: annual report, event poster series, kids' poster book, product and quotation brochures, catalog, data sheet, trifolds, trade-show panels, stage backdrop). The contact sheets, per-design notes and per-client systems live in `references/house/`, which is private and never ships. Read this file at Setup with INDEX.md.

It has two jobs: carry the studio's strengths into every piece, and fix the habits the originals picked up from Canva templates. **Returning client?** Read their section in `references/house/CLIENTS.md` (if present) at intake; follow their system unless the brief asks for a redesign.

## The signature (keep)
- **Dark drenched grounds with one warm or hot accent:** navy→plum with amber and gold, near-black with gold, black and white with scarlet as punctuation, navy drench for export work. Covers, dividers and back covers share one ground, so colour does the navigation (house-01, 02, 09, 15).
- **Condensed heavy caps for display,** often in two-line stacks set solid, with widely tracked small caps for labels and big numerals as proof: a founding year, a count of projects delivered (house-09, 10, 15).
- **The client's own place as the hero image:** floodlit night aerials of pitches, factory lines, a building whose signage becomes the headline. The strongest asset in every job (house-04, 09, 11).
- **Poster instinct:** one giant word, a figure in front of it, light (beams, backlight) used as a graphic device (house-03, 05).
- **Bilingual Tamil and English** with hard scale contrast between the scripts (house-05).
- **Punctuation as motif:** an accent full stop after a title, number chips on photos, pill tags (house-09).
- **Engineering literacy:** dimension tables keyed to drawings, spec label/value pairs on hairlines (house-07, 09).

## Upgrade on every job
| Habit in the originals | Folio's rule |
|---|---|
| Each section in a different template skin (filigree, black rules, florals, marble) | One grid, one type pair and one motif for the whole book; sections differ by colour ground and pattern |
| 5–15 typefaces per piece; a new font for each poster in a series | Display + body (+ label) per design. A consistent **series** changes photos and words, not fonts; deliberate **variants** (the poster default) each get their own pair |
| Missing folios, a frozen "PAGE 2", contents without page numbers, wrong "05/14" | folio.css counters; contents built from real page numbers |
| Template leftovers shipped: placeholder photos, "reallygreatsite.com", striped FPO frames, stray elements | preflight ERROR `placeholder`; FPO frames only in drafts |
| Same photo or paragraph on two pages | preflight WARN `dup-image` / `dup-copy` |
| Numbers drift between pieces for one client | One FACTS.md per client, reused and dated (brief.md 1b) |
| Icon-in-circle rows, "Why choose us?" grids, glass cards, drop-shadow cards | Proof as numbers, names, certifications and photos; hairlines, not boxes |
| Justified narrow columns with rivers; white text on pale sky; body text over busy photos | typography.md measure and justification rules; text on photos only in the quiet area |
| Bottom third of a page left empty | Page-fill check: anchor, re-flow or declare `breathing` |
| Title colour sampled from each photo | Colours come from the palette roles only |
| Chatbot copy ("excellence", "seamless", "X That Transforms Y", "A • B • C" slogans) and typos | `reference/copy.md` with humanizer; names, figures and spellings checked on every build |
| Folded pieces laid out in reading order | `reference/formats.md`: impose in fold order |
| Legacy Tamil fonts (Bamini) | Unicode Tamil only (typography.md) |

## Studio reflexes (for the Variety axis)
The studio's own defaults are a reflex too: Anton or Bebas display with Poppins or Montserrat body, navy with gold, the drenched centred cover. Use them when the brand requires it. For a new client, choose against them and say so in the Design Read.

## Learned from this work
Patterns: `speaker-poster`, `series-rail`, `bilingual-lockup`, `numeral-window`, `product-cell-grid`, `spec-sheet-frame`, `quote-cover`, `estimate-sheet`, `layer-section`. Direction: `vigil`. Single-sheet and folded formats (poster, flyer, trifold, large-format panels, backdrops): `reference/formats.md`.
