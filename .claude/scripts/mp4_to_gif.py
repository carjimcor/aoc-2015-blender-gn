"""Convert a video to a small looping animation for a day README.

Usage: python mp4_to_gif.py input.mp4 output.gif|output.webp [width=480] [fps=20] [webp_quality=90] [slow]
Needs: pip install av pillow

slow plays part of the clip at another speed: "30-570x0.5" plays source frames 30 to 570 at
half speed (the rest at normal speed), so the animation gets longer.

GIF has 256 colours, fine for flat graphics. For renders with many colours or shading,
write .webp instead: full colour, usually smaller, and GitHub shows it like a GIF.

Any source and target frame rate works (for example 60 or 24 fps in, 20 or 24 fps out).
GIF delays are whole centiseconds, so they are spread to keep the total duration exact.
"""
import sys

import av
from PIL import Image

src, dst = sys.argv[1], sys.argv[2]
width = int(sys.argv[3]) if len(sys.argv) > 3 else 480
fps = float(sys.argv[4]) if len(sys.argv) > 4 else 20
quality = int(sys.argv[5]) if len(sys.argv) > 5 else 90  # lower it for busy clips, such as scrolling text
slow = sys.argv[6] if len(sys.argv) > 6 else None

container = av.open(src)
stream = container.streams.video[0]
src_fps = float(stream.average_rate)
height = round(stream.height * width / stream.width)

# Speed of each part of the source, as (first frame, end frame, speed).
total = stream.frames or sum(1 for _ in av.open(src).decode(video=0))
parts = [(0, total, 1.0)]
if slow:
    span, speed = slow.split("x")
    a, b = (int(v) for v in span.split("-"))
    parts = [(0, a, 1.0), (a, b, float(speed)), (b, total, 1.0)]


def source_frame(t):
    """The source frame shown at output time t (seconds), or None after the end."""
    for a, b, speed in parts:
        length = (b - a) / src_fps / speed
        if t < length:
            return a + round(t * speed * src_fps)
        t -= length
    return None


# Output frame k shows the source frame nearest to time k / fps.
wanted = []
k = 0
while (i := source_frame(k / fps)) is not None and i < total:
    wanted.append(i)
    k += 1

wanted_set = set(wanted)
frames = {
    i: f.to_image().resize((width, height), Image.LANCZOS)
    for i, f in enumerate(container.decode(video=0))
    if i in wanted_set
}
frames = [frames[i] for i in wanted]

# Delay of frame k = difference of rounded cumulative times, in milliseconds.
delays = [10 * (round((k + 1) * 100 / fps) - round(k * 100 / fps)) for k in range(len(frames))]

if dst.lower().endswith(".webp"):
    frames[0].save(dst, save_all=True, append_images=frames[1:], duration=delays, loop=0, quality=quality, method=6)
    print(f"{dst}: {len(frames)} frames, {width}x{height}, {sum(delays) / 1000:.2f} s")
    sys.exit()

# One palette for the whole clip avoids flicker; no dithering keeps flat colors clean.
sample = frames[::6]
mosaic = Image.new("RGB", (width, height * len(sample)))
for n, frame in enumerate(sample):
    mosaic.paste(frame, (0, n * height))
palette = mosaic.quantize(256, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
frames = [f.quantize(palette=palette, dither=Image.Dither.NONE) for f in frames]

frames[0].save(dst, save_all=True, append_images=frames[1:], duration=delays, loop=0, disposal=1)
print(f"{dst}: {len(frames)} frames, {width}x{height}, {sum(delays) / 1000:.2f} s")
