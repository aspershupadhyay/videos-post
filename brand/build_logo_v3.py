"""Cut the CatchTheError logo v3 (the creator's "ct(e)" mark, 2026-10-27) into animatable layers.

Source: brand/logo-v3/cte-logo-source.png (1080 x 1080, the creator's file; never edit it).
Out:    brand/logo-v3/layers/*.png, full-canvas 1080 x 1080 RGBA layers that share one coordinate
        system, so stacking them at the same box rebuilds the logo exactly:
          c.png t.png e.png   red letters (flat #DD483F)
          circle.png          the hand-drawn red pen circle round the "e"
          rule.png            the grey baseline the "e" drops under
          tagline.png         CATCH · THE · ERROR
          mark-on-paper.png   letters + circle + rule + tagline on the paper ground (static logo)
        brand/logo-v3/geometry.json: each layer's box and the circle's centre, for the motion sting.

    python3 brand/build_logo_v3.py
"""
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

D = Path(__file__).resolve().parent / "logo-v3"
OUT = D / "layers"
RED = (221, 72, 63)
GREY = (88, 88, 86)

src = np.asarray(Image.open(D / "cte-logo-source.png").convert("RGB")).astype(np.float32)
R, G, B = src[..., 0], src[..., 1], src[..., 2]
H, W = R.shape

# Red ink: the paper is neutral grey (R ~ G), the ink is R - G ~ 149.
red_a = np.clip((R - G - 6) / (RED[0] - RED[1] - 6), 0, 1)

# Letters are ~40 px strokes, the pen circle ~6 px: an opening (min then max filter) keeps only the letters.
m = Image.fromarray((red_a > 0.5).astype(np.uint8) * 255)
letters = np.asarray(m.filter(ImageFilter.MinFilter(13)).filter(ImageFilter.MaxFilter(13))) > 0


def largest(mask):
    """Keep the largest 4-connected blob of a boolean mask (drops pen fragments that survive the opening)."""
    seen, best = np.zeros_like(mask), []
    for y0, x0 in zip(*np.nonzero(mask)):
        if seen[y0, x0]:
            continue
        stack, blob = [(y0, x0)], []
        seen[y0, x0] = True
        while stack:
            y, x = stack.pop()
            blob.append((y, x))
            for yy, xx in ((y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)):
                if 0 <= yy < mask.shape[0] and 0 <= xx < mask.shape[1] and mask[yy, xx] and not seen[yy, xx]:
                    seen[yy, xx] = True
                    stack.append((yy, xx))
        if len(blob) > len(best):
            best = blob
    out = np.zeros_like(mask)
    ys, xs = zip(*best)
    out[list(ys), list(xs)] = True
    return out


def grow(mask, n):
    return np.asarray(Image.fromarray(mask.astype(np.uint8) * 255).filter(ImageFilter.MaxFilter(n))) > 0


# Split the letters by column gaps: c | t | e.
cols = letters.any(axis=0)
runs, x = [], 0
while x < W:
    if cols[x]:
        x0 = x
        while x < W and cols[x]:
            x += 1
        runs.append((x0, x))
    x += 1
runs = [r for r in runs if r[1] - r[0] > 40]  # a doubled pen stroke can survive the opening
assert len(runs) == 3, f"expected c, t, e; got {runs}"

# Grey ink (rule + tagline): darker than the local paper, not red.
L = (R + G + B) / 3
# The paper has a vignette, so measure ink against the local paper (a max filter of the luminance).
paperL = np.asarray(Image.fromarray(L.astype(np.uint8)).filter(ImageFilter.MaxFilter(21)).filter(ImageFilter.GaussianBlur(6))).astype(np.float32)
grey_a = np.clip((paperL - L - 8) / (paperL - GREY[0] - 8), 0, 1) * (red_a < 0.05)


def layer(alpha, rgb, name):
    a = (np.clip(alpha, 0, 1) * 255).astype(np.uint8)
    img = np.zeros((H, W, 4), np.uint8)
    img[..., :3] = rgb
    img[..., 3] = a
    Image.fromarray(img, "RGBA").save(OUT / f"{name}.png", optimize=True)
    ys, xs = np.nonzero(a > 20)
    return {"x": int(xs.min()), "y": int(ys.min()), "w": int(xs.max() - xs.min() + 1), "h": int(ys.max() - ys.min() + 1)}


OUT.mkdir(parents=True, exist_ok=True)
geo = {"canvas": [W, H]}
letters_d = np.zeros_like(letters)
for name, (x0, x1) in zip("cte", runs):
    box = np.zeros_like(letters)
    box[:, max(0, x0 - 2):x1 + 2] = True
    one = grow(largest(letters & box), 5)
    letters_d |= one
    geo[name] = layer(red_a * one, RED, name)

geo["circle"] = layer(red_a * (~letters_d), RED, "circle")
c = geo["circle"]
geo["circle"]["cx"], geo["circle"]["cy"] = c["x"] + c["w"] // 2, c["y"] + c["h"] // 2

# The rule is the thin grey line around y ~ 590; the tagline sits around y ~ 885.
rule = np.zeros_like(grey_a)
rule[560:620, 200:880] = grey_a[560:620, 200:880]
geo["rule"] = layer(rule, (128, 128, 126), "rule")
tag = np.zeros_like(grey_a)
tag[850:920, 300:780] = grey_a[850:920, 300:780]
geo["tagline"] = layer(tag, GREY, "tagline")

# Static mark on a flat paper ground (the source's vignette and grain dropped).
paper = Image.new("RGBA", (W, H), (231, 231, 229, 255))
for n in ["rule", "c", "t", "e", "circle", "tagline"]:
    paper.alpha_composite(Image.open(OUT / f"{n}.png"))
paper.convert("RGB").save(D / "mark-on-paper.png", optimize=True)

(D / "geometry.json").write_text(json.dumps(geo, indent=1))
print(json.dumps(geo))

# Paper ground for 9:16 videos, matched to the logo's ground: flat #E7E7E5 centre, soft vignette, fixed-seed grain.
rng = np.random.default_rng(21)
yy, xx = np.mgrid[0:1920, 0:1080].astype(np.float32)
r = np.sqrt(((xx - 540) / 760) ** 2 + ((yy - 960) / 1250) ** 2)
base = 231 - 16 * np.clip(r - 0.35, 0, 1) ** 1.6
grain = rng.normal(0, 2.2, (1920, 1080)).astype(np.float32)
specks = (rng.random((1920, 1080)) > 0.9985) * rng.uniform(-14, -6, (1920, 1080))
g = np.clip(base + grain + specks, 0, 255)
paper = np.stack([g, g, g - 2], -1).astype(np.uint8)
Image.fromarray(paper).save(D / "paper-1080x1920.png", optimize=True)

# The pen circle on its own, cropped to its box: the brand's "red pen" for circling things in videos.
c = geo["circle"]
Image.open(OUT / "circle.png").crop((c["x"], c["y"], c["x"] + c["w"], c["y"] + c["h"])).save(OUT / "circle-crop.png", optimize=True)
