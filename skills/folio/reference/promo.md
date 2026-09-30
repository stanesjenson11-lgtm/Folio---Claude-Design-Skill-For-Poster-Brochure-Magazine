# promo — launch assets for a finished book (after latent-spaces/brag)

Offer this after delivery; run it when the user wants to share or announce the brochure.

```bash
python <skill>/scripts/promo.py out --bg "<tint hex>" --format square     # or vertical / landscape
```
Produces `out/promo/`: presentation mockups of the cover and every spread, `social-square.png`, `social-story.png`, `linkedin.png`, `poster.jpg`, and `reel.mp4` (cover hold, then spreads with a gentle push-in; transitions dip through the ground colour instead of cross-fading two busy spreads; the first frame is the poster so every platform's thumbnail shows it).

## Creative laws (adapted from brag)
- **Short.** Reels 12–20 seconds. Pages are read in the PDF, not the reel.
- **Show the thing.** Real pages only — no invented claims, numbers or testimonials in captions.
- **Every frame postable.** Before handing over, look at the poster frame and two mid-reel stills (extract with `ffmpeg -ss 5 -i reel.mp4 -frames:v 1 f5.png`); fix anything cropped, muddy or illegible.
- **Specific share copy.** Write `out/promo/share-copy.txt`: 1–3 sentences from the book's own content, postable as-is. Name the organisation and one concrete highlight ("126 schools, 41,280 visitors, one reopened dome — our 2025–26 report is out."). No "excited to share"; run it through `reference/copy.md` like every word folio writes. Offer a Tamil or other-language version when the audience is local.
- **Ground colour** = the brand tint or a neutral grey; never a new colour.

Music is off by default (licensing). If the user supplies a track they own: `ffmpeg -i reel.mp4 -i track.mp3 -shortest -c:v copy -c:a aac reel-music.mp4`.
