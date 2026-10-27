"""Write scripts/sfx_cues.json from the voice timings (so a re-voiced line moves its SFX too), then run build_sfx.py.
Each cue: [film time the picture lands, sfx file, volume, label]. Takes rotate (scratch-a/b/c, thud/plate/drop)."""
import json
import subprocess
from pathlib import Path

P = Path(__file__).resolve().parent.parent
T = json.loads((P / "assets/vo/timing.json").read_text())
L = {l["id"]: l for l in T["lines"]}
cut = lambda vid: round(L[vid]["start"] - 0.2, 2)


def w(vid, word, n=1):
    import re
    return [s for ww, s, e in L[vid]["words"] if re.sub(r"[^\w.]", "", ww).lower().strip(".") == word][n - 1]


sting = cut("vo-10") + 0.05
cues = [
    [w("vo-01", "photo") - 0.06, "whoosh-short", 0.12, "toy -> photo swap"],
    [w("vo-01", "sentence") - 0.3, "typing", 0.10, "the prompt types"],
    [w("vo-01", "designed") - 0.32, "whoosh", 0.18, "zoom through into the toy"],
    [w("vo-01", "toy"), "pop", 0.2, "red asterisk"],
    [cut("vo-02"), "tick-a", 0.2, "cut to the demo"],
    [w("vo-02", "tiny") + 0.25, "scratch-c", 0.45, "pen ring round the footnote"],
    [cut("vo-03") + 1.6, "whoosh-cinematic", 0.10, "earth -> Lisbon zoom"],
    [w("vo-03", "gpt") - 0.1, "key-press", 0.2, "pill types GPT-6.1 Terra"],
    [w("vo-03", "chat") + 0.15, "scratch-a", 0.4, "strike 'built to chat'"],
    [w("vo-03", "built", 2), "typing", 0.12, "built to use your computer"],
    [w("vo-03", "computer") + 0.15, "whoosh-short", 0.14, "the world shrinks into a card"],
    [cut("vo-04"), "click-soft", 0.25, "the 3D app"],
    [w("vo-04", "tram") - 0.15, "whoosh-short", 0.13, "carry to ChatGPT"],
    [cut("vo-05"), "tick-b", 0.22, "cut to the numbers"],
    [w("vo-05", "half"), "typing", 0.12, "Half the price types"],
    [w("vo-05", "terra") + 0.1, "whoosh-short", 0.12, "the tram rolls in"],
    [w("vo-05", "faster") + 0.3, "whoosh", 0.16, "the tram drives off on 'faster'"],
    [w("vo-05", "three") + 0.05, "punch", 0.3, "3x faster*"],
    [w("vo-05", "bigger"), "select", 0.15, "the asterisk note"],
    [w("vo-06", "that") + 0.3, "whoosh", 0.14, "zoom into the footnote"],
    [w("vo-06", "shown") + 0.1, "whoosh-short", 0.16, "zoom through it"],
    [w("vo-06", "shown") + 0.12, "typing", 0.12, "Shown at actual speed."],
    [w("vo-06", "some"), "typing", 0.12, "Some sections omitted."],
    [w("vo-06", "omitted") + 0.4, "scratch-b", 0.45, "pen under 'Some sections omitted.'"],
    [cut("vo-07"), "tick-a", 0.2, "Actual speed."],
    [w("vo-07", "cut"), "scratch-a", 0.5, "the slash"],
    [w("vo-07", "cut") + 0.1, "plate", 0.22, "'cut.' splits"],
    [cut("vo-08"), "whoosh-short", 0.14, "3x faster? + the write-up"],
    [w("vo-08", "three") + 0.3, "whoosh", 0.1, "zoom to the 3x sentence"],
    [w("vo-08", "three") + 0.75, "scratch-b", 0.4, "pen under 'three times faster'"],
    [w("vo-08", "own") + 0.25, "scratch-c", 0.4, "pen under 'OpenAI's claims'"],
    [w("vo-08", "no") + 0.1, "stamp-a", 0.28, "Not yet."],
    [cut("vo-09"), "impact-bass-1", 0.22, "the line"],
    [w("vo-09", "under") + 0.2, "scratch-a", 0.45, "pen under the line"],
    [sting + 0.32, "drop", 0.3, "the dot lands on the rule"],
    [sting + 0.52, "thud-wood", 0.22, "c lands"],
    [sting + 0.64, "plate", 0.18, "t lands"],
    [sting + 0.85, "pop", 0.25, "the dot becomes the e"],
    [sting + 1.3, "scratch-c", 0.45, "the pen circles the e"],
    [sting + 1.75, "typing", 0.14, "CATCH · THE · ERROR"],
]
cues.sort(key=lambda c: c[0])
(P / "scripts/sfx_cues.json").write_text(json.dumps({"cues": [[round(c[0], 3)] + c[1:] for c in cues]}, indent=1, ensure_ascii=False))
subprocess.run(["python3", str(P / "scripts/build_sfx.py")], check=True)
