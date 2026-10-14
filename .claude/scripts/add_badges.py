"""Stamp round badges on a day's thumbnail (still or animated WebP) or any image, in its top corners.

Usage: python add_badges.py <in.webp|png> <out.webp|png> <badge> [<badge> ...]
The badges scale with the image width (52 px on a 240 px thumbnail, at most 120 px).
Badges: noviz (top left, a crossed-out eye: no visualization in Blender),
        ai (top right, "AI": the day has a node group or image made with AI).
Run it once on a freshly made thumbnail (make_thumbnail.py), not on one that already has badges.
Needs: pip install pillow
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont, ImageSequence

src, dst, badges = sys.argv[1], sys.argv[2], sys.argv[3:]
FONT = os.path.join(os.path.dirname(__file__), "..", "..", "fonts", "IBMPlexMono-Regular.ttf")
SS = 8  # supersampling factor
source = Image.open(src)
SIZE = min(round(source.width * 52 / 240), 120)  # diameter: 52 px on a thumbnail, at most 120
MARGIN = round(SIZE * 8 / 52)
U = SS * SIZE / 52  # one thumbnail pixel of line width, supersampled
FILL, LIGHT = (20, 22, 34, 230), (230, 232, 240, 255)
RING = {"noviz": (240, 160, 70, 255), "ai": (170, 140, 255, 255)}


def badge(kind):
    """One badge as an RGBA image of SIZE x SIZE."""
    s = SIZE * SS
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    ring = RING[kind]
    d.ellipse([0, 0, s - 1, s - 1], fill=FILL, outline=ring, width=round(4 * U))
    c = s / 2
    if kind == "noviz":
        w, h = s * 0.31, s * 0.17  # eye: an almond outline and an iris, crossed by a slash
        xs = [c - w + 2 * w * i / 40 for i in range(41)]
        top = [(x, c - h * (1 - ((x - c) / w) ** 2)) for x in xs]
        bottom = [(x, c + h * (1 - ((x - c) / w) ** 2)) for x in reversed(xs)]
        d.polygon(top + bottom, outline=LIGHT, width=round(3 * U))
        r = s * 0.11
        d.ellipse([c - r, c - r, c + r, c + r], fill=LIGHT)
        k = s * 0.26
        d.line([c - k, c + k, c + k, c - k], fill=FILL, width=round(9 * U))
        d.line([c - k, c + k, c + k, c - k], fill=ring, width=round(4 * U))
    elif kind == "ai":
        font = ImageFont.truetype(FONT, int(s * 0.42))
        d.text((c, c), "AI", font=font, fill=LIGHT, anchor="mm", stroke_width=round(U), stroke_fill=LIGHT)
    else:
        sys.exit(f"unknown badge {kind!r} (noviz, ai)")
    return img.resize((SIZE, SIZE), Image.LANCZOS)


CORNER = {"noviz": "left", "ai": "right"}
stamps = [(badge(b), CORNER[b]) for b in badges]
frames, durations = [], []
for frame in ImageSequence.Iterator(source):
    f = frame.convert("RGBA")
    for img, side in stamps:
        x = MARGIN if side == "left" else f.width - MARGIN - SIZE
        f.alpha_composite(img, (x, MARGIN))
    frames.append(f.convert("RGB"))
    durations.append(frame.info.get("duration", 50))
if len(frames) == 1:
    frames[0].save(dst, quality=90)
else:
    frames[0].save(dst, save_all=True, append_images=frames[1:], duration=durations, loop=0, quality=85, method=6)
print(f"{dst}: {len(frames)} frame(s), badges {', '.join(badges)}")
