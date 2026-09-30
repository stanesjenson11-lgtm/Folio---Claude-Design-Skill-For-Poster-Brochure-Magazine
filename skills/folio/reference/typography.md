# typography for print

## Size ladder (A4; scale ×0.92 for A5, ×1.1 for A3 posters' body)
| Role | Size | Leading | Notes |
|---|---|---|---|
| Furniture (folio, running head) | 6.5–7pt | 1 | same position every page |
| Caption, source, footnote | 6.5–7.5pt | 1.3 | ink-2, never lighter than 4.5:1 |
| Label / kicker | 7–8.5pt | 1.1 | caps with +0.04–0.08em tracking, only for 1–4 words |
| Body | 8.5–10pt (corporate/catalog 9–10, magazine 8.5–9.5) | 1.35–1.5 | ragged-right sans or justified serif with hyphenation |
| Lead / standfirst | 11–15pt | 1.25–1.35 | first paragraph of a section or article |
| Pull quote | 16–28pt | 1.1–1.2 | hang the opening quote mark |
| Section heading | 18–34pt | 1.0–1.1 | |
| Page title | 36–72pt | 0.9–1.0 | |
| Display (cover, openers, numerals) | 80–220pt | 0.8–0.9 | tracking −0.02 to −0.04em; floor −0.04em |

Contrast is the point: a cover or opener usually spans at least a 10× jump between the largest and smallest type. Web rules that cap headings near 96px do not apply to print.

## Measure and columns
40–70 characters per line. On A4 that means 2 columns (≈ 85mm each) or 3 (≈ 55mm) inside the margins, or a single column spanning 5–7 of 12 grid columns next to an image. Justified text needs `hyphens:auto` and a `lang` attribute, or it rivers.

## Choosing typefaces
1. Start from the three tone words in DIRECTION.md, and the register.
2. Client brand fonts win — use them even if they are common (identity preservation).
3. Otherwise, reject the reflex list: Inter, Roboto, Open Sans, Montserrat, Lato, Arial/Helvetica, Poppins, DM Sans, Space Grotesk, Plus Jakarta Sans, Outfit, Playfair Display, Fraunces, Cormorant, Lora, Newsreader, IBM Plex, Instrument Sans/Serif, Syne, Crimson, DM Serif Display/Text, Space Mono. The studio's own reflex (Anton or Bebas with Poppins or Montserrat, `library/HOUSE.md`) counts too for new clients.
   Procedure (after impeccable): name the three fonts you would reach for by reflex and drop them; look for the brand as a physical object (a site-hoarding stencil, a hymn-book title page, a valve's cast lettering, a seed-packet label) and find the face that belongs on it; if the final pick matches the first reflex, start over.
4. Pair on a contrast axis (grotesk display + serif text; condensed display + humanist text) or use one family with real weight/width contrast. Two nearly-identical sans faces is the worst option.
5. Check the family has the weights you need (a 300 and an 800 for contrast), real italics, tabular figures, and — for Indian clients — the ₹ sign and, if needed, Tamil/Devanagari coverage.

Starting points that work in print and are available from Google Fonts / Fontsource (verify fit, don't default to them):
- **Grotesk / neo-grotesk display:** Archivo (incl. Black), Schibsted Grotesk, Hanken Grotesk, Familjen Grotesk, Onest, Rethink Sans, Bricolage Grotesque
- **Condensed / poster display:** Big Shoulders Display, Barlow Condensed, Saira Extra Condensed, Antonio, Sofia Sans Extra Condensed, League Gothic
- **Wide / heavy display:** Unbounded, Dela Gothic One, Archivo Expanded (variable width), Anybody
- **Serif text:** Source Serif 4, Literata, Spectral, Gelasio, Petrona, Alegreya, Libre Caslon Text
- **Sans text:** Figtree, Red Hat Text, Public Sans, Atkinson Hyperlegible, Karla, Barlow, Commissioner
- **Tamil:** Hind Madurai, Mukta Malar, Catamaran, Noto Sans Tamil / Noto Serif Tamil, Anek Tamil (variable width)

## Aesthetic roster and font policy (the user's rule, 2026-09-29)
- **Posters:** aesthetic faces only, for every line of text.
- **Brochures:** aesthetic faces for headers, subheaders, the cover, the back cover and the contents page. Body paragraphs may use a common face (Times New Roman by default; Georgia or Arial on request).
- **Tamil** uses the functional companions listed below; it is exempt.
- Name the aesthetic font **first** in every stack and a free stand-in second: `font-family: 'The Seasons', 'Gloock', serif`. If the user has the font installed or activated (Adobe Fonts), the preview uses it; otherwise the stand-in renders and preflight says so (`stand-in-font`). The Canva file keeps the aesthetic name, and Canva Pro has these fonts.

| Aesthetic font (the user's list) | Character | Where it lives | Free stand-in folio renders with | Use for |
|---|---|---|---|---|
| The Seasons | soft high-contrast serif | Canva Pro, Adobe Fonts (My Creative Land) | Gloock | covers, headers, pastel and heritage work |
| Aesthet Nova | sharp editorial serif | Canva, Adobe Fonts (Inhouse Type) | Bodoni Moda | luxury heads, big numerals |
| Fromage | soft retro display serif | Canva, Adobe Fonts (Adam Ladd) | Young Serif | warm heads, retro pop |
| Wayfinder CF | characterful geometric sans | Canva, Adobe Fonts (Connary Fagen) | Familjen Grotesk | subheads, labels, poster info lines |
| Hagrid | wide heavy display serif | Canva, Zetafonts | Chonburi | poster words, cover titles |
| Roca | contemporary display serif | Canva, Fontfabric | Yeseva One | headers |
| Sedgwick Ave | hand-lettered marker | free (Google Fonts) | itself | stickers, tags, pop-culture accents |
| Shameless, Absolute Beauty, Gratia, Cesso, Erotiq, Wanchy, Aquavit | display and script faces | Canva / their foundries | chosen once a sample is seen | headers and accents |

Added for the magazine kits (2026-09-29): Archivo Black (wide heavy sans for sport and e-book numerals), Sedgwick Ave Display (graffiti script for street/skate styles), League Gothic and Big Shoulders for condensed news heads. Anton, Bebas Neue and Playfair Display stay banned as common; use these instead.

Free aesthetic display faces folio can fetch and use on their own (the Arc Stage family was built with them and the user loved it): Sofia Sans Extra Condensed, Big Shoulders Display, League Gothic, Gloock, Bodoni Moda, Young Serif, Italiana, Shrikhand, Pinyon Script. Preflight's `reflex-font` check flags a common face (Arial, Helvetica, Times, Poppins, Montserrat, Roboto…) wherever an aesthetic face is required.

## Poster pairs (one per variant; tested in print and in the Canva export)
| Display | Body | Tamil companion | Character |
|---|---|---|---|
| Unbounded 800 | Figtree | Catamaran 800 | wide, rounded geometric: loud, friendly |
| Gloock | Karla | Hind Madurai 600 | high-contrast serif: editorial, calm |
| Bricolage Grotesque 800 | Red Hat Text | Mukta Malar 700 | quirky grotesk: warm, hand-made |
| Sofia Sans Extra Condensed 900 | Commissioner | Anek Tamil 800 | condensed: big words, tight spaces |
Rotate them; add a pair only after checking its figures (1 vs I), Tamil companion, and weights.

## Details
- **Light type on dark pages** (after impeccable): compensate on three axes, not one: leading +0.05–0.1, tracking +0.01–0.02em, and one weight step up for body (regular → medium). Drenched and night pages need all three.
- **Paragraphs:** space between paragraphs *or* a first-line indent, never both. Use the body leading as the unit for vertical spacing so columns share a baseline rhythm.
- **Serif body** can run a slightly longer measure than sans and wants slightly more leading (after frontend-design).
- **Descender clearance** (after taste-skill): display leading of 0.8–0.9 clips italic descenders (y g j p q) and Tamil vowel signs. Italic or Tamil display lines get at least 1.05–1.1 leading and a few points of bottom padding; preflight's overflow check does not see ink clipping, so look at the PNG.
- **Tamil:** Unicode fonts only (legacy Bamini/TAM encodings break search, copy and the PDF text layer); never letter-space Tamil; set it about 1.1× the Latin size optically; hierarchy between scripts per `library/patterns/bilingual-lockup.md`.
- `font-variant-numeric: tabular-nums lining-nums` for tables, stats and prices.
- Check the digits of every face before setting numbers in it: some display serifs draw 1 like I ("Ist Floor", "64III4").
- Never let the browser synthesise bold or italic — fetch the real weights.
- Caps only for short labels, never paragraphs; add tracking to caps, remove it from big display type.
- Pull quotes and big numerals are the cheapest way to add scale contrast to a text-heavy page.
- Numbers in a sequence (01, 02) use the display face at display size — they are graphics, not labels.
