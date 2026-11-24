---
id: poster-youth-post
name: Youth Posts (letter)
family: posters
best_for: theme-of-the-month posts, youth conventions, camps and conferences, flyers that also print on Letter or A4; feed posts (crop to 4:5); bold type with a twist; a black-and-white worship photo for t02
size: letter ratio (73.6 x 95.2 mm -> 1081 x 1398 px; scale for US Letter / A4 print)
pages: 2
render: --png-only --dpi 373
fonts: League Gothic:400,wdth75-100; Antonio:700; Herr Von Muellerhoff:400; Plus Jakarta Sans:500,700,800; Montserrat:400; Chonburi:400
theme: brand #F47A2E; brand-2 #74A3BC; brand-3 #C76A66; accent #F5D90A; accent-2 #E4572E
---
# Youth Posts (letter)

**Looks like:** two letter-ratio church youth posts: (t01) a charcoal ground with leaf shadows, grain and glowing yellow lightning bolts, thin curve lines carrying the month's scripture, a signature-script line, condensed WELCOME TO and a rainbow month word (blue -> mauve -> red -> orange) with a number swapped in (OCT10BER) and its last letters leaning out in perspective; (t02) a black-and-white worship photo washed with a red-orange film light leak, dust and scratches, a quoted verse in a wide wedge-serif, huge outline serif words with a white glow, a solid word riding an S-wave between them (Stranger Things style), the year, a centred details block, partner logos and a cost box. Rebuilt from 1:1 replicas of two reference posters (`reference/posters.md` §6 Youth); grounds are generated.

## Templates
| id | Name | fits | Looks like |
|---|---|---|---|
| t01 | Rainbow month | theme of the month, new series, new-month welcome · treatment 16 (rainbow perspective month word) · photo: none · text: light | logo and name at the top, script line, WELCOME TO, a rainbow month word, a social row, scripture along curve lines in three corners |
| t02 | Film outline | youth convention, camp, conference, retreat · treatment 17 (outline serif stack + S-wave word) · photo: full-bleed black and white · text: medium | quoted verse at the top, YTH / wave word / CAMP, year, dates, venue, city, web, handle, hashtag, two logos and a cost box |

**Image slots:** t02: one black-and-white worship photo (`imagery.py grade --treatment bw`), hands or a crowd on one side so the type sits on the darker half. Logos: logo placeholders (white versions read best).

**Theme colours:** the rainbow runs from brand-2 (cool) through brand-3 to brand (warm); accent is the lightning yellow; accent-2 the film leak. The month word keeps four to six stops; never put the rainbow on body text.

**Filling it:**
- t01: the month word stays one line of 6-9 condensed letters; split it into a run plus the last two or three letters, each leaning a little more (skewX 5 / 9 / 14 deg, skewY 3-4 deg) so the word fans out like the reference. Scripture is quoted exactly from the translation the church reads; update all three blocks.
- t02: the outline words are three to four letters; keep the wave word 9-14 letters (`textLength` on the path stretches it). Bake the glow before export: `imagery.py shadow poster.html --select .ol --dx 0 --dy 0 --blur .6 --color "#FFFFFF" --out assets/glow.png`, place it under the outline words, delete the CSS filter.

**Deviations from the references:** free stand-ins: Antonio Bold for the month word (the original's letters touch: keep its tight tracking), Chonburi for ITC Benguiat, Herr Von Muellerhoff for the signature script, Plus Jakarta Sans for the logo type.

**Using it:** `/folio:poster-youth` (it offers both kits) or `kit.py new poster-youth-post <project> --pages t01,t02 --name poster`, then `render.py poster.html --png-only --dpi 373`.
