"""Level the voice lines, place them on the film clock, find phrase onsets, master the music bed.

    python3 scripts/prep_audio.py

Picked takes: hook A (vo-01, 8 words, rule: line 1 <= 8 words); "3D" (vo-05b, 0.30 s, same length as "three-D" in vo-05);
"OLED" (vo-07, one 0.38 s word, vs "oh-led" in vo-07b). Hooks B/C and the other spellings stay in assets/vo/raw for A/B.
Word times: assets/vo/raw/subs/*.subs.json (scripts/word_times.py). Writes assets/vo/timing.json and assets/music/bed.wav.
"""
import json
import re
import subprocess
from pathlib import Path

P = Path(__file__).resolve().parent.parent
RAW = P / "assets/vo/raw"
# line id -> (raw take, gap before it). The re-hook (vo-08), the payoff (vo-09) and the line (vo-12) get air.
LINES = {"vo-01": ("vo-01", 0.10), "vo-02": ("vo-02", 0.25), "vo-03": ("vo-03", 0.30), "vo-04": ("vo-04", 0.35),
         "vo-05": ("vo-05b", 0.15), "vo-06": ("vo-06", 0.15), "vo-07": ("vo-07", 0.30), "vo-08": ("vo-08", 0.50),
         "vo-09": ("vo-09", 0.40), "vo-10": ("vo-10", 0.25), "vo-11": ("vo-11", 0.45), "vo-12": ("vo-12", 0.50),
         "vo-13": ("vo-13", 0.50)}
TAIL = 3.6      # end card holds after the last word
MUSIC_IN = 2.0  # Pamgaea is at full groove from 2 s


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


def wt(vid, word):
    return next(s for ww, s, e in l[vid]["words"] if re.sub(r"[^\w]", "", ww).lower() == word)


# dips: the re-hook "So, what about the arm?" (vo-08) and the fine print ("The only fine print? Weight varies.")
dips = [(l["vo-08"]["start"] - 0.35, l["vo-09"]["start"] + 0.05), (wt("vo-11", "only") - 0.25, l["vo-11"]["end"] + 0.1)]
lift = l["vo-13"]["end"]


def dip(a, b, low=0.16, ramp=0.25):
    return (f"if(between(t,{a:.2f},{b:.2f}),{low},if(between(t,{a - ramp:.2f},{a:.2f}),1-(1-{low})*(t-{a - ramp:.2f})/{ramp},"
            f"if(between(t,{b:.2f},{b + ramp:.2f}),{low}+(1-{low})*(t-{b:.2f})/{ramp},")


expr = "".join(dip(a, b) for a, b in dips) + f"if(gt(t,{lift + 0.4:.2f}),1.7,if(gt(t,{lift:.2f}),1+0.7*(t-{lift:.2f})/0.4,1))" + ")))" * len(dips)
run("ffmpeg", "-v", "error", "-y", "-ss", str(MUSIC_IN), "-t", str(film + 1), "-i", str(P / "assets/music/pamgaea-source.mp3"),
    "-af", f"loudnorm=I=-26:TP=-2:LRA=11,afade=t=in:d=0.15,volume='{expr}':eval=frame,afade=t=out:st={film - 1.6}:d=1.6",
    "-ar", "48000", str(P / "assets/music/bed.wav"))
print("film", film)
for x in lines:
    print(x["id"], x["start"], x["end"], x["phrases"])
