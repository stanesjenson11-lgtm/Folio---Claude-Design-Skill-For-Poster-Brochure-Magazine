# critique — art-director review

Render first (`render.py`), then review the contact sheet and every page PNG. Critique the printed object, not the code. Write your own verdict from the PNGs **before** reading preflight output (after impeccable): a report anchors judgment, and a clean preflight is never proof that the design is strong.

## Scorecard (0–4 each, with one sentence of evidence per line)
| # | Criterion | 0 = generated look | 4 = studio work |
|---|---|---|---|
| 1 | Rhythm | every page same weight | planned loud/quiet sequence, openers land |
| 2 | Spread composition | two unrelated pages | one dominant element per spread, cross-gutter logic |
| 3 | Type hierarchy | medium everything | extreme, purposeful scale contrast; 3–4 clear levels |
| 4 | Typesetting | web sizes, long measures, widows | 8.5–10pt body, 40–70 cpl, clean rags |
| 5 | Grid & alignment | drifting margins | shared hang lines, edges align across pages |
| 6 | Imagery | boxed, small, low-res | bleeding, cropped with intent, consistent treatment |
| 7 | Colour | timid or rainbow | committed strategy, tints not greys |
| 8 | Motif & identity | none / clip-art | one motif carried through the book |
| 9 | Furniture | none | folios, running heads, consistent placement |
| 10 | Content integrity | invented, placeholder or chatbot-sounding copy | client copy intact, TK marked, folio's words pass reference/copy.md |

Total /40. Below 28 is not deliverable.

## Six-axis self-critique (after hallmark)
Also score 1–5: **P**hilosophy · **H**ierarchy · **E**xecution · **S**pecificity · **R**estraint · **V**ariety. Any axis < 3 → revise first. Variety is structural: compare the pattern list and dials with the stamps of this user's previous folio projects (search the workspace for `<!-- folio ·`, or ask claude-mem) — a colour swap is not variety. Write the stamp as the first comment in `<head>`:
`<!-- folio · direction: <id> · dials V<n> D<n> VOL<n> · patterns: <ids> · critique P<n> H<n> E<n> S<n> R<n> V<n> -->` Then list fixes as P0 (breaks trust or print: overflow, wrong names, low-res), P1 (makes it look generic), P2 (polish). Each fix names the page and the concrete change ("p6: move the table to cols 1–8 and bleed the photo into cols 9–12 + outer bleed").

## Also check against the user's references
If reference images were supplied, compare side by side and say honestly where the build falls short of them — usually photo scale, type contrast or rhythm.

Run `preflight.py` as part of every critique and fold its ERROR/WARN findings into the P0/P1 lists.
