"""Cut the Nexus Institute footage into the film's two clips and its dialogue track.

    python3 scripts/cut_clips.py <path to veliz-nexus.mp4>

Source: "Is technology neutral?" (Nexus Institute, youtube.com/watch?v=AhED5V1TcC0), 1920x1080 50 fps, as uploaded to
VoiceBox Files (Videos / veliz-nexus.mp4) by the creator. Clips are git-ignored (too big); this script rebuilds them.

Each shot is reframed to 9:16 by its own crop (562x1000 from the top of the frame, so Nexus's burned-in name bar at
y 1010+ and its white side bar at x 1838+ stay out); the one wide shot sits 16:9 over a blurred copy of itself.
Cut times are the source's own cuts (ffmpeg scdet at 50 fps); speech edges from a 25 ms loudness profile.
Writes assets/clips/coldopen.mp4, assets/clips/main.mp4, assets/audio/coldopen.wav, assets/audio/main.wav.
"""
import subprocess
import sys
from pathlib import Path

P = Path(__file__).resolve().parent.parent
SRC = sys.argv[1]
W, H = 562, 1000          # crop box; scaled to 1080x1920
FPS = 30

# Cold open: Véliz, "It would never occur to you to cook with a gun. It's not made for that."
COLD = (82.90, 87.00, 829)
# Main: AlQama's "I think technology in and of itself…" (59.85) to his "I agree." (ends 109.40); the picture ends at
# 109.60 and the dialogue track runs on into the applause (to 113.40) under the end card.
SHOTS = [  # (src in, src out, crop x | "wide")  — speaker
    (59.85, 60.08, 829),     # AlQama
    (60.08, 72.22, 979),     # Véliz listening, over his shoulder (he speaks)
    (72.22, 74.32, "wide"),  # the panel
    (74.32, 75.86, 799),     # AlQama ("You can jump in now." / laughter)
    (75.86, 89.30, 829),     # Véliz: never neutral … cook with a gun … to threaten or kill
    (89.30, 93.08, 499),     # AlQama listening
    (93.08, 105.66, 859),    # Véliz: A.I. … surveil … made to control
    (105.66, 109.60, 559),   # AlQama: "I agree."
]
AUDIO_END = 113.40


def run(*a):
    subprocess.run(a, check=True)


def shot_filter(i, a, b, x):
    trim = f"[0:v]trim={a}:{b},setpts=PTS-STARTPTS,fps={FPS}"
    if x == "wide":
        return (f"{trim},split[w{i}a][w{i}b];"
                f"[w{i}a]crop=1838:1080:0:0,scale=-2:1920,crop=1080:1920,boxblur=40:2,eq=brightness=-0.12[w{i}bg];"
                f"[w{i}b]crop=1838:1080:0:0,scale=1080:-2[w{i}fg];"
                f"[w{i}bg][w{i}fg]overlay=0:(H-h)/2,setsar=1[v{i}]")
    return f"{trim},crop={W}:{H}:{x}:0,scale=1080:1920:flags=lanczos,setsar=1[v{i}]"


(P / "assets/clips").mkdir(parents=True, exist_ok=True)
(P / "assets/audio").mkdir(parents=True, exist_ok=True)
enc = ["-c:v", "libx264", "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-an"]

a, b, x = COLD
run("ffmpeg", "-v", "error", "-y", "-i", SRC, "-filter_complex", shot_filter(0, a, b, x), "-map", "[v0]", *enc,
    str(P / "assets/clips/coldopen.mp4"))

fc = ";".join(shot_filter(i, s, e, x) for i, (s, e, x) in enumerate(SHOTS))
fc += ";" + "".join(f"[v{i}]" for i in range(len(SHOTS))) + f"concat=n={len(SHOTS)}:v=1:a=0[v]"
run("ffmpeg", "-v", "error", "-y", "-i", SRC, "-filter_complex", fc, "-map", "[v]", *enc, str(P / "assets/clips/main.mp4"))

# Dialogue: one gain for both (measured on the main stretch), so the cold open and the debate sit at the same level.
m0, m1 = SHOTS[0][0], AUDIO_END
run("ffmpeg", "-v", "error", "-y", "-ss", str(m0), "-to", str(m1), "-i", SRC, "-vn", "-ac", "2", "-ar", "48000",
    "-af", f"loudnorm=I=-15:TP=-1.5:LRA=11,afade=t=in:d=0.02,afade=t=out:st={m1 - m0 - 1.6:.2f}:d=1.6",
    str(P / "assets/audio/main.wav"))
run("ffmpeg", "-v", "error", "-y", "-ss", str(a), "-to", str(b), "-i", SRC, "-vn", "-ac", "2", "-ar", "48000",
    "-af", f"loudnorm=I=-15:TP=-1.5:LRA=11,afade=t=in:d=0.015,afade=t=out:st={b - a - 0.05:.2f}:d=0.05",
    str(P / "assets/audio/coldopen.wav"))
print("main video", round(sum(e - s for s, e, _ in SHOTS), 2), "s; main audio", round(m1 - m0, 2), "s; cold open", round(b - a, 2), "s")
