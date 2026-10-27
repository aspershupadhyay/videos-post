"""Level the voice lines, place them on the film clock, find phrase onsets, master the music bed.

    python3 scripts/prep_audio.py

No Whisper subtitles: phrase onsets inside a line come from its own pauses (silencedetect), which is all
the cues need. Writes assets/vo/timing.json and assets/music/bed.wav.
"""
import json
import re
import subprocess
from pathlib import Path

P = Path(__file__).resolve().parent.parent
RAW = P / "assets/vo/raw"
# gap (s) before each line; the twist (vo-08) and the repeatable line (vo-12) get air.
GAPS = {"vo-01": 0.12, "vo-02": 0.22, "vo-03": 0.15, "vo-04": 0.35, "vo-05": 0.25, "vo-06": 0.3, "vo-07": 0.35,
        "vo-08": 0.75, "vo-09": 0.35, "vo-10": 0.3, "vo-11": 0.3, "vo-12": 0.55, "vo-13": 0.45}
TAIL = 3.2      # end card holds after the last word
MUSIC_IN = 18.0


def run(*a):
    return subprocess.run(a, check=True, capture_output=True, text=True)


def lufs(f):
    err = run("ffmpeg", "-hide_banner", "-i", str(f), "-af", "ebur128", "-f", "null", "-").stderr
    return float(re.findall(r"I:\s+(-?[\d.]+) LUFS", err)[-1])


def dur(f):
    return float(run("ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(f)).stdout)


def onsets(f):
    err = run("ffmpeg", "-hide_banner", "-i", str(f), "-af", "silencedetect=n=-38dB:d=0.11", "-f", "null", "-").stderr
    return [0.0] + [round(float(x), 3) for x in re.findall(r"silence_end: ([\d.]+)", err)]


lines, t = [], 0.0
for vid, gap in GAPS.items():
    src, out = RAW / f"{vid}.wav", P / f"assets/vo/{vid}.wav"
    gain = -14.0 - lufs(src)
    run("ffmpeg", "-v", "error", "-y", "-i", str(src), "-af", f"volume={gain:.2f}dB,alimiter=limit=0.89:level=false",
        "-ar", "48000", str(out))
    t += gap
    d = dur(out)
    lines.append({"id": vid, "start": round(t, 3), "duration": round(d, 3), "end": round(t + d, 3),
                  "phrases": [round(t + o, 3) for o in onsets(out)]})
    t += d
film = round(t + TAIL, 2)
(P / "assets/vo/timing.json").write_text(json.dumps({"film": film, "lines": lines}, indent=1))

l = {x["id"]: x for x in lines}
quiet_a, quiet_b = l["vo-07"]["end"], l["vo-08"]["start"] + 1.2   # music drops out for the twist
lift = l["vo-13"]["end"]
env = (f"volume='if(between(t,{quiet_a:.2f},{quiet_b:.2f}),0.12,if(between(t,{quiet_b:.2f},{quiet_b + 0.6:.2f}),"
       f"0.12+0.88*(t-{quiet_b:.2f})/0.6,if(gt(t,{lift + 0.4:.2f}),1.78,if(gt(t,{lift:.2f}),1+0.78*(t-{lift:.2f})/0.4,1))))':eval=frame")
run("ffmpeg", "-v", "error", "-y", "-ss", str(MUSIC_IN), "-t", str(film + 1), "-i", str(P / "assets/music/ethernight-club-source.mp3"),
    "-af", "loudnorm=I=-26:TP=-2:LRA=11,afade=t=in:d=0.3," + env + f",afade=t=out:st={film - 1.6}:d=1.6",
    "-ar", "48000", str(P / "assets/music/bed.wav"))
print("film", film)
for x in lines:
    print(x["id"], x["start"], x["end"], x["phrases"])
