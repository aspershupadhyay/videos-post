"""Track a flat surface (a desk, a laptop screen, a keyboard deck) through a shot, so a label can be pinned onto it the
way Apple's films pin "Up to 2000 nits peak brightness" onto the desk (brand/MOTION.md, "Labels live in the scene").

    python3 tools/track_plane.py <video> <t0> <t1> "<x1,y1 x2,y2 x3,y3 x4,y4>" <out.json> [--w 1920] [--show]

- The quad is the surface to follow, in px of the source frame scaled to --w wide (default 1920), on the frame at t0.
  Pick an area with texture (keys, a wood grain, screen UI); hands crossing it are fine (RANSAC drops those points).
- Writes {"fps", "w", "h", "t0", "t1", "quad", "H": [[9 floats] per frame]}: H maps a point on the t0 frame to the same
  point on frame i (row-major 3x3). `--show` also writes <out>.jpg, the quad redrawn on the first, middle and last frames.
- Use it in HyperFrames with `pin()` in videos/case-026-touch-macbook-pro/scripts/build_scenes.py: the label is laid out
  in the t0 frame's px, then a timeline proxy sets `transform: matrix3d(...)` per frame (deterministic, seek-safe).
Needs opencv-python-headless (pip install opencv-python-headless) and ffmpeg (decodes AV1/HEVC that cv2 can't).
"""
import json
import subprocess
import sys

import cv2
import numpy as np


def frames(video, t0, t1, w):
    probe = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height,r_frame_rate",
                            "-of", "csv=p=0", video], capture_output=True, text=True, check=True).stdout.strip().split(",")
    sw, sh = int(probe[0]), int(probe[1])
    num, den = map(int, probe[2].split("/"))
    h = round(sh * w / sw / 2) * 2
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-ss", str(t0), "-i", video, "-t", str(t1 - t0), "-vf", f"scale={w}:{h}",
                          "-f", "rawvideo", "-pix_fmt", "gray", "-"], stdout=subprocess.PIPE)
    out = []
    while True:
        buf = p.stdout.read(w * h)
        if len(buf) < w * h:
            break
        out.append(np.frombuffer(buf, np.uint8).reshape(h, w))
    p.wait()
    return out, num / den, h


def detect(img, quad):
    mask = np.zeros_like(img)
    cv2.fillConvexPoly(mask, quad.astype(np.int32), 255)
    pts = cv2.goodFeaturesToTrack(img, 400, 0.01, 7, mask=mask, blockSize=7)
    return pts.reshape(-1, 2) if pts is not None else np.zeros((0, 2), np.float32)


def track(video, t0, t1, quad, w=1920):
    imgs, fps, h = frames(video, t0, t1, w)
    quad = np.array(quad, np.float32)
    ref = detect(imgs[0], quad)                 # points on the t0 frame
    cur = ref.copy()                            # the same points on the previous frame
    Hs = [np.eye(3)]
    lk = dict(winSize=(25, 25), maxLevel=4, criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 30, 0.01))
    for i in range(1, len(imgs)):
        nxt, st, _ = cv2.calcOpticalFlowPyrLK(imgs[i - 1], imgs[i], cur.reshape(-1, 1, 2), None, **lk)
        back, st2, _ = cv2.calcOpticalFlowPyrLK(imgs[i], imgs[i - 1], nxt, None, **lk)
        ok = (st.ravel() == 1) & (st2.ravel() == 1) & (np.linalg.norm(back.reshape(-1, 2) - cur, axis=1) < 1.0)
        ref, cur = ref[ok], nxt.reshape(-1, 2)[ok]
        H = Hs[-1]
        if len(ref) >= 8:
            H, inl = cv2.findHomography(ref, cur, cv2.RANSAC, 3.0)
            if H is None:
                H = Hs[-1]
            else:
                ref, cur = ref[inl.ravel() == 1], cur[inl.ravel() == 1]
        Hs.append(H / H[2, 2])
        if len(ref) < 120:                      # top up: new points in the tracked quad, mapped back to t0
            q = cv2.perspectiveTransform(quad.reshape(-1, 1, 2), H).reshape(-1, 2)
            new = detect(imgs[i], q)
            if len(new):
                back0 = cv2.perspectiveTransform(new.reshape(-1, 1, 2), np.linalg.inv(H)).reshape(-1, 2)
                ref, cur = np.vstack([ref, back0]).astype(np.float32), np.vstack([cur, new]).astype(np.float32)
    return {"fps": fps, "w": w, "h": h, "t0": t0, "t1": t1, "quad": quad.tolist(),
            "H": [np.round(H.ravel(), 7).tolist() for H in Hs]}, imgs


def show(res, imgs, path):
    quad = np.array(res["quad"], np.float32).reshape(-1, 1, 2)
    tiles = []
    for i in (0, len(imgs) // 2, len(imgs) - 1):
        im = cv2.cvtColor(imgs[i], cv2.COLOR_GRAY2BGR)
        q = cv2.perspectiveTransform(quad, np.array(res["H"][i]).reshape(3, 3)).astype(np.int32)
        cv2.polylines(im, [q], True, (63, 72, 221), 4)
        tiles.append(cv2.resize(im, (640, round(640 * im.shape[0] / im.shape[1]))))
    cv2.imwrite(path, np.hstack(tiles))


if __name__ == "__main__":
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    w = int(sys.argv[sys.argv.index("--w") + 1]) if "--w" in sys.argv else 1920
    if "--w" in sys.argv:
        a.remove(str(w))
    video, t0, t1, quad, out = a[0], float(a[1]), float(a[2]), [list(map(float, p.split(","))) for p in a[3].split()], a[4]
    res, imgs = track(video, t0, t1, quad, w)
    json.dump(res, open(out, "w"))
    print(f"{len(res['H'])} frames at {res['fps']:.3f} fps -> {out}")
    if "--show" in sys.argv:
        show(res, imgs, out.rsplit(".", 1)[0] + ".jpg")
