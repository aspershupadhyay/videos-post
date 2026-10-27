# Editing taste — how CatchTheError cuts (v1, 2026-10-27)

Research-backed rules for short vertical fact-checks. Pair with `VISUALS.md` (what's on screen) and `STRATEGY.md` (story).

## 1. What a cut has to earn (Walter Murch, *In the Blink of an Eye*)
Murch's "Rule of Six" weighs a cut: **emotion 51% · story 23% · rhythm 10% · eye-trace 7% · 2D plane 5% · 3D space 4%**.
If you must sacrifice one, give up the lower ones first. For us: a cut that lands the surprise (emotion) beats a cut
that's tidy. Never sacrifice "does the viewer feel the catch?" for a pretty transition.

## 2. Our cutting rules
1. **Cut on the voice.** Every cut lands on a stressed word or the breath before it (we get phrase onsets from
   `prep_audio.py`). Never cut mid-word.
2. **Vary shot length.** Runs of 0.8–1.5 s shots, then one 3–4 s hold on the evidence. Same-length shots feel generated.
3. **J and L cuts.** Let the next line start 0.2–0.4 s before its picture (J), or let a sound tail over the cut (L).
   This is the difference between "slideshow" and "edit".
4. **Eye-trace in 9:16.** Keep the thing that matters in the middle third (y 640–1280) across consecutive shots so the eye
   never hunts. The red pen lands where the eye already is.
5. **Freeze → annotate → release.** Our signature move: stop the real footage, mark it, then let it play again.
6. **Silence is a cut.** Drop the music 0.3–0.5 s before the twist line; bring it back on the next beat.
7. **One motion per shot.** A push *or* a pan *or* a pen stroke — not all three.
8. **Hold the payoff.** The verdict frame stays ≥ 1.5 s after the last word lands, so it can be screenshotted.
9. **Physical > typed.** Real pages, real UI, real scroll recordings, real paper. Text we add is the minimum that
   carries the line (Casey Neistat-style text-on-real-things beats animated text cards).
10. **Re-watch the middle.** 25–40 s is where retention dies; if two consecutive shots are stills, replace one with motion.

## 3. Sound
Voice −14 LUFS, bed −26 LUFS under it, +5 dB after the last word. One sound per visible event (pen = scratch, callout
= tick, cut = short whoosh at most). No riser into every scene. Measure, don't trust ears alone.

## 4. Type & logo (v2 proposal — see `brand/lookbook/type-sheet.jpg`, `logo-sheet.jpg`)
**Why change:** Geist + Instrument Serif is the default pairing of AI-startup websites (a 2026 "design slop" round-up
lists both), so our videos read as "AI product" before a word is heard.
**Recommended — "Newsroom":** Schibsted Grotesk 800 (commissioned by the Schibsted media group, Bakken & Bæck) for
headlines · Newsreader Italic (Production Type, built for on-screen news reading) for the one word that matters and
quotes · IBM Plex Mono 500 for labels and credits. All OFL; files in `brand/fonts/`.
Alternative — "Broadsheet": Archivo 800 at 68% width · Source Serif 4 Italic · JetBrains Mono (denser, more tabloid).
**Logo concepts:** 1 Circled (wordmark with our red-pen circle on "Error"; avatar = E in a hand-drawn ring) ·
2 Brackets ([sic], the editor's mark for an error in a quote; avatar = [sic]) · 3 Struck (Error crossed out).
Status: **awaiting the creator's pick**; until then videos keep v3 type.
