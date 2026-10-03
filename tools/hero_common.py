"""Shared canvas, palette and type for the generated essay heroes.

TWO CROPS DECIDE THE GEOMETRY.

  1. The listing thumbnail (.guide-thumb img, style.css) is `aspect-ratio: 5/2`
     with `object-fit: cover; object-position: center top`. Right for a
     screenshot, wrong for a drawing: a 2:1 hero lost its bottom 20%. So the
     canvas IS 5:2 and nothing is cropped on the listing.

  2. hero_image also feeds og:image and twitter:image. X centre-crops anything
     wider than 2:1 back to 2:1, removing 128px from each side of a 5:2 canvas.
     So content stays between X0 and X1.

Type is the Windows Segoe UI variable font. Its named instances are "Bold Text"
etc., not "Bold", and set_variation_by_name fails SILENTLY on a wrong name, so
every weight renders at 400 and the hierarchy quietly vanishes. Axes are set
directly instead.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1280, 512
X0, X1 = 128 + 14, 1280 - 128 - 14

BG = "#0a0a0b"
SURFACE = "#141416"
BORDER = "#26262b"
TEXT = "#f5f5f7"
MUTED = "#a1a1aa"
DIM = "#6b6b73"
BAR = "#3a3a42"
ACCENT = "#ff6b35"
ACCENT_SOFT = "#ffa077"
LIT_FILL = "#1b100b"

FONT = "C:/Windows/Fonts/SegUIVar.ttf"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def f(size, weight=400, optical=None):
    """Weight 300-700, optical size 5-36."""
    ft = ImageFont.truetype(FONT, size)
    ft.set_variation_by_axes([weight, optical or min(36, max(5, size // 2))])
    return ft


def canvas(eyebrow):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.text((X0, 42), "   ".join(" ".join(w) for w in eyebrow.upper().split()),
           font=f(17, 600, 10), fill=DIM)
    return img, d


def footer(d):
    ft = f(19, 380, 12)
    foot = "navisualguide.com"
    d.text((X0, H - 48), "The AI guides, you decide.", font=ft, fill=DIM)
    d.text((X1 - d.textlength(foot, font=ft), H - 48), foot, font=ft, fill=DIM)


def save(img, slug, name):
    out = os.path.join(ROOT, "images", "guides", slug)
    os.makedirs(out, exist_ok=True)
    p = os.path.join(out, name)
    img.save(p, optimize=True)
    print(f"{p}  {img.size}  {os.path.getsize(p)//1024} KB")
    return p
