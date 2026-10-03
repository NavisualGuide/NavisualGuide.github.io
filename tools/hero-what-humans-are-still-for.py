"""Hero for 'What humans are still for when AI agents can act'.

The three positions the essay sets out: the agent acts, the agent asks
permission, or you act and the AI guides. Two greyed, one lit.

Run: python tools/hero-what-humans-are-still-for.py   (geometry: hero_common.py)
"""
from hero_common import (X0, X1, SURFACE, BORDER, TEXT, MUTED, DIM, BAR,
                         ACCENT, ACCENT_SOFT, LIT_FILL, f, canvas, footer, save)

img, d = canvas("When AI agents can act")

ROWS = [
    ("The agent acts",
     "It clicks, types and buys. You find out afterwards.", False),
    ("The agent asks permission",
     "Allow? Allow? Allow?", False),
    ("You act. The AI guides.",
     "It points. You click.", True),
]

top, row_h, gap = 88, 108, 18

for i, (title, sub, lit) in enumerate(ROWS):
    y0 = top + i * (row_h + gap)
    y1 = y0 + row_h
    if lit:
        d.rounded_rectangle([X0, y0, X1, y1], 14, fill=LIT_FILL, outline=ACCENT, width=2)
        bar, tcol, scol = ACCENT, TEXT, ACCENT_SOFT
    else:
        d.rounded_rectangle([X0, y0, X1, y1], 14, fill=SURFACE, outline=BORDER, width=1)
        bar, tcol, scol = BAR, MUTED, DIM
    d.rounded_rectangle([X0 + 20, y0 + 22, X0 + 25, y1 - 22], 3, fill=bar)
    d.text((X0 + 46, y0 + 20), title, font=f(32, 680, 20), fill=tcol)
    d.text((X0 + 46, y0 + 63), sub, font=f(21, 380, 13), fill=scol)

footer(d)
save(img, "what-humans-are-still-for", "01-three-positions.png")
