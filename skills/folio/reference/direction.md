# direction — art direction before pixels

A direction is a structural grammar plus type behaviour plus a motif plus a colour strategy. It is not a colour: the named directions in `library/directions/` are re-coloured with the client's brand.

The intake gate (`reference/intake.md`) runs this step interactively: it proposes three directions from different schools, a palette from `palette.py`, and a boldness level, asks once, then locks the result here. Use the procedure below to prepare those options or when the user asked you to decide.

## Procedure
1. **Three physical tone words** from the brief ("civic, sunlit, orderly"; "gritty, floodlit, loud"; "engineered, marine, exact"). Not "modern", "clean", "professional".
2. **Name the reference lane.** Pick from `library/directions/` or a real-world lane ("Swiss corporate report", "Nike training-magazine", "Muji catalogue", "The Economist data page"). If the user uploaded references, the lane comes from them — say which images and what exactly you are taking (grid? motif? type contrast? photo treatment?).
3. **Colour strategy** (Restrained / Committed / Full / Drenched) and the role map: paper, ink, ink-2, brand, brand-ink, tint, accent. Existing brand colours are kept; the direction decides how much surface they get.
4. **Typography** via `reference/typography.md`: display + body (+ optional label), weights, the size ladder for this page size.
5. **Motif** — one shape family used everywhere (cover crop, image masks, tabs, chart shapes, dividers).
6. **Photo treatment** — natural / duotone / B&W / cut-out, and the crop rule (tight, horizon low, gaze inwards).
7. **Pattern set** — 6–10 patterns from `library/patterns/` this book may use. Fewer patterns, reused with variation, is more coherent than twenty.

When the user has not chosen, offer three directions **from different schools** (structural · warm institutional · confident colour · editorial-expressive — see intake.md), each with a flagship reference, three vibe words and one sentence on what it means for this brief; never three variations of the same idea. If they asked you to decide, choose and state why in one sentence.

8. **Dials** — VARIANCE, DENSITY, VOLUME (defined in intake.md). The flatplan's loud share must match VOLUME.

Write DIRECTION.md with those eight items, then `tokens.css` (start from `palette/tokens-<id>.css`, which already passes contrast):

```css
:root{
  --paper:#fff; --ink:#0f1115; --ink-2:#3b4048; --rule:#d7dbe2;
  --brand:#EE2C27; --brand-ink:#fff; --tint:#fdecec; --accent:#0D0D0D;
  --font-display:'Archivo', sans-serif; --font-body:'Source Serif 4', serif; --font-label:'Archivo', sans-serif;
  --fs-body:9.25pt; --lh-body:1.42; --fs-h2:24pt; --fs-h1:48pt; --fs-display:110pt;
}
```

## Calibration: where generated design clusters
Before locking, check the direction against the places AI-made design lands by default (after frontend-design, impeccable and taste-skill). Landing in one is allowed when the brand or register requires it; landing there by default is not.
1. Warm cream paper + high-contrast serif display + terracotta, clay, brass or oxblood accent + espresso ink.
2. Near-black ground + one acid-green, vermilion or neon accent (folio's `night-court` and `signal-yellow` live here: earn it with the client's brand, not by reflex).
3. Broadsheet: hairline rules, zero radius, dense newspaper columns (folio's own default grammar, so choose it, don't drift into it).
4. The SaaS card kit: rounded white cards, shadows, icon + heading + text.
5. Template chrome that appears whatever the subject (SKILL.md bans).
**Second-order reflex** (after impeccable): avoiding the reflex font but landing in a saturated lane (editorial-typographic, Swiss-grid-with-one-accent, drenched-centred-cover) is the same trap one level deeper. **Similar-brief test** (after frontend-design): if a similar client in the same industry would get this same plan, change the part that is generic and say what changed. **Rotate palette families** across this user's projects (compare with past stamps; `library/HOUSE.md` names the studio's own habits).

**Narrative spine** (after taste-skill): name the one metaphor the book carries (an archive, a journey, an instrument, a stage, a field report) and let openers, captions and the motif follow it. One line in DIRECTION.md.

## Style tile (for bigger jobs)
Before building 20+ pages, build the cover and one interior spread only, render them, and show the contact sheet. It is ten times cheaper to change direction now.
