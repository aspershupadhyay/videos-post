"""Place the voiceover lines, write word timings, and master the music bed.

    python3 scripts/prep_audio.py
"""
import json, subprocess
from pathlib import Path

P = Path(__file__).resolve().parent.parent
# Line id -> start in film seconds. Narration is the clock; scenes are cut to these.
STARTS = {"vo-01": 0.10, "vo-02": 5.50, "vo-03": 9.45, "vo-04": 15.45, "vo-05": 26.45,
          "vo-06": 32.30, "vo-07": 38.80, "vo-08": 46.85, "vo-09": 57.10, "vo-10": 63.85}
FILM = 69.7
MUSIC_IN = 6.0  # skip the quiet intro of the source track
# Baked into the bed (HyperFrames volume lanes don't lift above unity): silent for the beat
# before "The verdict", back with the post landing, +5 dB once the last word has been said.
ENVELOPE = ("volume='if(between(t,56.7,57.2),0,if(between(t,56.45,56.7),1-(t-56.45)/0.25,"
            "if(gt(t,67.8),1.78,if(gt(t,67.1),1+0.78*(t-67.1)/0.7,1))))':eval=frame")


def dur(f):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(f)]))


lines, words = [], []
for vid, start in STARTS.items():
    subs = json.loads((P / f"assets/vo/{vid}.subs.json").read_text())
    d = dur(P / f"assets/vo/{vid}.wav")
    lines.append({"id": vid, "start": start, "duration": round(d, 3), "end": round(start + d, 3)})
    for w in subs["words"]:
        words.append({"line": vid, "text": w["w"], "start": round(start + w["s"], 3), "end": round(start + w["e"], 3)})
(P / "assets/vo/timing.json").write_text(json.dumps({"film": FILM, "lines": lines, "words": words}, indent=1))

# Music bed: -26 LUFS integrated (about 12 dB under the -14 LUFS voice), true peak -2 dBTP.
subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(MUSIC_IN), "-t", str(FILM + 1), "-i", str(P / "assets/music/twisting-source.mp3"),
                "-af", "loudnorm=I=-26:TP=-2:LRA=11,afade=t=in:d=0.4," + ENVELOPE + f",afade=t=out:st={FILM - 1.6}:d=1.6",
                "-ar", "48000", str(P / "assets/music/bed.wav")], check=True)
for l in lines:
    print(l)
