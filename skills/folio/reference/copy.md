# copy: words that don't read as generated (humanizer built in)

A brochure with studio layout and chatbot copy still reads as AI-made. The reader notices the copy first: "Where innovation meets excellence", "Learn. Grow. Thrive.", "More than just a school". Folio runs every word it writes through `reference/humanizer.md` (blader/humanizer), with the print exceptions below.

## What this applies to
| Text | Treatment |
|---|---|
| Headlines, decks, captions, pull-quote picks, section openers, back-cover lines, share copy, alt text: anything **folio writes** | Always. Humanizer in embedded mode: return only the final text. |
| Client copy at **Verbatim** (brief.md 1d) | Never rewrite. If it reads AI-written, say so once and offer a **Light** humanize pass. |
| Client copy at **Light / Moderate** | Humanize as part of the edit. List the changes for approval; the approved text becomes `copy.md`. |
| Names, designations, figures, addresses, legal lines, quotes from people | Untouchable at every level. |

Client copy that reads AI-written is common: the client drafted it with a chatbot. Report the three strongest tells with one before/after example each, and ask: "Want me to run a Light humanize pass? Every fact stays; you approve the result." Don't lecture.

## Process
1. **Voice sample first.** Use the client's own writing (old brochure via `extract`, website About page, letters, the owner's message) as humanizer's voice sample. No sample → take the voice from the register: corporate and NGO plain and factual; catalog precise and specific; magazine can have attitude.
2. **Every headline carries a fact from the copy:** a number, a name, a place, a year, a thing the reader can do. "126 schools visited the dome this year" beats "Inspiring young minds". If the copy has no fact to carry, write a plain label ("Programmes and fees").
3. **Run humanizer's four steps** (mark the tells, draft, check, final) on the whole set of words together, not line by line. Tells show up at the book scale: the same kind of closer on every opener, a triad in every deck.
4. **Check against the source.** No added fact, number, award, testimonial or claim. Humanizer's rule applies unchanged: an unsupported addition is an error.

## Premium from thin input (user rule)
When the client gives little (a website, a card), the copy still has to read like a premium studio wrote it:
- Build every line from a real fact: a service, a timeline, a price, a place, the industries served, the number of projects, the people. Say what the client gets (on-time delivery, the finish, one team from sketch to deploy), not adjectives about the client.
- One idea per line, concrete nouns, short sentences; confident without superlatives ("Every site ships on the date we agree" beats "We deliver world-class excellence").
- Fill a thin panel with more facts, not longer sentences: a three-step process, a timeline, logos of the tools used, the industries served.
- Anything folio infers rather than reads (a promise, a process step) carries `data-sample` so the client confirms it before print.

## Print exceptions (these override humanizer.md)
- **§21 curly quotes:** print sets real quotes and apostrophes (“ ” ’). Keep them; polish.md decides.
- **§8 dashes:** en dashes in ranges (2025–26, 9–11 am) are typesetting, keep them. In text folio writes, don't use em dashes to join clauses. In client copy, keep the client's dashes and set them consistently.
- **§2 fragments:** a short display line is normal on covers and posters when it states a fact ("Open Saturdays, 7 am"). The tell is a row of abstract one-word sentences: "Learn. Grow. Thrive." / "Bold. Modern. Yours." Ban those.
- **§20 headings:** sentence case by default. All-caps or small-caps display set by the direction is typography, not a tell.
- **§19 bold labels:** spec sheets, price lists, timetables and contact blocks are real labelled data; keep the labels. The tell is a bold label on every bullet of running prose.
- **§26 wrong reader:** does not apply; a brochure is written for a reader with no context.

## Brochure tells (in addition to humanizer §1–25)
- "Where X meets Y", "Your journey starts here", "Discover the difference", "Welcome to X, where…", "Step into…", "Experience the…"
- "More than just a…" / "Not just a school, a family" (humanizer §1 in slogan form)
- "Committed to excellence", "a one-stop solution", "tailored solutions", "a legacy of…", "trusted partner", "holistic", "state-of-the-art facilities"
- Unlock, elevate, empower, unleash, transform, redefine, seamless, world-class, cutting-edge, next-gen
- A triad in every deck: "quality, innovation and trust"
- Stock closers on the back cover: "The future is bright", "Join us on this journey", "Together, we can…"
- Rhetorical-question openers: "Looking for the best…?", "Ready to…?"; question marks on statements ("Who We Are?", "Why Choose Us?")
- Dot-triad taglines: "Trust • Quality • Deliverance", "Innovative · Reliable · Scalable" (humanizer §6 in slogan form). If it's the client's registered tagline, keep it and say so; don't write new ones.
- Formula heads: "Technology That Transforms Business", "Turning X into Y", "Whether you're A, B, or C", "Let's Build Something Great Together"
- The same "built for X, A over B" sentence shape opening every section
- Literal translation in bilingual work: English back-translated word for word from Tamil ("to hear the noise" for the voice). Quote scripture and statutes from a published English version; otherwise ask the client for the English.

Micro-rules (after taste-skill): pull quotes three lines at most, attributed with name and role; captions say what and where, never a fake archive label ("Plate 03"); section labels name the content ("Programmes and fees"), not a mood; "Step 1 / Phase 01" only for a real sequence.

Replace each with the specific thing the copy knows: what they make, where, since when, for whom, how many, what it costs, how to reach them.

## Automated check
`preflight.py` reports the measurable tells: `ai-contrast` (§1 not-X-but-Y), `ai-fragments` (§2 slogan rows), `ai-dashes` (§8) and `generic-copy` (§12, §16 and the brochure list). With `--copy copy.md`, hits that come from the client's own copy are skipped: they stay the client's decision. The rest (§3–7, §13–18) needs a read-through; do it once on the final text.
