"""Offline print treatments for the Tabloid and Zine looks (deterministic; run once per asset).

    python3 print_fx.py halftone IN OUT [--cell 9] [--ink 0a0a0a] [--paper none|PATH]
    python3 print_fx.py photocopy IN OUT [--paper PATH]
    python3 print_fx.py torn IN OUT [--seed 3] [--edge 18]      # torn-paper edge, transparent PNG

Real newsprint dots / xerox contrast / torn edges are baked into image files, so the video never fakes them with
CSS filters (HyperFrames contract). Keep `seed` fixed so re-runs are identical.
"""
import argparse
import math
import random
from PIL import Image, ImageDraw, ImageFilter, ImageOps


def halftone(src, cell=9, ink=(10, 10, 10), paper=None):
    g = ImageOps.autocontrast(src.convert("L"), cutoff=1)
    g = g.point(lambda v: int(255 * (v / 255) ** 0.5))  # lift midtones so dark sources still print
    w, h = g.size
    big = Image.new("L", (w * 2, h * 2), 255)
    d = ImageDraw.Draw(big)
    small = g.resize((max(1, w // cell), max(1, h // cell)), Image.BILINEAR)
    for y in range(small.height):
        for x in range(small.width):
            v = 1 - small.getpixel((x, y)) / 255
            r = cell * math.sqrt(v) * 0.78
            cx, cy = (x + 0.5) * cell * 2, (y + 0.5) * cell * 2
            if r > 0.4:
                d.ellipse((cx - r * 2, cy - r * 2, cx + r * 2, cy + r * 2), fill=0)
    mask = ImageOps.invert(big.resize((w, h), Image.LANCZOS))
    base = paper.resize((w, h)).convert("RGB") if paper else Image.new("RGB", (w, h), (244, 242, 238))
    base.paste(Image.new("RGB", (w, h), ink), (0, 0), mask)
    return base


def photocopy(src, paper=None):
    g = ImageOps.autocontrast(src.convert("L"), cutoff=3)
    g = g.point(lambda v: 0 if v < 70 else (255 if v > 175 else int((v - 70) * 255 / 105)))
    g = g.filter(ImageFilter.UnsharpMask(2, 160, 2))
    w, h = g.size
    base = paper.resize((w, h)).convert("RGB") if paper else Image.new("RGB", (w, h), (238, 236, 230))
    ink = Image.new("RGB", (w, h), (18, 18, 18))
    base.paste(ink, (0, 0), ImageOps.invert(g))
    return base


def torn(src, seed=3, edge=18):
    rnd = random.Random(seed)
    w, h = src.size
    pts = []
    def side(a, b, n, axis):
        for i in range(n + 1):
            t = i / n
            x = a[0] + (b[0] - a[0]) * t
            y = a[1] + (b[1] - a[1]) * t
            j = rnd.uniform(0, edge) * (0.35 + 0.65 * rnd.random())
            pts.append((x + (j if axis == "l" else -j if axis == "r" else 0), y + (j if axis == "t" else -j if axis == "b" else 0)))
    n = max(80, (w + h) // 12)
    side((0, 0), (w, 0), n, "t"); side((w, 0), (w, h), n, "r"); side((w, h), (0, h), n, "b"); side((0, h), (0, 0), n, "l")
    m = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m).polygon(pts, fill=255)
    out = src.convert("RGBA"); out.putalpha(m)
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["halftone", "photocopy", "torn"])
    ap.add_argument("src"); ap.add_argument("out")
    ap.add_argument("--cell", type=int, default=9); ap.add_argument("--ink", default="0a0a0a")
    ap.add_argument("--paper"); ap.add_argument("--seed", type=int, default=3); ap.add_argument("--edge", type=int, default=18)
    a = ap.parse_args()
    im = Image.open(a.src)
    paper = Image.open(a.paper) if a.paper else None
    if a.mode == "halftone":
        im = halftone(im, a.cell, tuple(int(a.ink[i:i + 2], 16) for i in (0, 2, 4)), paper)
    elif a.mode == "photocopy":
        im = photocopy(im, paper)
    else:
        im = torn(im, a.seed, a.edge)
    im.save(a.out)
    print(a.out, im.size)
