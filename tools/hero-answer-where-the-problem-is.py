"""Hero for 'The answer, where the problem is'.

The illustration is Gemini's (tools/hero-src/, prompts below); this script
fits it to the site rather than redrawing it.

  * levels: Gemini draws on a blue-grey, not the site's #0a0a0b. Each channel
    is remapped so that grey lands on BG and white stays white, which darkens
    the greys proportionally instead of cutting them out (a cut-out leaves a
    halo on every anti-aliased edge). The source grey is MEASURED -- an edit
    pass does not return the same background as the image it was given.
  * flatten: the stretch exposes blotches in Gemini's not-quite-flat
    background, so pixels within NOISE of BG are set to BG.
  * hue: the ring comes back golden. Only SATURATED pixels are turned to the
    accent's hue, ramped by saturation, so the greys are untouched and the
    glow's soft edge goes with the ring. Source hue measured, as above.
  * fit: the laptop's right edge lands on X1, so X's 2:1 card crop keeps the
    whole laptop, hand and mouse. The arm enters from the right edge, so the
    sleeve's last column is repeated out to the canvas edge rather than
    leaving it cut off in mid-air.

Generated with gemini-3.1-flash-image at 21:9 on 2026-10-03, in three passes:

  1. Minimalist editorial illustration on a very dark near-black background.
     Only greys plus one warm orange accent colour. Wide composition read left
     to right: a faint progression of small greyed objects, each a little
     brighter than the last - an open book, a search bar, a photograph, a
     video play button, a robotic arm reaching for a mouse. On the right,
     larger and in focus: a laptop screen showing a simple app dialog where one
     button is circled by a glowing orange ring, and a human hand on a mouse
     about to click it. Flat vector style, calm, generous negative space.
     Absolutely no text, letters, numbers, words or logos anywhere. Keep all
     important content inside the central 80 percent of the width.

     -> drew a hand holding a mouse AND poking the screen with a finger.

  2. (--edit 1) Remove the hand touching the screen; put a mouse to the right
     of the laptop with a hand on it, and a white pointer arrow on the ringed
     button. Nothing touches the screen. Keep everything else the same.

     -> right idea; the hand was oversized and ran off the bottom.

  3. (--edit 2) Hand and mouse about half the size, from the side, resting on
     the laptop's surface line, entirely inside the image. Keep everything
     else the same.

Run: python tools/hero-answer-where-the-problem-is.py
"""
import os
from collections import Counter
from PIL import Image
from hero_common import W, X0, X1, BG, ROOT, canvas, footer, save

SRC = os.path.join(ROOT, "tools", "hero-src", "answer-where-the-problem-is.gemini.png")
ACCENT_HUE = 11          # #ff6b35 on Pillow's 0-255 hue scale
NOISE = 10
LAPTOP_BELOW = 500    # source rows above the hand and sleeve: the laptop's extent

art = Image.open(SRC).convert("RGB")
src_bg = Counter(art.get_flattened_data()).most_common(1)[0][0]
bg = tuple(int(BG[i:i + 2], 16) for i in (1, 3, 5))

# levels
lut = []
for c in range(3):
    lo, to = src_bg[c], bg[c]
    lut += [max(0, min(255, round(to + (v - lo) * (255 - to) / (255 - lo)))) for v in range(256)]
art = art.point(lut)

# flatten
dist = Image.eval(art.convert("L"), lambda p: 255 if abs(p - sum(bg) // 3) > NOISE else 0)
art = Image.composite(art, Image.new("RGB", art.size, bg), dist)

# hue, saturated pixels only
h, s, v = art.convert("HSV").split()
sat = sorted(hh for hh, ss, vv in zip(h.get_flattened_data(), s.get_flattened_data(),
                                       v.get_flattened_data()) if ss > 120 and vv > 120)
shift = ACCENT_HUE - sat[len(sat) // 2]
hp, sp = h.load(), s.load()
for y in range(art.height):
    for x in range(art.width):
        w = min(1.0, max(0.0, (sp[x, y] - 30) / 60))
        if w:
            hp[x, y] = (hp[x, y] + round(shift * w)) % 256
art = Image.merge("HSV", (h, s, v)).convert("RGB")
print(f"source bg {src_bg}, hue shift {shift}")

# fit. The laptop decides the scale: its right edge lands on X1, so X's card
# crop keeps all of it. The sleeve beyond it is a flat horizontal band, so its
# last column is repeated out to the canvas edge -- the arm still enters from
# off-frame instead of stopping in mid-air. The crop is clamped to the image:
# past the edge Pillow pads with pure black, which showed as a stripe.
m = 24
lum = Image.eval(art.convert("L"), lambda p: 255 if p > 40 else 0)
box = lum.getbbox()
laptop_right = lum.crop((0, 0, art.width, LAPTOP_BELOW)).getbbox()[2]
left = max(0, box[0] - m)
# EDGE: Gemini's outermost rows are lighter than its background and survive
# the flatten as a dashed line, so they are never part of the crop.
EDGE = 6
art = art.crop((left, max(EDGE, box[1] - m), art.width, min(art.height - EDGE, box[3] + m)))
band_top, band_bot = 78, 452
k = min((X1 - X0) / (laptop_right + m - left), (band_bot - band_top) / art.height)
art = art.resize((round(art.width * k), round(art.height * k)), Image.LANCZOS)

img, d = canvas("Each better than the last")
y = band_top + (band_bot - band_top - art.height) // 2
img.paste(art, (X0, y))
edge = art.crop((art.width - 1, 0, art.width, art.height))
for x in range(X0 + art.width, W):
    img.paste(edge, (x, y))
print(f"scale {k:.3f}, laptop ends at x={X0 + round((laptop_right - left) * k)} (safe to {X1})")
footer(d)
save(img, "answer-where-the-problem-is", "01-each-better-than-the-last.png")
