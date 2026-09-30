# intake — the slash-command gate (theme, palette, how bold)

Runs when the user starts a new piece: `/folio` with content, `/folio craft | brief | direction`, or any build request where no `DIRECTION.md` exists yet. Skip it when `DIRECTION.md` already exists (the direction is locked — follow it), for `critique`, `polish`, `preflight`, `extract`, `export`, `promo`, and when the user has already named both theme and palette (then just confirm them in the Design Read).

The gate asks **once**. Never ladder follow-up questions; unanswered items are inferred and stated.

## 1. Pre-flight scan (before asking anything)
Read the folder and attachments first — asking for something the user already supplied wastes their time.
- logo files (`logo*`, `*.svg`, a logo inside a brand-guide PDF) → brand colours with `palette.py --from-image logo.png`
- brand guide / previous brochures (PDF) → colours and fonts via `harvest.py` tokens or `pdffonts`
- an existing `DIRECTION.md` / `tokens.css` / folio stamp from an earlier job for this client → identity to preserve
- photos: count, pixel sizes, how many can print full-page at A4 (≥ 2480 px on the long side)
- copy files (word count per section), sketches, reference images
- claude-mem corpus answers when available (reference/memory.md)

Emit one compact block with what was found and what folio will keep vs. propose:
```
Pre-flight: logo.png → maroon #7d1f35 + brass #c99a2e · 23 photos (6 can carry a full A4 page) ·
copy.docx ~4,800 words · 2 sketches (cover, p2) · no brand fonts found
Keeping: logo colours, sketch structure. Proposing: theme, type, motif, palette roles.
```
If nothing is found, one line: "Pre-flight: no brand assets found — proposing from the brief."

## 2. Design Read (one line)
"Reading this as: **<piece>** for **<audience>**, <register> register, leaning toward **<lane>** — <pages> pp <size>, <print | screen>."

## 3. Prepare the options
**Themes — three directions from different schools**, never three variations of one idea:
| School | Directions |
|---|---|
| Structural / architectural | navy-column, harbor-band, Swiss grid |
| Warm institutional | civic-arc, field-green |
| Confident colour | ink-drench (drenched covers) |
| Editorial / expressive | night-court, signal-yellow, blaze-editorial |
Mark the best fit for register + industry + the user's references as *recommended*. Each option label: name + a 6–10 word description of what the pages will look like ("Civic Arc — big maroon arcs over campus photos").

**Palettes** — run `python <skill>/scripts/palette.py --brand <hex> [--brand2 <hex>] [--industry "<industry words>"] --out palette` (or `--from-image logo.png`, or `--industry` alone when there's no brand). Show `palette/swatches.png` to the user *before* the question so they choose by eye. Option A is the client's own colours; B and C are the engine's alternatives; add "Keep my exact colours".

**How bold** (the VOLUME dial): Calm (about 1 page in 4 loud) · Balanced (1 in 3) · Bold (1 in 2, drenched openers).

## 3b. Brochure type and style (brochures only)
Ask these in the same round when the piece is a brochure and the brief doesn't say (list the full set in the question text; offer the likeliest three as options, the rest via "Other"):
- **Type:** Bi-Fold, Tri-Fold, Z-Fold, Accordion, Gate, Double Gate, Roll, French, Double Parallel, Booklet (`reference/formats.md`).
- **Magazine styles (kits, `kits/INDEX.md`, `/folio:styles` or a named style command):** ask the family first (Sport & action · Editorial & minimal · Pop & colour · Business & news), then the kit in that family, then theme colour (kit colours / brand colour / you choose) and pages (8 / 12 / 16). Show `kits/GALLERY.png` first.
- **Style:** Corporate, Minimalist, Editorial / Magazine (`sport-layers` **Ivory**, the user's loved magazine look, or **Night**, dark and high-contrast; `pop-culture`), Neomorphism, Brutalist, Retro / Vintage, **Old-money classic book** (`old-money-book`, the user's loved book look), or "Replicate my reference 1:1" when reference pages were supplied.

## 4. Ask once
Use the platform's question tool so the user can tap: claude.ai → `ask_user_input_v0` (max 3 questions, 2–4 options each); Claude Code → `AskUserQuestion`; otherwise one message with numbered options. Always include a "You choose" / "Go ahead" path.

Default questions: **Theme**, **Palette**, **How bold**. If page size or output (print vs screen) cannot be inferred from the brief, replace **How bold** with **Format** ("A4 printed", "A5 printed", "Screen PDF", "Square") and infer boldness from the chosen theme.

Example (school annual report, maroon logo):
- Theme: Civic Arc — maroon arcs over campus photos *(recommended)* · Navy Column — architectural slabs, condensed caps · Ink Drench — drenched maroon covers, big numerals · You choose
- Palette: A · Your maroon + brass *(recommended)* · B · Maroon + muted teal · C · Cobalt Civic · Keep my exact colours
- How bold: Calm · Balanced *(recommended)* · Bold

## 5. Better-alternative check (after the answer, before building)
Say each point in one sentence, then proceed with the user's choice — do not re-ask.
- **Palette audit** (`palette.py --check` on the chosen colours): apply every *fix* automatically and say what changed ("gold fails as text on white, so headings use deep maroon and gold stays on numerals"); mention *notes* (CMYK dullness, cream paper).
- **Category reflex:** if the pick is the industry default (school → blue + building; turf academy → black + neon; finance → navy + gold) and no brand rule requires it, name one alternative that would stand apart. Once.
- **Content fit:** does the material support the theme? (Drenched themes need few but strong photos; Civic Arc needs architecture or landscape; magazine lanes need action photos.) If not, say which pages will suffer and what would help.
- **Print:** vivid RGB brand colours → ask for CMYK/Pantone values and a hard proof.

## 6. Lock
Write `DIRECTION.md` (lane, dials, colour strategy, type, motif, photo treatment, pattern set) and `tokens.css` (from `palette/tokens-<id>.css` + type roles). Add the stamp comment to the HTML head (reference/critique.md). From here on, the direction is followed, not re-litigated.

## Dials (adapted from taste-skill)
| Dial | 1 | 10 | Corporate | Catalog | Magazine |
|---|---|---|---|---|---|
| VARIANCE — grid discipline vs. deliberate breaks | strict Swiss grid | frequent overlaps, cut-outs, bleeding type | 3–5 | 2–4 | 6–9 |
| DENSITY — air vs. information per page | gallery-airy | packed spec sheets | 3–5 | 6–8 | 4–6 |
| VOLUME — share of loud pages | 15% | 60% | 25–35% | 30–40% | 40–55% |
Record the values in DIRECTION.md; the flatplan's loud/quiet column must match VOLUME within ±10%.
