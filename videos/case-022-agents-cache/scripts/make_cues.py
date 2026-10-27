"""Write scripts/sfx_cues.json from the voice timings (so a re-voiced line moves its SFX too), then run build_sfx.py.
Each cue: [film time the picture lands, sfx file, volume, label]. Takes rotate (scratch-a/b/c, tick-a/b, stamp-a/b/c).
Cues past the film's end (the --demo cut) are dropped."""
import json
import re
import subprocess
from pathlib import Path

P = Path(__file__).resolve().parent.parent
FILM = float(re.search(r'data-composition-id="main" data-start="0" data-duration="([\d.]+)"', (P / "index.html").read_text()).group(1))
T = json.loads((P / "assets/vo/timing.json").read_text())
L = {l["id"]: l for l in T["lines"]}
cut = lambda vid: round(L[vid]["start"] - 0.2, 2)


def w(vid, word, n=1):
    return [s for ww, s, e in L[vid]["words"] if re.sub(r"[^\w]", "", ww).lower() == word][n - 1]


cues = [
    [0.32, "whoosh", 0.16, "the cover lifts off"],
    [w("vo-01", "sealed"), "click-soft", 0.3, "box A locks"],
    [w("vo-01", "sealed") + 0.1, "select", 0.2, "box B locks"],
    [w("vo-01", "sealed") + 0.7, "impact-bass-2", 0.25, "the wall slams down"],
    [w("vo-01", "still"), "pop", 0.2, "the red dot appears"],
    [w("vo-01", "secret") - 0.35, "whoosh-short", 0.14, "the dot hops the wall"],
    [w("vo-01", "secret") + 0.25, "drop", 0.3, "the dot lands in B"],
    [cut("vo-02") + 0.05, "plate", 0.18, "headline 1"],
    [cut("vo-02") + 0.6, "thud-wood", 0.18, "headline 2"],
    [cut("vo-02") + 1.15, "plate", 0.15, "headline 3"],
    [w("vo-02", "read") - 0.2, "whoosh", 0.14, "headlines fly off"],
    [w("vo-02", "read") + 0.15, "thud-wood", 0.2, "the report lands"],
    [w("vo-02", "scary"), "scratch-b", 0.35, "the title is redacted"],
    [cut("vo-03"), "whoosh-short", 0.12, "the boxes shrink up"],
    [w("vo-03", "both") + 0.1, "impact-bass-1", 0.2, "the chip rises"],
    [w("vo-03", "share"), "scratch-a", 0.3, "wires draw"],
    [w("vo-03", "processor"), "typing", 0.1, "the cache lights up"],
    [cut("vo-04"), "whoosh", 0.12, "zoom into the cache"],
    [w("vo-04", "kicks") + 0.1, "tick-a", 0.3, "evict 1"],
    [w("vo-04", "kicks") + 0.22, "tick-b", 0.3, "evict 2"],
    [w("vo-04", "kicks") + 0.34, "tick-a", 0.3, "evict 3"],
    [w("vo-04", "times") + 0.1, "select", 0.2, "the probe appears"],
    [w("vo-04", "fast"), "key-press", 0.3, "fast"],
    [w("vo-04", "slow"), "click-soft", 0.35, "slow"],
    [w("vo-04", "fast", 2), "key-press", 0.3, "fast"],
    [w("vo-04", "message") - 0.3, "typing", 0.14, "the bits drop in"],
    [w("vo-04", "message"), "pop", 0.25, "B gets the secret"],
    [cut("vo-05"), "thud-wood", 0.2, "the coverage card lands"],
    [w("vo-05", "told"), "scratch-c", 0.4, "pen under 'asked to exchange'"],
    [w("vo-05", "test") + 0.1, "scratch-a", 0.35, "pen under 'test.'"],
]
cues = sorted([c for c in cues if c[0] < FILM - 0.1], key=lambda c: c[0])
(P / "scripts/sfx_cues.json").write_text(json.dumps({"cues": [[round(c[0], 3)] + c[1:] for c in cues]}, indent=1, ensure_ascii=False))
subprocess.run(["python3", str(P / "scripts/build_sfx.py")], check=True)
