#!/usr/bin/env python3
"""Flag dead visuals in a render: empty frames (nothing but ground) and frozen stretches.

    python3 tools/qa_frames.py videos/<case>/renders/<file>.mp4 [--ground dark|light]

Samples 10 fps at 54x96 greyscale (fast: ~5 s for a 75 s film). Exit code 1 if anything fails,
so it can gate a delivery. Thresholds come from the Case 018 post-mortem (6 empty gaps of 0.6-1.1 s
at scene starts on a black ground).

  EMPTY   < 1% of pixels differ from the ground for >= 0.3 s   -> fail (something must be on screen)
  STATIC  no visible change for > 2.0 s                        -> fail (add a push, a build, a cut)
"""
import argparse
import subprocess
import sys

W, H, FPS = 54, 96, 10
EMPTY_MIN_S, STATIC_MAX_S = 0.3, 2.0


def frames(path):
    raw = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", path, "-vf", f"fps={FPS},scale={W}:{H},format=gray",
         "-f", "rawvideo", "-"],
        check=True, capture_output=True).stdout
    n = W * H
    return [raw[i * n:(i + 1) * n] for i in range(len(raw) // n)]


def runs(flags, min_len):
    out, start = [], None
    for i, f in enumerate(flags + [False]):
        if f and start is None:
            start = i
        elif not f and start is not None:
            if (i - start) / FPS >= min_len:
                out.append((start / FPS, i / FPS))
            start = None
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--ground", choices=["dark", "light"], default="dark")
    a = ap.parse_args()

    fs = frames(a.video)
    n = W * H
    if a.ground == "dark":
        empty = [sum(b > 40 for b in f) / n < 0.01 for f in fs]
    else:
        empty = [sum(b < 215 for b in f) / n < 0.01 for f in fs]
    static = [False] + [sum(abs(x - y) for x, y in zip(f, p)) / n < 0.3 for f, p in zip(fs[1:], fs)]

    # the last 3 s may hold still on the end card
    tail = len(fs) - 3 * FPS
    static = [s and i < tail for i, s in enumerate(static)]

    bad = [("EMPTY", r) for r in runs(empty, EMPTY_MIN_S)] + \
          [("STATIC", r) for r in runs(static, STATIC_MAX_S)]
    for kind, (s, e) in sorted(bad, key=lambda b: b[1]):
        print(f"{kind:6} {s:6.1f}-{e:.1f}s  ({e - s:.1f}s)")
    print(f"{len(fs) / FPS:.1f}s checked: " + ("PASS" if not bad else f"FAIL ({len(bad)})"))
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
