# refs — turn reference images into layout knowledge

The library grows every time the user shares inspiration. The goal is to learn the *grammar* (grid moves, type contrast, motif, rhythm), never to copy a template's artwork, logos, copy or photos.

## Where references come from
- Images the user uploads or pastes (Pinterest pins, Behance shots, photos of printed brochures, screenshots of PDFs). Pinterest itself is behind a login and its pins are other people's copyrighted work, so do not scrape it; ask the user to save the pins they like and upload them, or give direct image URLs.
- Web search for named lanes ("Swiss annual report grid", "Müller-Brockmann poster", "Kinfolk layout") is fine for studying ideas; describe what you learn in words.

## Procedure per image (or per board)
1. Identify the piece type and register (corporate / catalog / magazine) and every page or spread visible in the mockup.
2. For each distinct layout, decide whether it matches an existing card in `library/patterns/` (then add the image to that card's `seen_in` and any new variation) or is new (then write a new card).
3. Write what makes it *not generic* in one or two sentences — this is the valuable part. ("The cover's giant circle is cropped by the page edge, so the circle reads as a window, not a sticker.")
4. Extract the direction-level signals: colour strategy and roles, type behaviour (weights, case, scale jumps), motif, photo treatment. If it's a new lane, write a card in `library/directions/`.
5. Update `library/INDEX.md`.

## Pattern card format (library/patterns/<id>.md)
```markdown
---
id: arc-window
family: cover | opener | contents | text | quote | data | gallery | profile | map | closer
registers: [corporate, catalog, magazine]
loud: true
seen_in: ["ref: school annual report (blue arcs), user board 2026-09"]
---
# Arc window
**Why it works:** …one or two sentences…
**Anatomy:** ASCII wireframe + element list with grid positions/insets
**Rules:** 3–6 bullets
**Goes generic when:** 1–3 bullets
**Build notes:** folio.css classes, clip-paths, sizes
```

## House references (the user's own past work)
The user's own designs are a different kind of reference from Pinterest boards: they show what this studio already does, for clients folio will meet again.
- **Getting them from Canva:** share links (`canva.link/…`) → `resolve-shortlink` → `read-design` with thumbnails for every page (export is often disabled on shared designs; thumbnails are enough for grammar) → one contact sheet per design with PIL → `library/references/house/<slug>.png`, logged in SOURCES.md as `house-NN`. Exported PDFs or PNGs dropped in the folder work the same way.
- **Critique before encoding.** House work mixes studio-grade moves with Canva-template habits (icon-in-circle rows, glass cards, "Why choose us" grids, centred everything). Encode the strong moves as pattern cards; list the template habits under "Don't carry over" in `library/HOUSE.md`, so folio learns the studio's taste and not the template's. Canva templates the user only lightly edited (placeholder text such as "reallygreatsite.com" is the giveaway) are third-party refs, not house work.
- **House signature → `library/HOUSE.md`:** recurring choices across the user's work, per-client systems for returning clients, and what folio should do better than the originals.
- **Client material stays with its client.** Logos, photos, names and copy in house refs are never reused in another client's piece. House copy is a voice sample for `reference/copy.md` only where the user wrote it; if it carries AI tells, take its vocabulary, not its tells.

## Store the source
Save the reference image under `library/references/<yyyy-mm>-<slug>.jpg` with a line in `library/references/SOURCES.md` (URL or "user upload", date, what was taken). Keep references in the user's copy of the plugin; they are private study material, not assets to ship in client work.

If claude-mem is available, also follow the "after a project" step in `reference/memory.md` so the corpus knows the new patterns exist.
