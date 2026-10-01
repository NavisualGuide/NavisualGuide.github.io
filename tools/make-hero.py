"""Hero for 'What humans are still for when AI agents can act'.

Draws the argument the essay makes, which is the three positions: the agent
acts, the agent asks permission, or you act and the AI guides. Two greyed, one
lit. Site palette.

TWO CROPS DECIDE THE GEOMETRY, and the first version ignored both.

  1. The listing thumbnail (.guide-thumb img, style.css) is `aspect-ratio: 5/2`
     with `object-fit: cover; object-position: center top`. That is right for a
     screenshot, where the top of the frame is the action. On a 2:1 image it ate
     the bottom 20%, which here is the lit row -- the whole point of the picture.
     So the canvas IS 5:2. Nothing is cropped on the listing.

  2. hero_image also feeds og:image and twitter:image. X center-crops anything
     wider than 2:1 back to 2:1, which on a 5:2 canvas removes 128px from each
     side. So all content stays inside SAFE_X, and the card loses only margin.

Run: python tools/make-hero.py  (needs Pillow; uses the Windows Segoe UI
variable font, whose named instances are "Bold Text" etc., not "Bold" --
set_variation_by_name fails SILENTLY on a wrong name, so every weight renders
at 400 and the hierarchy quietly vanishes. The axes are set directly instead.)
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1280, 512          # 5:2, the thumbnail frame exactly
SAFE = 128 + 14           # survives a centred 2:1 share-card crop, with margin

BG = "#0a0a0b"
SURFACE = "#141416"
BORDER = "#26262b"
TEXT = "#f5f5f7"
MUTED = "#a1a1aa"
DIM = "#6b6b73"
ACCENT = "#ff6b35"
ACCENT_SOFT = "#ffa077"
LIT_FILL = "#1b100b"

FONT = "C:/Windows/Fonts/SegUIVar.ttf"


def f(size, weight=400, optical=None):
    """Weight 300-700, optical size 5-36."""
    ft = ImageFont.truetype(FONT, size)
    ft.set_variation_by_axes([weight, optical or min(36, max(5, size // 2))])
    return ft


img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

x0, x1 = SAFE, W - SAFE

# --- eyebrow -----------------------------------------------------------------
d.text((x0, 42), "W H E N   A I   A G E N T S   C A N   A C T",
       font=f(17, 600, 10), fill=DIM)

# --- the three positions -----------------------------------------------------
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
        d.rounded_rectangle([x0, y0, x1, y1], 14, fill=LIT_FILL, outline=ACCENT, width=2)
        bar, tcol, scol = ACCENT, TEXT, ACCENT_SOFT
    else:
        d.rounded_rectangle([x0, y0, x1, y1], 14, fill=SURFACE, outline=BORDER, width=1)
        bar, tcol, scol = "#3a3a42", MUTED, DIM
    d.rounded_rectangle([x0 + 20, y0 + 22, x0 + 25, y1 - 22], 3, fill=bar)
    d.text((x0 + 46, y0 + 20), title, font=f(32, 680, 20), fill=tcol)
    d.text((x0 + 46, y0 + 63), sub, font=f(21, 380, 13), fill=scol)

# --- footer ------------------------------------------------------------------
ft = f(19, 380, 12)
foot = "navisualguide.com"
d.text((x0, H - 48), "The AI guides, you decide.", font=ft, fill=DIM)
d.text((x1 - d.textlength(foot, font=ft), H - 48), foot, font=ft, fill=DIM)

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "images", "guides", "what-humans-are-still-for")
os.makedirs(OUT, exist_ok=True)
p = os.path.join(OUT, "01-three-positions.png")
img.save(p, optimize=True)
print(f"{p}  {img.size}  {os.path.getsize(p)//1024} KB")
