# taste — learn the user's choices and keep improving

Folio gets better for this user in three ways: it remembers verdicts (`library/TASTE.md`, portable), it recalls them through claude-mem when that plugin is installed, and it studies new references from the web in the lanes the user likes.

## 1. Before designing (every intake, every variant set)
1. Read `library/TASTE.md`. Its **Defaults** override the library's general rules: default direction, headline orientation, photo frame shape, motifs to avoid.
2. If claude-mem tools exist, recall what TASTE.md may not have yet:
   ```
   search query="folio taste verdict poster brochure" limit=10     → IDs
   get_observations ids=[…]                                         → the verdicts in full
   ```
   Also `search query="<client> design feedback"` for a returning client. Skip silently when the tools are missing.
3. Say it in the Design Read, one line: "Using your taste: Arc Stage family, horizontal headlines, rectangular photos."

## 2. After every delivery: ask, then record
1. Ask for a verdict with the question tool (one question per variant set, multi-select): *Which of these work?* Options: each variant by name, plus "None — tell me why". If the user already said it in words, don't ask again.
2. Record it in **three** places:
   - `library/TASTE.md` → add a dated row to the Log (what exactly they loved or rejected, with the concrete traits: font, ground, header position, frame shape, texture), then update **Defaults** if the verdict changes one.
   - The conversation → say it plainly in one line starting with "Taste recorded:", so claude-mem's observer captures it in the default worker runtime ("Taste recorded: loved Arc — condensed headline crossing a rectangular photo; rejected rotated headlines.").
   - claude-mem server-beta runtime only → `observation_add kind="folio-taste" content="…" metadata={liked:[…], disliked:[…]}`.
3. Turn repeated verdicts into rules: two rejections of the same trait → add it to Defaults → *Avoid*; a loved design → write or update its direction card (as `arc-stage` was).
4. Tell the user in one line what changed: "Taste updated: posters now default to Arc Stage."

## 3. Keep improving from the web (`learn`)
Run on request (`/folio learn [lane]`), or on a schedule the user sets up (for example a weekly cloud routine via `/schedule`).
1. Pick the lane from TASTE.md (the loved direction, or the lane the user names).
2. `WebSearch` for professional work in that lane on sources that serve images without a login: Behance, Dribbble, designer portfolios, typographicposters.com, fontsinuse.com, poster archives. Pinterest is login-walled and its pins are other people's work: study pins only when the user saves them and uploads the images.
3. Download 4–6 preview images to `library/references/web/<yyyy-mm>-<slug>.jpg` (private study material, never shipped or reused as artwork) and **look at each**.
4. Write `library/references/web/NOTES.md`: source URL, designer, what matches the loved grammar, 1–3 concrete moves worth adopting, what to avoid.
5. Fold the best moves into the direction card and pattern cards (grammar only: layout moves, type behaviour, texture, info-block ideas), log them in `library/references/SOURCES.md`, and add one CHANGELOG line.
6. Report in three lines: what was studied, what was added, what to try on the next job.

Never copy a reference's artwork, copy, photos or logos; the goal is better grammar, not a clone. For a deliberate near-replica of a licensed template, see `reference/replica.md`.
