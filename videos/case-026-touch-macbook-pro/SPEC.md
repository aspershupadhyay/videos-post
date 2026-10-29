# SPEC — Case 026: "Steve Jobs was wrong?" (Apple's first touchscreen Mac)

REFERENCE: Apple's "MacBook Pro with PROLED XDR Display" film (Oct 28 2026), 1:56.7, 3840×2160 AV1, 23.976 fps, music only,
           no narration; uploaded by the creator to VoiceBox Files (Videos / `MacBook.mp4`) and asked to learn its moves.
SPINE:   In 2010 Steve Jobs said a touchscreen Mac doesn't work ("your arm wants to fall off"); this week Apple shipped one,
         and its answer to his complaint is that you never have to use it: trackpad and keyboard stay, touch is extra.
TAKE:    "Jobs was right. That's why touch is optional."
LINE:    "Touch is *optional.*"
BRIEF:   the creator: "make it like a MacBook is paying us": a premium, ad-grade cut of Apple's own footage, voiced by us,
         with one CatchTheError beat (we read the whole ad for the catch: the only fine print is "Weight varies").
SCORE:   stakes 1 (a $2,899+ laptop; most viewers won't buy) · twist 2 (Jobs' own 2010 verdict vs the 2026 product) ·
         real media 2 (Apple's 4K film, its last frame) · fresh 2 (announced Oct 28 2026, out Nov 6) · spine 2 = 9/10.
OUTPUT:  HyperFrames 1080×1920, 30 fps, 41.74 s; cuts derived from assets/vo/timing.json (scripts/build_scenes.py).
LOOK:    learned from the source (rule 15): full-bleed 9:16 crops of the 4K film cut on the word; labels that live in the
         scene: pinned to a tracked surface ("Spin." on the display glass, `tools/track_plane.py`) or fixed in one slot
         while the world moves past ("In the panel.", "Trackpad ✓", "New hinge."); the ad's own bookends (the lid logo
         lighting up, the lid closing). Ours: black ground, Inter 800, the red pen #DD483F as the one accent, the paper
         cover whose printed photo grows into the film, the paper end card + logo sting. Captions on (rule 16).
VOICE:   VoiceBox `sparsh` (myvoice), one job: 17 takes (3 hooks + "3D"/"three-D" + "OLED"/"oh-led"), takes 2, temp 0.6,
         lexicon off. Server Whisper heard every line right (vo-02's 0.87 = "twenty ten" written as "2010"). Picked hook A
         (8 words), "3D" (vo-05b), "OLED" (vo-07): both pairs measured the same length. Word times: scripts/word_times.py
         (faster-whisper on CPU, because the GPU was stopped before the subs JSON was fetched).
MUSIC:   "Pamgaea" (Kevin MacLeod, CC BY 4.0) from 2 s, at −26 LUFS; dips under the re-hook (vo-08) and the fine print, lifts
         after the CTA. Mix: −14.5 LUFS integrated, LRA 2.6.
QA:      check PASS · qa_layout PASS (first run FAIL ×3: "2010" above y 240, the asterisk under the right rail and touching
         the card) · draft qa_frames PASS first time · delivery qa_frames PASS.

| Film s | Scene | Voice | Screen |
|---|---|---|---|
| 0–2.48 | s1 hook | "Steve Jobs said a touchscreen Mac doesn't work." | Frame 0 = cover ("Steve Jobs was *wrong?*"); at 0.36 s its printed photo opens into the film: a hand touching the screen (57.95 s, 0.48×). "“It doesn't work.”" |
| 2.48–5.55 | s2 | "That was twenty ten. He said your arm would fall off." | An arm reaching out to the screen (38.45 s); red italic "2010", pen under it; on "fall" the whole shot falls off its top-right corner onto… |
| 5.55–7.67 | s3 | "This week, Apple shipped one anyway." | …the lid's Apple logo lighting up (3.2 s); the quote returns and the pen strikes through "doesn't" |
| 7.67–9.88 | s4 | "The touch is built right into the screen." | A finger in Finder → pinching a 3D car; fixed label "In the panel. / Not layered on top." |
| 9.88–11.95 | s5 | "Spin a 3D model with one finger." | A finger turns the 3D model; "Spin." pinned to the display glass, riding it as the camera pulls back |
| 11.95–13.67 | s6 | "Play piano on the display." | Logic's on-screen piano in the forest, slow push |
| 13.67–17.52 | s7 | "And that screen is OLED. Two thousand nits." | Macro finger on the pixels → the red Photoshop art; "2,000 / nits · tandem OLED" |
| 17.52–19.41 | s8 re-hook | "So, what about the arm?" | The arm shot again; "The *arm?*" (music out) |
| 19.41–24.90 | s9 payoff | "Apple's answer: you never have to lift it. The trackpad stays. The keyboard stays." | The arm… then plays backwards (it goes back down) → hands on the keyboard; "Trackpad ✓" "Keyboard ✓" (red pen ticks) |
| 24.90–27.89 | s10 | "And a new hinge holds the screen steady when you tap." | A fingertip taps the bottom of the screen (0.45×); "New hinge. / Steadier when you tap." |
| 27.89–32.43 | s11 the catch | "We read the whole ad for a catch. The only fine print? Weight varies." | Four ad shots race past (drone, MagSafe, HDMI, car); Apple's own "3 pounds light" + red asterisk; the ad's last frame as a printed frame, pushed in, pen under "Weight varies" |
| 32.43–35.57 | s12 line | "Jobs was right. That's why touch is optional." | The lid closes and its logo glows (the ad's ending); "Touch is *optional.*" |
| 35.57–41.74 | s13 end | "Would you touch your laptop screen? Tell us." | Paper end card "Would you touch it?" → "Tell us below." + logo sting |

Hook variants kept for A/B (assets/vo/raw): **A (used)** "Steve Jobs said a touchscreen Mac doesn't work." ·
B "Your arm wants to fall off. That's Steve Jobs, on touchscreen Macs." · C "Apple just shipped the Mac that Steve Jobs said doesn't work."

## Facts → source (checked 2026-10-29)
- **Primary:** Apple Newsroom, "Apple unveils groundbreaking MacBook Pro with PROLED XDR Display and Touch for the first time
  on Mac" (Oct 28 2026), apple.com/newsroom/2026/10/apple-unveils-groundbreaking-macbook-pro-with-proled-xdr-display/.
  Verbatim: "the touch sensor is built directly into the display panel — not layered on top of it"; "these new ways to
  interact … work in tandem with the keyboard shortcuts and trackpad gestures pros know and love"; "a newly designed hinge
  provides greater stability while using Touch"; "up to 2000 nits peak HDR and SDR brightness"; "two self-illuminating pixel
  layers" (tandem OLED); 14-inch "now weighs half a pound less at 3 pounds"; from $2,899 (14-inch M5 Pro); pre-order Oct 28,
  available Nov 6.
- **The ad's only fine print** (last frame, 1:51–1:56): "Weight varies by configuration and manufacturing process."
- **Jobs, 2010:** Apple's "Back to the Mac" event, Oct 20 2010: "We've done tons of user testing on this, and it turns out it
  doesn't work. Touch surfaces don't want to be vertical. … after an extended period of time, your arm wants to fall off."
  (TechRadar, 9to5Mac, Ed Bott report the same quote.) Voice says "your arm would fall off" (reported speech).
- Cross-check: 9to5Mac, Macworld, MacObserver (Oct 28 2026) report the same specs and dates.
- Not claimed: "first-ever OLED Mac" style superlatives, the $400 premium over the Liquid Retina model (secondary only),
  battery life, the 16-inch's weight.
