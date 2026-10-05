"""Make a day's thumbnail for the Days grid in the root README: the animation with a "Day 01" label below.

Usage: python make_thumbnail.py <day> <out.webp> [video.mp4 | image.png]
With an image (a day without animation, such as a node capture) it makes a still thumbnail:
the editor background becomes the usual dark blue and the image is centered.
Without either it makes a static placeholder for a day that is not finished yet.
Needs: pip install av pillow
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

day, dst = int(sys.argv[1]), sys.argv[2]
src = sys.argv[3] if len(sys.argv) > 3 else None

WIDTH, HEIGHT, BAND, FPS = 240, 320, 40, 20
FONT = os.path.join(os.path.dirname(__file__), "..", "..", "fonts", "IBMPlexMono-Regular.ttf")
font = ImageFont.truetype(FONT, 20)
label = f"Day {day:02d}"


def with_label(frame, background, color):
    """Add a band with the label under a frame."""
    out = Image.new("RGB", (WIDTH, HEIGHT + BAND), background)
    out.paste(frame, (0, 0))
    ImageDraw.Draw(out).text((WIDTH / 2, HEIGHT + BAND / 2), label, font=font, fill=color, anchor="mm")
    return out


if src is None:  # placeholder: same size as a real thumbnail, so every row has the same height
    background = (28, 29, 38)
    with_label(Image.new("RGB", (WIDTH, HEIGHT), background), background, (110, 112, 125)).save(dst, quality=90)
    sys.exit()

if src.lower().endswith((".png", ".jpg")):
    background = (35, 37, 57)  # same dark blue as the day 1 render
    image = Image.open(src).convert("RGB")
    editor = image.getpixel((2, 2))
    pixels = image.load()
    for y in range(image.height):
        for x in range(image.width):
            if sum(abs(a - b) for a, b in zip(pixels[x, y], editor)) <= 6:
                pixels[x, y] = background
    margin = 16
    scale = min((WIDTH - 2 * margin) / image.width, (HEIGHT - 2 * margin) / image.height)
    image = image.resize((round(image.width * scale), round(image.height * scale)), Image.LANCZOS)
    box = Image.new("RGB", (WIDTH, HEIGHT), background)
    box.paste(image, ((WIDTH - image.width) // 2, (HEIGHT - image.height) // 2))
    with_label(box, background, (220, 222, 230)).save(dst, quality=90)
    sys.exit()

import av  # noqa: E402  (only needed for real thumbnails)

container = av.open(src)
stream = container.streams.video[0]
src_fps = float(stream.average_rate)
total = stream.frames or sum(1 for _ in av.open(src).decode(video=0))
wanted = []
while round(len(wanted) * src_fps / FPS) < total:
    wanted.append(round(len(wanted) * src_fps / FPS))
wanted_set = set(wanted)
scale = min(WIDTH / stream.width, HEIGHT / stream.height)  # fit any aspect ratio into the same box
size = (round(stream.width * scale), round(stream.height * scale))
frames = {
    i: f.to_image().resize(size, Image.LANCZOS)
    for i, f in enumerate(container.decode(video=0))
    if i in wanted_set
}
background = frames[wanted[0]].getpixel((2, 2))  # the box and band take the render's own background
boxed = []
for i in wanted:
    box = Image.new("RGB", (WIDTH, HEIGHT), background)
    box.paste(frames[i], ((WIDTH - size[0]) // 2, (HEIGHT - size[1]) // 2))
    boxed.append(box)
frames = [with_label(f, background, (220, 222, 230)) for f in boxed]
delays = [10 * (round((k + 1) * 100 / FPS) - round(k * 100 / FPS)) for k in range(len(frames))]
frames[0].save(dst, save_all=True, append_images=frames[1:], duration=delays, loop=0, quality=85, method=6)
print(f"{dst}: {len(frames)} frames")
