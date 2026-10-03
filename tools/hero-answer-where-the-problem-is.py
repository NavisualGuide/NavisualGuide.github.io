"""Hero for 'The answer, where the problem is'.

The illustration is Gemini's (tools/hero-src/, prompt below); this script
fits it to the site rather than redrawing it:

  * levels: Gemini's background is a blue-grey (22,26,29), not the site's
    #0a0a0b. Each channel is remapped so that grey lands on BG and white stays
    white, which darkens the greys proportionally instead of cutting them out
    (a cut-out leaves a halo on every anti-aliased edge).
  * flatten: the stretch exposes blotches in Gemini's not-quite-flat
    background, so pixels within NOISE of BG are set to BG.
  * hue: the ring came back golden (hue 22/255). Only SATURATED pixels are
    turned to the accent's hue (11), ramped by saturation, so the greys are
    untouched and the glow's soft edge goes with the ring.
  * fit: the art ran to 7% from each edge, and X's 2:1 card crop takes 10%.
    It is cropped to its content and scaled into X0..X1 (hero_common.py).

Prompt (gemini-3.1-flash-image, 21:9, 2026-10-03):
  Minimalist editorial illustration on a very dark near-black background.
  Only greys plus one warm orange accent colour. Wide composition read left to
  right: a faint progression of small greyed objects, each a little brighter
  than the last - an open book, a search bar, a photograph, a video play
  button, a robotic arm reaching for a mouse. On the right, larger and in
  focus: a laptop screen showing a simple app dialog where one button is
  circled by a glowing orange ring, and a human hand on a mouse about to click
  it. Flat vector style, calm, generous negative space. Absolutely no text,
  letters, numbers, words or logos anywhere. Keep all important content inside
  the central 80 percent of the width.

Run: python tools/hero-answer-where-the-problem-is.py
"""
import os
from PIL import Image
from hero_common import X0, X1, BG, ROOT, canvas, footer, save

SRC = os.path.join(ROOT, "tools", "hero-src", "answer-where-the-problem-is.gemini.png")
SRC_BG = (22, 26, 29)
SRC_HUE, ACCENT_HUE = 22, 11

art = Image.open(SRC).convert("RGB")

# levels
bg = tuple(int(BG[i:i + 2], 16) for i in (1, 3, 5))
lut = []
for c in range(3):
    lo, to = SRC_BG[c], bg[c]
    lut += [max(0, min(255, round(to + (v - lo) * (255 - to) / (255 - lo)))) for v in range(256)]
art = art.point(lut)

# Gemini's background is not flat: three greys a level apart, in blotches. The
# stretch above makes them visible, so anything within NOISE of BG becomes BG.
NOISE = 10
dist = Image.eval(art.convert("L"), lambda p: 255 if abs(p - sum(bg) // 3) > NOISE else 0)
art = Image.composite(art, Image.new("RGB", art.size, bg), dist)

# hue, saturated pixels only
h, s, v = art.convert("HSV").split()
shift = ACCENT_HUE - SRC_HUE

hp, sp = h.load(), s.load()
for y in range(art.height):
    for x in range(art.width):
        w = min(1.0, max(0.0, (sp[x, y] - 30) / 60))
        if w:
            hp[x, y] = (hp[x, y] + round(shift * w)) % 256
art = Image.merge("HSV", (h, s, v)).convert("RGB")

# fit
box = Image.eval(art.convert("L"), lambda p: 255 if p > 40 else 0).getbbox()
m = 24
art = art.crop((box[0] - m, box[1] - m, box[2] + m, box[3] + m))
band_top, band_bot = 78, 452
k = min((X1 - X0) / art.width, (band_bot - band_top) / art.height)
art = art.resize((round(art.width * k), round(art.height * k)), Image.LANCZOS)

img, d = canvas("Each better than the last")
img.paste(art, (X0 + (X1 - X0 - art.width) // 2, band_top + (band_bot - band_top - art.height) // 2))
footer(d)
save(img, "answer-where-the-problem-is", "01-each-better-than-the-last.png")
