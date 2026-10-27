"""Write the SFX <audio> tags into index.html from scripts/sfx_cues.json.

Each cue names the film time its picture lands; the clip is placed so its measured
peak arrives one frame (1/30 s) after it. Rerun after changing a cue or a file.

    python3 scripts/build_sfx.py
"""
import json
import re
import subprocess
from pathlib import Path

import numpy as np

P = Path(__file__).resolve().parent.parent
FRAME = 1 / 30
FILM = json.loads((P / "assets/vo/timing.json").read_text())["film"]
_peaks = {}


def peak(name, media_start=0.0):
    key = (name, media_start)
    if key not in _peaks:
        raw = subprocess.check_output(["ffmpeg", "-v", "error", "-ss", str(media_start), "-i", str(P / f"assets/sfx/{name}.mp3"), "-ac", "1", "-ar", "48000", "-f", "f32le", "-"])
        a = np.frombuffer(raw, dtype=np.float32)
        _peaks[key] = (int(np.argmax(np.abs(a))) / 48000, len(a) / 48000)
    return _peaks[key]


cues = json.loads((P / "scripts/sfx_cues.json").read_text())["cues"]
tags = []
lanes = []  # end time of the last clip on each SFX lane; layered hits go on separate lanes
for i, cue in enumerate(cues):
    hit, name, vol, label = cue[:4]
    media_start = cue[4] if len(cue) > 4 else 0.0
    pk, length = peak(name, media_start)
    start = max(0.0, hit + FRAME - pk)
    dur = min(length, FILM - start)
    lane = next((n for n, end in enumerate(lanes) if end <= start), len(lanes))
    if lane == len(lanes):
        lanes.append(0.0)
    lanes[lane] = start + dur
    extra = f' data-media-start="{media_start}"' if media_start else ""
    tags.append(
        f'      <audio id="sfx-{i + 1:02d}" class="clip" src="assets/sfx/{name}.mp3" data-start="{start:.3f}" data-duration="{dur:.3f}"{extra} '
        f'data-track-index="{12 + lane}" data-volume="{vol}" data-audio-group="sfx"></audio><!-- {label} -->'
    )

index = (P / "index.html").read_text()
index = re.sub(
    r"(<!-- SFX:BEGIN[^>]*-->\n).*?(\s*<!-- SFX:END -->)",
    lambda m: m.group(1) + "\n".join(tags) + m.group(2),
    index,
    flags=re.S,
)
(P / "index.html").write_text(index)
print(len(tags), "sfx cues written")
