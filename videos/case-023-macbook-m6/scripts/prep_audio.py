"""Level the voice lines, place them on the film clock, find phrase onsets, master the music bed.

    python3 scripts/prep_audio.py

Picked takes: hook A (vo-01) and the "M one" spelling (vo-04: "M1," 0.74 s with a beat after it, vs "M1" 0.66 s in
vo-04b); hooks B/C and vo-04b stay in assets/vo/raw for A/B.
Phrase onsets inside a line come from its own pauses (silencedetect); word times from Whisper
(assets/vo/raw/subs/*.subs.json) are copied in as "words" for cues that land on a word.
Writes assets/vo/timing.json and assets/music/bed.wav.
"""
import json
import re
import subprocess
from pathlib import Path

P = Path(__file__).resolve().parent.parent
RAW = P / "assets/vo/raw"
# line id -> (raw take, gap before it). The payoff (vo-06) and the repeatable line (vo-09) get air.
LINES = {"vo-01": ("vo-01", 0.10), "vo-02": ("vo-02", 0.25), "vo-03": ("vo-03", 0.45), "vo-04": ("vo-04", 0.30),
         "vo-05": ("vo-05", 0.45), "vo-06": ("vo-06", 0.40), "vo-07": ("vo-07", 0.25), "vo-08": ("vo-08", 0.45),
         "vo-09": ("vo-09", 0.50), "vo-10": ("vo-10", 0.50)}
TAIL = 3.6      # end card holds after the last word
MUSIC_IN = 0.0


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
for vid, (take, gap) in LINES.items():
    src, out = RAW / f"{take}.wav", P / f"assets/vo/{vid}.wav"
    gain = -14.0 - lufs(src)
    run("ffmpeg", "-v", "error", "-y", "-i", str(src), "-af", f"volume={gain:.2f}dB,alimiter=limit=0.89:level=false",
        "-ar", "48000", str(out))
    t += gap
    d = dur(out)
    words = json.loads((RAW / f"subs/{take}.subs.json").read_text())["words"]
    lines.append({"id": vid, "take": take, "start": round(t, 3), "duration": round(d, 3), "end": round(t + d, 3),
                  "phrases": [round(t + o, 3) for o in onsets(out)],
                  "words": [[w["w"], round(t + w["s"], 3), round(t + w["e"], 3)] for w in words]})
    t += d
film = round(t + TAIL, 2)
(P / "assets/vo/timing.json").write_text(json.dumps({"film": film, "lines": lines}, indent=1))

l = {x["id"]: x for x in lines}
quiet_a, quiet_b = l["vo-03"]["start"] - 0.3, l["vo-04"]["start"] + 0.1   # music drops out under the fine print (vo-03)
lift = l["vo-10"]["end"]
env = (f"volume='if(between(t,{quiet_a:.2f},{quiet_b:.2f}),0.12,if(between(t,{quiet_b:.2f},{quiet_b + 0.6:.2f}),"
       f"0.12+0.88*(t-{quiet_b:.2f})/0.6,if(gt(t,{lift + 0.4:.2f}),1.78,if(gt(t,{lift:.2f}),1+0.78*(t-{lift:.2f})/0.4,1))))':eval=frame")
run("ffmpeg", "-v", "error", "-y", "-ss", str(MUSIC_IN), "-t", str(film + 1), "-i", str(P / "assets/music/voxel-revolution-source.mp3"),
    "-af", "loudnorm=I=-26:TP=-2:LRA=11,afade=t=in:d=0.3," + env + f",afade=t=out:st={film - 1.6}:d=1.6",
    "-ar", "48000", str(P / "assets/music/bed.wav"))
print("film", film)
for x in lines:
    print(x["id"], x["start"], x["end"], x["phrases"])
