# brief — content inventory and flatplan

The flatplan is the single biggest difference between a designed book and a generated one. It is decided before any HTML exists, so page variety is planned rather than hoped for.

## 1. Gather (ask only for what is missing)
Read everything the user gave: copy (docx, text, PDF), photos, logos, brand guide, reference images, sketches. Then fill BRIEF.md. Ask the user — in one message, at most three questions — only for things that change the design and cannot be inferred:
- piece type and use: printed (offset / digital print / office printer) or screen PDF, and the print size (A4, A5, square, DL trifold, magazine 230×300);
- page count constraint (saddle-stitched booklets must be a multiple of 4);
- audience and the one thing the reader should do or feel afterwards;
- brand colours and fonts if the organisation has them;
- whether the output also has to go into Canva.

## 1b. Brand assets — ask item by item, not "do you have guidelines?" (after claude-design-skill)
Ranked by how much they make the piece recognisably the client's:
1. **Logo** — vector (SVG/AI/PDF/EPS) preferred; a high-res PNG at least. Mandatory for any client piece.
2. **Brand colours** — hex or CMYK/Pantone; otherwise read them from the logo with `palette.py --from-image`.
3. **Photos** of the real place, people, products, events — originals, not WhatsApp-compressed copies.
4. **Fonts** the organisation already uses (letterheads, signage, previous brochures).
5. **Previous brochure / report** — for continuity or a deliberate break (`extract`).
6. **Verified facts** — names with designations, phone, email, address, website, registration numbers, figures with their period and source. Keep them in the client's `FACTS.md` and reuse it on their next piece, dating any figure that changes; counts that differ between a client's brochure and quotation (projects delivered, years, staff) are the most common error in past work.

## 1c. Answer before planning (after brag)
What is it, in one sentence? Who reads it, and what should they do or feel afterwards? What sets this organisation apart — the most impressive *true* claim? Which two or three photos are the visual hook? What must never be cut? Put the answers at the top of BRIEF.md; they decide the loud pages.

## 1d. Copy rewrite level (after html-magazine) — the client decides
| Level | Folio may… |
|---|---|
| **Verbatim** (default) | only fix obvious typos it reports back; add nothing but headings, captions and pull quotes taken word-for-word from the copy |
| **Light** | tighten sentences and fix flow, keeping every fact and the author's voice; list edits for approval |
| **Moderate** | rewrite for print — shorter paragraphs, stronger openings, new headlines and decks — with every change approved |
Never invent facts at any level. If the client's copy reads AI-written (a chatbot draft), say so once and offer a Light humanize pass (`reference/copy.md`). Record the level in BRIEF.md and save the approved source text as `copy.md` for `preflight --copy`.

## 2. Inventory
For each section of copy: title, word count, and the natural unit (letter, list, table, profile, gallery, timeline, stats). For each image: file, pixel size, orientation, subject, and the largest size it can print at 250 ppi (`px / 250 * 25.4` mm). Note which images are strong enough to carry a full page or spread — usually only two or three are, and they decide the loud pages.

```bash
python - <<'PY'
from PIL import Image; import glob
for f in sorted(glob.glob('img/*')):
    w,h = Image.open(f).size; print(f"{f:40} {w}x{h}  max@250ppi {w/250*25.4:.0f}x{h/250*25.4:.0f}mm")
PY
```

## 3. Sketches
If the user supplied pencil or paper layouts, run `reference/sketch.md` now; sketched pages are fixed in the flatplan and take priority over library patterns. Honour the sketch's structure; improve proportions, alignment and type.

## 4. Flatplan
Write FLATPLAN.md as a table, one row per page, grouped into spreads:

| Pg | Side | Spread | Content | Pattern | Loud/quiet | Hero image | Notes |
|----|------|--------|---------|---------|-----------|------------|-------|
| 1 | R | cover | title, year, deck | arc-window | L | p01-building.jpg | |
| 2 | V | 2–3 | director's message | quote-portrait | Q | p02-director.jpg | portrait on outer edge |
| 3 | R | 2–3 | contents | drench-index | L | – | |

Rules the flatplan must satisfy (check them explicitly before moving on):
- every section opener is loud; no more than two quiet pages in a row; never three consecutive pages with the same pattern;
- every spread has one dominant element;
- page count fits the binding (multiple of 4 for saddle stitch; covers count);
- the strongest photos are assigned to the loudest slots; weak or small photos go to galleries, strips or small inset frames;
- copy fits: estimate capacity per pattern (A4 text page in 2 columns at 9.25/13pt ≈ 650–750 words; 3 columns ≈ 850–950; with a half-page photo, halve it). If the copy overflows, add a page or change the pattern — do not shrink type below the register's body size.

Render the flatplan as a thumbnail row in the chat (ASCII or a quick sketch) and get a yes before building when the user is present. When the user said "just go", proceed and note the plan in your summary.

## BRIEF.md template
```markdown
# Brief — <client> <piece>
- Piece / size / pages / binding:
- Output: print (offset | digital) | screen | Canva
- Audience + reader's one takeaway:
- Brand: colours, fonts, logo files, rules
- Tone words (3, physical, not "modern"):
- Must include / must avoid:
- References supplied (and what to take from each):
- Open questions / TK:
```
