"""Join overlapping screenshots of one node tree into a single image.

Usage:
  python stitch_images.py out.png img1.png img2.png ...   find how the images overlap
  python stitch_images.py out.png layout.json             use offsets from capture_node_tree.py
  python stitch_images.py --dir capture_dir media_dir     every capture_dir/<slug>/layout.json -> media_dir/<slug>.png
Needs: pip install pillow numpy

Images must share the same zoom and overlap their neighbours (any order, any direction).
"""
import json
import os
import sys

import numpy as np
from PIL import Image


def gray(img):
    return np.asarray(img.convert("L"), dtype=np.float32)


def compose(placed):
    """placed: [(image, x, y)] -> (canvas image, coverage mask, origin shift)."""
    x0, y0 = min(x for _, x, _ in placed), min(y for _, _, y in placed)
    w = max(x + im.width for im, x, _ in placed) - x0
    h = max(y + im.height for im, _, y in placed) - y0
    canvas = Image.new("RGB", (w, h), placed[0][0].getpixel((2, 2)))
    mask = np.zeros((h, w), bool)
    for im, x, y in placed:
        canvas.paste(im, (x - x0, y - y0))
        mask[y - y0:y - y0 + im.height, x - x0:x - x0 + im.width] = True
    return canvas, mask


def locate(canvas, mask, img, tries=8):
    """Find where img sits on the canvas: phase correlation for candidates, exact diff to confirm."""
    a, b = gray(canvas), gray(img)
    a = np.where(mask, a - a[mask].mean(), 0)
    b = b - b.mean()
    shape = (a.shape[0] + b.shape[0], a.shape[1] + b.shape[1])
    cross = np.fft.rfft2(a, shape) * np.conj(np.fft.rfft2(b, shape))
    corr = np.fft.irfft2(cross / (np.abs(cross) + 1e-6), shape)
    background = canvas.getpixel((2, 2))
    a_rgb = np.asarray(canvas, dtype=np.int16)
    b_rgb = np.asarray(img, dtype=np.int16)
    best = None
    for idx in np.argsort(corr, axis=None)[::-1][:tries]:
        y, x = np.unravel_index(idx, shape)
        y = y - shape[0] if y >= a.shape[0] else y
        x = x - shape[1] if x >= a.shape[1] else x
        ya, yb = max(y, 0), max(-y, 0)
        xa, xb = max(x, 0), max(-x, 0)
        h = min(a.shape[0] - ya, b.shape[0] - yb)
        w = min(a.shape[1] - xa, b.shape[1] - xb)
        if h < 20 or w < 20:
            continue
        # Compare away from the borders, where editor scrollbars and arrows can differ.
        t = max(0, min(40, (min(h, w) - 40) // 2))
        both = mask[ya + t:ya + h - t, xa + t:xa + w - t]
        pa = a_rgb[ya + t:ya + h - t, xa + t:xa + w - t]
        pb = b_rgb[yb + t:yb + h - t, xb + t:xb + w - t]
        content = (np.abs(pb - np.array(background)).sum(axis=2) > 12) & both
        if content.sum() < 200:  # need a real overlap with something in it
            continue
        diff = np.abs(pa - pb)[content].mean()
        if best is None or diff < best[0]:
            best = (diff, x, y)
    return best if best and best[0] < 2 else None


def stitch(out, sources):
    if len(sources) == 1 and sources[0].endswith(".json"):
        base = os.path.dirname(sources[0])
        layout = json.load(open(sources[0]))
        crop = layout["crop"]  # drop the editor's scrollbars and arrows at every tile edge
        box = layout["box"]
        placed = []
        for t in layout["tiles"]:
            im = Image.open(os.path.join(base, t["file"])).convert("RGB")
            placed.append((im.crop((crop, crop, im.width - crop, im.height - crop)), t["x"] + crop, t["y"] + crop))
    else:
        box = None
        images = [Image.open(p).convert("RGB") for p in sources]
        placed, rest = [(images[0], 0, 0)], images[1:]
        while rest:
            canvas, mask = compose(placed)
            for img in rest:
                found = locate(canvas, mask, img)
                if found:
                    placed.append((img, found[1], found[2]))
                    rest.remove(img)
                    break
            else:
                sys.exit(f"{len(rest)} image(s) do not overlap the others cleanly.")
            # positions found are canvas coordinates; convert back to a common frame
            x0, y0 = min(x for _, x, _ in placed[:-1]), min(y for _, _, y in placed[:-1])
            im, x, y = placed[-1]
            placed[-1] = (im, x + x0, y + y0)
    canvas, _ = compose(placed)
    if box:  # the capture script knows where the tree is
        canvas = canvas.crop((max(box[0] - crop, 0), max(box[1] - crop, 0),
                              min(box[2] - crop, canvas.width), min(box[3] - crop, canvas.height)))
    canvas.save(out, optimize=True)
    print(f"{out}: {canvas.width}x{canvas.height} from {len(placed)} images")


def main():
    if sys.argv[1] == "--dir":
        src, dst = sys.argv[2], sys.argv[3]
        os.makedirs(dst, exist_ok=True)
        for name in sorted(os.listdir(src)):
            layout = os.path.join(src, name, "layout.json")
            if os.path.exists(layout):
                stitch(os.path.join(dst, name + ".png"), [layout])
    else:
        stitch(sys.argv[1], sys.argv[2:])


main()
