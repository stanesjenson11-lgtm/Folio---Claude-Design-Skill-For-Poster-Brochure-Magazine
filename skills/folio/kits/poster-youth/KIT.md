---
id: poster-youth
name: Youth Story Posters
family: posters
best_for: youth nights, connect groups, youth services, young-adult takeovers, worship nights; Instagram / WhatsApp stories (9:16); loud, warm, street-meets-church; a speaker photo is optional (t03 only)
size: 9:16 story (73.6 x 130.8 mm → 1080 x 1920 px)
pages: 4
render: --png-only --dpi 373
fonts: Anton:400; Fruktur:400; JetBrains Mono:400; Hanken Grotesk:400,500,700,800; Inter:400,500,700,800; League Gothic:400,wdth75-100; Montserrat:500,600,700,800; Delicious Handrawn:400; Alfa Slab One:400; Work Sans:400,600; Herr Von Muellerhoff:400; Just Another Hand:400; Antonio:700
theme: brand #F47A2E; brand-2 #FB7A2F; brand-3 #D9682B; brand-4 #EB5A49; brand-5 #F39C66; brand-6 #EC8A2E; brand-7 #F07A2A; accent #B12A1B; accent-2 #CA4529; accent-3 #C4462A; accent-4 #DE7642; accent-5 #E7742F; accent-6 #F48E48; accent-7 #BE3622; brand-8 #CE72A8; brand-9 #FCAEBF; brand-10 #DDA1D3; brand-11 #B37AA9
---
# Youth Story Posters

**Looks like:** three loud 9:16 story posters for church youth: (t01) grunge charcoal with caution-tape strips, a coral-to-peach condensed headline where one letter per line is swapped for a blackletter lowercase, a tilted time block with a hand-drawn arrow and a dry-brush scribble; (t02) a soft espresso-and-orange glow with film grain and pixel-stripe blocks, a red condensed headline on a white die-cut sticker tilted −7°, white label boxes; (t03) a dark twill ground with a dashed route line, a huge ultra-condensed white stack with a die-cut AND, an orange marker word, marker notes with "+" and a black-and-white person cut at the edge. Rebuilt from 1:1 replicas of three reference posters (`reference/posters.md` §6, Youth); grounds are generated, never copied.

## Templates
| id | Name | fits | Looks like |
|---|---|---|---|
| t01 | Tape & blackletter | youth night, connect group, weekly series · treatment 11 (blackletter letter swap) · photo: none · text: medium | caution tapes top and bottom carrying the series name, a mono eyebrow, a two-line gradient headline, a ">WEEKDAY / DD MON / 07:00 PM" block tilted 5.75°, venue line with pin and brush underline, handle at the foot, round badge top right |
| t02 | Sticker on glow | youth service, worship night, theme night · treatment 12 (die-cut sticker) · photo: none · text: medium | org lines top left, badge, a WED / [22] / JUL '26 date stack, a two-line sticker headline, two white label boxes (time, place) with the details under them, pixel-stripe blocks around the headline |
| t03 | Takeover | youth & young-adult service, takeover Sunday, camp night · treatment 13 (stacked condensed + nested sticker word + marker word) · photo: cut-out person at the edge · text: medium | "+ YOU'RE INVITED" and "+ BRING A FRIEND" marker notes, YOUTH / AND / YOUNG ADULT, an orange marker word, one date-and-times line, pin, address and credits, a dashed route crossing behind the headline |
| t04 | Layered stack (pink) | connect group, mission or outreach night, youth service · treatment 15 (two-tone back word + front word + small word on tape) · photo: full-bleed, any (toned plum) · text: heavy | a plum-toned stage photo with grunge scratches over everything, CONNECT GROUP eyebrow under a round badge, a big mauve back word with a signature-script echo, a ticket sticker, a blush front word crossing it, an arrow into a red tape label, a brush underline, heart and cross doodles, a tilted hand note with underlines, a tall 13 / JUN / 2026 date block with time and venue |

**Image slots:** t03 only: the speaker or youth leader, `imagery.py cutout --person` then `imagery.py grade --treatment bw`, cropped by the right edge from the waist down. Logos: drop the church logo on the badge (t01, t02); the badge ring text is a vector SVG (`imagery.py device --kind badge --text "…"`).

**Theme colours:** brand #F47A2E (orange) with its tape, marker, coral and peach variants; accent #B12A1B (red) with the pixel-block and glow variants. `kit.py new --brand --accent` moves every variant to the client's hue; keep the brand warm and saturated, and the grounds dark.

**Filling it (rules learned from the references):**
- Headline words stay short: one or two words per line, 4–8 letters. t01: swap one letter per line for its blackletter lowercase (`<span class="bl">u</span>`); never the first letter of both lines. t02: the white twin (`data-twin`) carries the same words as its front copy; re-run `imagery.py shadow <file>.html --select .stk-shadow --out assets/sticker-shadow.png`, place it under `.stk-shadow` and delete the CSS filter before export (Canva drops CSS filters).
- Facts are exact: weekday checked against the date; times as the client writes them ("07:00 PM" in t01's style, "6.30 PM" in t02's, "11AM + 4:30PM" in t03's).
- Tapes repeat the series short name and the group name (t01). Shift the text inside each tape so a name, not a dash, sits under the centre of the page.
- Hand-lettered notes (t03) use a dotted lowercase i inside caps ("iNVITED", "BRiNG", "FRiEND"), as the reference does.

**Deviations from the references:** fonts are the closest free faces in Canva's library (originals were commercial): Anton + Fruktur for the gradient headline, League Gothic (variable width; Canva shows it at full width) for sticker and stack, Delicious Handrawn for the marker notes, Alfa Slab One for AND. Grounds are rebuilt as vector fleck grids, CSS gradient meshes and grain recipes instead of the references' photographic textures.

**Using it:** `/folio:poster-youth` (or `/folio:poster` with Topic = youth). `kit.py new poster-youth <project> --pages t01,t02,t03 [--brand #hex --accent #hex] --name poster`, fill every `data-kit-sample`, then `render.py poster.html --png-only --dpi 373` and preflight.
