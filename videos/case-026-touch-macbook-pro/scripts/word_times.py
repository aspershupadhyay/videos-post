"""Word times for each voice line on the CPU (faster-whisper small.en), when VoiceBox's own subs JSON isn't at hand.

    python3 scripts/word_times.py

Writes assets/vo/raw/subs/<id>.subs.json as {"words": [{"w", "s", "e"}]}, the same shape VoiceBox's Whisper gives,
so prep_audio.py reads either. The script text is the prompt, so the spelling follows the script.
"""
import json
import subprocess
from pathlib import Path

import numpy as np

from faster_whisper import WhisperModel

P = Path(__file__).resolve().parent.parent
RAW = P / "assets/vo/raw"
SCRIPT = json.loads((P / "scripts/script.json").read_text())


def pcm(f):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(f), "-ac", "1", "-ar", "16000", "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32)


model = WhisperModel("small.en", device="cpu", compute_type="int8")
for vid, text in SCRIPT.items():
    segs, _ = model.transcribe(pcm(RAW / f"{vid}.wav"), word_timestamps=True, initial_prompt=text, beam_size=5)
    words = [{"w": w.word.strip(), "s": round(w.start, 3), "e": round(w.end, 3)} for s in segs for w in s.words]
    (RAW / f"subs/{vid}.subs.json").write_text(json.dumps({"text": text, "words": words}))
    print(vid, " ".join(w["w"] for w in words))
