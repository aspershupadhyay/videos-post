"""Place the voiceover lines, write word timings, and master the music bed (envelope baked in).

    python3 scripts/prep_audio.py
"""
import json
import subprocess
from pathlib import Path

P = Path(__file__).resolve().parent.parent
# Line id -> film start (s). The voice is the clock; scenes are cut to these words.
STARTS = {
    "vo-01": 0.15, "vo-02": 3.35, "vo-03": 7.30, "vo-04": 13.10,  # the walking story
    "vo-05": 17.30, "vo-06": 21.90,                               # the reveal + what it builds
    "vo-07": 28.40, "vo-08": 36.45,                               # the benchmark
    "vo-09": 39.75,                                               # re-hook (music drops out)
    "vo-10": 41.85, "vo-11": 50.60,                               # the cyber cut
    "vo-12": 54.15, "vo-13": 62.80,                               # the catch + the gap
    "vo-14": 67.95,                                               # CTA
}
FILM = 74.0
MUSIC_IN = 18.0  # "Ethernight Club": skip the sparse intro
# Bed envelope: full under the story; out from the end of vo-08 until "Moonshot made it worse";
# back in under the voice; +5 dB once the last word has been said.
ENVELOPE = ("volume='if(between(t,39.15,41.8),0,if(between(t,38.9,39.15),1-(t-38.9)/0.25,"
            "if(between(t,41.8,42.6),(t-41.8)/0.8,if(gt(t,72.4),1.78,if(gt(t,71.9),1+0.78*(t-71.9)/0.5,1)))))':eval=frame")


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

subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(MUSIC_IN), "-t", str(FILM + 1),
                "-i", str(P / "assets/music/ethernight-club-source.mp3"),
                "-af", "loudnorm=I=-26:TP=-2:LRA=11,afade=t=in:d=0.3," + ENVELOPE + f",afade=t=out:st={FILM - 1.8}:d=1.8",
                "-ar", "48000", str(P / "assets/music/bed.wav")], check=True)
for l in lines:
    print(l)
