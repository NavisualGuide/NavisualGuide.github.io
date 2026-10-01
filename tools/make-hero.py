"""Hero for 'What humans are still for when AI agents can act'.

Draws the argument the essay makes, which is the three positions: the agent
acts, the agent asks permission, or you act and the AI guides. Two greyed, one
lit. Site palette, 1280x640 to match social-preview.png.

Run: python tools/make-hero.py  (needs Pillow; uses the Windows Segoe UI
variable font, whose named instances are "Bold Text" etc., not "Bold" --
set_variation_by_name fails SILENTLY on a wrong name, so the axes are set
directly instead.)
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1280, 640
BG = "#0a0a0b"
SURFACE = "#141416"
BORDER = "#26262b"
TEXT = "#f5f5f7"
MUTED = "#a1a1aa"
DIM = "#6b6b73"
ACCENT = "#ff6b35"

FONT = r"C:\Windows\Fonts\SegUIVar.ttf"


def f(size, weight=400, optical=None):
    """Weight 300-700, optical size 5-36. The named instances are "Bold Text"
    etc., not "Bold", so setting them by name fails silently -- axes are set
    directly instead."""
    ft = ImageFont.truetype(FONT, size)
    ft.set_variation_by_axes([weight, optical if optical else min(36, max(5, size // 2))])
    return ft


img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

# --- eyebrow -----------------------------------------------------------------
eyebrow = "W H E N   A I   A G E N T S   C A N   A C T"
d.text((80, 62), eyebrow, font=f(19, 600, 10), fill=DIM)

# --- the three positions -----------------------------------------------------
ROWS = [
    ("The agent acts",
     "It clicks, types and buys. You find out afterwards.", False),
    ("The agent asks permission",
     "Allow? Allow? Allow?", False),
    ("You act. The AI guides.",
     "It points. You click.", True),
]

x0, x1 = 80, W - 80
top, row_h, gap = 116, 128, 26

for i, (title, sub, lit) in enumerate(ROWS):
    y0 = top + i * (row_h + gap)
    y1 = y0 + row_h
    if lit:
        d.rounded_rectangle([x0, y0, x1, y1], 16, fill="#1b100b", outline=ACCENT, width=2)
        bar = ACCENT
        tcol, scol = TEXT, "#ffa077"
    else:
        d.rounded_rectangle([x0, y0, x1, y1], 16, fill=SURFACE, outline=BORDER, width=1)
        bar = "#3a3a42"
        tcol, scol = MUTED, DIM
    # left accent bar
    d.rounded_rectangle([x0 + 22, y0 + 28, x0 + 27, y1 - 28], 3, fill=bar)
    d.text((x0 + 52, y0 + 30), title, font=f(35, 680, 20), fill=tcol)
    d.text((x0 + 52, y0 + 78), sub, font=f(24, 380, 14), fill=scol)

# --- footer ------------------------------------------------------------------
foot = "navisualguide.com"
ft = f(21, 380, 12)
d.text((x1 - d.textlength(foot, font=ft), H - 56), foot, font=ft, fill=DIM)
d.text((x0, H - 56), "The AI guides, you decide.", font=f(21, 380, 12), fill=DIM)

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "images", "guides", "what-humans-are-still-for")
os.makedirs(OUT, exist_ok=True)
p = os.path.join(OUT, "01-three-positions.png")
img.save(p, optimize=True)
print(f"{p}  {img.size}  {os.path.getsize(p)//1024} KB")
