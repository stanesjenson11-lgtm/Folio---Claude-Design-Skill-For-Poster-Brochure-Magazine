# wizard: the guided flow for a new piece

Used by `/folio:new`, `/folio:magazine`, `/folio:brochure`, `/folio:poster` (type already answered), every style command (style already answered), `/folio:styles`, and on claude.ai by plain words ("make a magazine from this PDF", "turn this text into a brochure"). It reads everything first, asks only what is missing in three short rounds, shows a page plan for approval, shows a first look, then builds.

This is folio's **default** for anything new: `/folio` alone or with content starts it, with no `/plan` and no sub-command needed. Rules: never ask what the user already stated in the request (take it and say so); facts found in the content are confirmed, not re-asked; at most three questions per round; every question has a recommended option (first, marked "(Recommended)" with a one-line reason) and accepts "You choose". "You choose everything" in round 1 skips to the plan with the recommended answers. Styles come only from the kit catalogue (`kit.py list`: the shipped kits plus the user's own) or a mix of two kits; nothing is invented outside it.

## 0. Platform
- **Claude Code:** plan mode is the default for every new piece. Before anything else, call `EnterPlanMode`; if it is listed only as a deferred tool, load it first (`ToolSearch` with `select:EnterPlanMode`). Scan and ask in plan mode (reading files is allowed; nothing is written); the page plan is presented with `ExitPlanMode`, and the build starts after approval. Questions: `AskUserQuestion`. Already in plan mode (the user typed `/plan`)? Just continue. If the switch is declined, run the same rounds and approve the plan in chat.
- **claude.ai / Claude desktop chat:** no plan mode and no slash commands. Questions: `ask_user_input_v0` (max 3 questions, 2–4 options each). Uploads are in `/mnt/user-data/uploads`; put anything the user should see or download (swatch sheet, gallery, first look, deliverables) in `/mnt/user-data/outputs`. Show the page plan as a table and ask "Go ahead · Change something". If a download fails (fonts, stock photos), say once: turn on Settings → Capabilities → code execution network access for all domains, or upload the photos.
- **Anywhere else:** one message with numbered options per round.
- **Showing an image to the user:** Claude Code opens it in the system viewer (`start "" <file>` on Windows, `open <file>` on macOS, `xdg-open <file>` on Linux); claude.ai copies it to the outputs folder.

## 1. Scan (ask nothing yet)
Read everything supplied: PDF (read the text; extract its photos with `extract` after approval), docx, pasted text, a website, logo files, photos, reference images, a Canva link. Also check the folio home (`python <skill>/scripts/kit.py home`) for a saved brand: `clients/<slug>/BRAND.md` matching the company name found in the content.

Pull out the facts into `source.md` (never invent any): company or event name, people with their roles, email, phone, website, address, figures. Inventory the photos: count, pixel size, subject (people, action, product, place), which can carry a full page, which could be cut out (a person or object on a clean background).

Say it in one compact block:
```
Found: report.pdf (2,400 words, 6 photos: 2 team, 3 product, 1 building), email + phone + website, no logo, 1 reference image.
Saved brand: none.
```

## 2. Round 1
- **Logo** (only if none was found): Attach it now (Recommended) · A LOGO placeholder box (swap it in Canva) · A text wordmark from "<name>". With a saved brand, ask instead: "Use <name>'s saved brand (logo, colours, contacts)? Yes (Recommended) · No, new look".
- **What** (skip when the command says it): Magazine · Brochure or company book · Poster · (Other: e-book, newsletter, catalogue, flyer).
- **Words:** Premium copy from my content (Recommended; `brief.md` level Moderate, facts only) · Keep my text word for word (Verbatim) · Light polish (Light).

"Attach it now": wait for the logo before round 2.

## 3. Round 2
- **Colour:** make the palettes first, then ask.
  - Logo: `python <skill>/scripts/palette.py --from-image <logo> --industry "<subject>" --out palette`. A typed brand colour: `--brand <hex>`. Nothing: `--industry "<subject>"` alone.
  - Show `palette/swatches.png`. Options A, B, C from `palette/options.json`, each as *name — why — suits <styles>*:
    - A is the logo's own colours, contrast-fixed ("gold fails as text on white, so headings use deep navy and gold stays on numbers");
    - B and C are the engine's alternatives ("warmer", "stands apart from other IT firms' blue");
    - add "Keep my exact colours".
  - Name the styles each palette suits:

    | Palette | Suits |
    |---|---|
    | Dark or saturated (navy, black, royal blue, deep red) | Night, Football Blue, Sport News |
    | Warm neutrals (espresso, ivory, champagne, sage) | Ivory, Old-money Classic Book |
    | Bright pairs (teal + orange, yellow + grey, lime + blue) | Pop Stripe, Split Pop, Skate Culture |
    | Mono + one colour (white, black, one green, blue or orange) | Business Newsletter, Winter Editorial, Minimal E-book |
- **Kind:** open `kits/GALLERY.png` (plus the user's own gallery at `<home>/kits/GALLERY.png` when it exists) before asking.
  - Magazine: Sports & action · Editorial & minimal · Pop & colour · Business & news, recommending the family whose top kit ranks best.
  - Brochure: the format first: Booklet or company book (Recommended for 8+ pages of content) · Tri-fold · Bi-fold · (Other: Z-fold, gate…; `formats.md`). The kind follows in round 3.
  - Poster: follow `formats.md` → Poster variants and `library/TASTE.md` (4 variants in the loved family). Skip Kind and Style; round 3 asks the event details and size.
- **Photos:** Use mine · Free stock photos from my industry (the `/folio:stock` steps) · Mix: mine for people and products, stock for the rest · Empty frames to fill in Canva. Recommend "Use mine" when there are enough strong photos for the page count (about one per page), "Mix" when some, stock when none.

## 4. Round 3
- **Style:** the top 3 kits for the chosen kind, ranked (below), each "name — one-line look — why it fits", plus "Mix two styles". For a brochure fold, offer the kits whose look carries to that format (palette, type, devices adapted to the fold grid in `formats.md`).
  - A reference image was supplied: ask "Your reference: Copy it 1:1 (Recommended) · Use it as inspiration for <best kit> · Ignore it". A 1:1 copy follows `/folio:replicate`, then the learn gate (§9).
- **Contacts:** "Use what I found: <name · email · phone · web>" (Recommended) · I'll type them · Placeholders to fill later. If nothing was found: I'll type them · Placeholders.
- **Pages:** the kit's own count (Recommended) · 8 · 12 · 16. Printed booklets stay a multiple of 4.

## 5. Ranking styles
Each kit's `KIT.md` has `best_for:` (subjects, tone, photos it needs, pages); `kits/INDEX.md` repeats it. Score each kit in the chosen kind:
- **Subject:** the content's nouns vs `best_for`.
- **Photos:**
  - the supply vs what the kit needs (a cut-out person for sport covers; 6+ strong photos for Winter or Sport News);
  - black-and-white or mixed photos suit Newsletter;
  - few or no photos suit Old-money book or Minimal E-book.
- **Length:** words vs pages (a thin text suits 8 pages).
- **Colour:** the chosen palette's fit (table above).
- **Taste:** styles marked user-loved in `library/TASTE.md` (Ivory, Night, Pop Stripe, Split Pop) rank higher.

The best one is marked "(Recommended)" and its reason names the deciding facts ("you have three action photos and a navy logo").

## 6. Mix two styles
Ask (one round, two questions): **Base** (grid, page archetypes, devices) and **Look** (colours and display font), each from the catalogue.
- Build: `kit.py new <base> <project> --brand <look's brand> --accent <look's accent>`.
- Then set the base's display-font variable in `:root` to the look's display face, and fetch it with `fonts.py`.
- Keep the base's page roles, cross-fold devices and density.
- Say which is which in the plan. A mix the user loves can go through the learn gate (§9).

## 7. The plan (for approval)
One table, one row per page (spreads as pairs):

| Page | Layout (kit archetype) | Headline (draft) | Content | Photo | Notes |
|---|---|---|---|---|---|
| 1 | cover: masthead behind a cut-out person | "Built to ship." | intro | your `team-02.jpg`, cut out | logo bottom left |
| 2–3 | contents + studio note, box across the fold | "Inside" | sections 1–5 | stock: code on screens | — |
| … | | | | | |
| 12 | back cover | "Let's build it" | contacts | your `office.jpg` | email, phone, web, address |

- **Photos:**
  - the strongest goes to the cover or the first opener; people go to the people pages; products go to the feature spreads;
  - a gap names the stock subject that fills it;
  - the user can move any photo by saying so ("put photo 3 on page 5").
- **Also list:** style (or mix), palette (hexes), fonts, page count and size, outputs (print PDF with bleed, Canva file), and anything still missing.
- **Approval:** Claude Code presents it with `ExitPlanMode`; elsewhere show it and ask "Go ahead · Change something".

## 8. Build, first look, deliver
1. **Start:** `kit-flow.md` step 3 (`kit.py new` with the chosen palette's `--brand` / `--accent`). Save the user's photos to `img/raw/`. Make every photo slot from the plan (grade, cut-out, stock, mockups), and fill every `data-kit-sample` element with the approved copy.
2. **First look:** render the cover and the first spread only (`render.py <file>.html --pages 1-3 --no-editable` plus the kit's flags). Show the PNGs, then ask "Carry on (Recommended) · Change something". Apply changes before building the rest.
3. **Build and check:** the remaining pages, then the full render; look at every page. Preflight must show 0 errors and 0 warnings; the Canva file must match at ≥ 97% and stay ≤ 8 MB.
4. **Deliver:** the PDF, the contact sheet and the Canva-editable HTML.
   - Add a **still-to-fill list**: every `logo-placeholder`, empty `slot-photo` frame and `[[TK: …]]` left, with its page and how to finish it in Canva. For example: "p1 and p12: LOGO box. In Canva, open the editable file, click the box, Replace, upload your logo."
   - Nothing marked `data-kit-sample` may remain (preflight ERRORs).
5. **Verdict and brand:**
   - Ask which pages work and record the verdict (`taste.md`).
   - Offer "Save <name>'s brand for next time?":
     - **Claude Code:** write `<home>/clients/<slug>/` with the logo file and `BRAND.md` (name, people and roles, email, phone, web, address, chosen palette hexes, fonts, the style used).
     - **claude.ai:** offer the same folder as `folio-brand-<slug>.zip` in outputs, to upload next time or keep in a claude.ai Project.

## 9. Learn gate (after a 1:1 copy of a reference, or a loved mix)
**Default: do not add.** Find the closest kit in the catalogue, then score the reference and that kit 1–5 on six points:
- spread composition and cross-fold connection;
- type scale contrast;
- a 3–4 colour palette;
- density (no empty areas);
- layering and texture;
- print safety (readable contrast, no decorative hairlines, no upside-down or bottom-to-top headings).

**Offer "Save as a new style?" only when all three hold:**
- it beats the closest kit by 3 or more points in total;
- it breaks none of the bans in `library/TASTE.md`;
- it is not a near-duplicate (same family, same devices) of a kit already in the catalogue.

Otherwise it stays in this job only. Say so in one line with the scores ("Not added: it scores 21 vs Sport News 24; same yellow-panel devices").

**Saving:** `python <skill>/scripts/kit.py save <project> <id> --name "…" --family "…"`, then complete its `KIT.md` (including `best_for`) and run `kit.py gallery`.
- **Installed plugin:** it lands in the folio home with a personal command `/folio-<id>`.
- **Maintainer:** from the git checkout it lands in the shipped catalogue with `/folio:<id>`.
- **claude.ai:**
  1. copy the skill folder to a writable place;
  2. run that copy's `kit.py save … --builtin`;
  3. zip the copy as `folio.skill` into outputs, and tell the user to upload it under Settings → Capabilities → Skills.
