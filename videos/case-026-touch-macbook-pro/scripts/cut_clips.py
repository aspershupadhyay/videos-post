"""Cut the 9:16 shots from Apple's film (the creator's 4K upload, VoiceBox Files: Videos / MacBook.mp4).

    python3 scripts/cut_clips.py <MacBook.mp4> [name ...]

Each shot: (source in, source out, crop centre x in 1920-wide px, speed). The 9:16 window is 1215x2160 of the 3840x2160
master (cx * 2 +- 607), scaled to 1080x1920, 30 fps, no audio. speed < 1 slows it (setpts; Apple shot at 23.976); a negative speed plays it backwards.
Writes assets/clips/<name>.mp4 and assets/clips/shots.json (in, out, cx, speed) for the tracker mapping in build_scenes.py.
"""
import json
import subprocess
import sys
from pathlib import Path

P = Path(__file__).resolve().parent.parent
SHOTS = {
    "spin":    (42.00, 44.10, 780, 0.75),   # a finger turns a 3D model on the screen (hook, frame 0's payoff)
    "macro":   (44.15, 44.78, 900, 0.50),   # the finger on the model, macro
    "arm":     (38.45, 41.68, 1000, 1.0),   # an arm reaching out to the screen: Jobs' "your arm wants to fall off"
    "armrev":  (39.90, 41.68, 1000, -1.25), # the same arm, played backwards: "you never have to lift it"
    "logo":    (3.20, 6.60, 960, 1.0),      # the closed lid, its logo lights up
    "open":    (8.50, 11.40, 760, 0.70),     # hands on the keyboard as the camera swings round (tracked)
    "finder":  (46.90, 48.24, 1100, 1.0),   # dragging files with a finger
    "car":     (71.30, 74.05, 900, 1.0),    # pinching a 3D car
    "piano":   (79.50, 83.60, 850, 1.0),    # playing a piano on the display
    "red":     (14.40, 15.95, 900, 0.58),    # the OLED: Photoshop art, deep blacks
    "tap":     (57.95, 59.00, 1150, 0.48),   # a hand touches the screen (hook)
    "tap2":    (33.95, 35.30, 1420, 0.45),   # a hand on the screen, the hinge in view
    "carry":   (69.44, 71.27, 960, 1.0),    # Apple's own "3 pounds light" label
    "drone1":  (96.43, 98.40, 960, 1.0),    # FPV over the rocks
    "magsafe": (90.72, 92.10, 960, 1.0),    # the port labels (Apple's)
    "hdmi":    (92.90, 94.20, 960, 1.0),
    "close":   (107.40, 110.12, 960, 0.85),  # the lid closes, the logo glows: the bookend
}


def cut(src, name, t0, t1, cx, speed):
    x = max(0, min(3840 - 1215, round(cx * 2 - 607.5)))
    vf = f"crop=1215:2160:{x}:0,scale=1080:1920:flags=lanczos,setpts=(PTS-STARTPTS)/{abs(speed)},fps=30"
    out = P / f"assets/clips/{name}.mp4"
    enc = ["-c:v", "libx264", "-crf", "17", "-preset", "slow", "-pix_fmt", "yuv420p", "-movflags", "+faststart"]
    fwd = out.with_suffix(".fwd.mp4") if speed < 0 else out
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t0}", "-t", f"{t1 - t0:.3f}", "-i", src, "-an", "-vf", vf, *enc,
                    str(fwd)], check=True)
    if speed < 0:   # backwards: a second pass, with fresh frame-numbered timestamps
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(fwd), "-vf", "reverse,setpts=N/30/TB", "-r", "30", *enc, str(out)], check=True)
        fwd.unlink()


if __name__ == "__main__":
    src, only = sys.argv[1], set(sys.argv[2:])
    for name, (t0, t1, cx, speed) in SHOTS.items():
        if not only or name in only:
            cut(src, name, t0, t1, cx, speed)
            print(name, round((t1 - t0) / abs(speed), 2), "s")
    (P / "assets/clips/shots.json").write_text(json.dumps(
        {k: {"in": a, "out": b, "cx": c, "speed": s} for k, (a, b, c, s) in SHOTS.items()}, indent=1))
