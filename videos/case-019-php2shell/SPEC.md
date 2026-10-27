# SPEC — Case 019: "AI found it in weeks. Hackers needed 45 minutes." (PHP2Shell)

STATUS:  researched + storyboarded 2026-10-27; production not started.
SPINE:   AI found a ten-year-old hole in PHP, the code behind most websites, and attacks hit within 45 minutes of
         the news, but "70% of the internet" means 70% of sites *run* PHP, not 70% are hackable: unpatched ones are.
SCORE:   stakes 2 · twist 2 · real media 1 · fresh 1 (6 days old, still being exploited) · spine 2 = 8/10.
TAKE:    AI just turned patching into a race measured in minutes.
OUTPUT:  HyperFrames 1080×1920, 30 fps, ~45 s, ≤ 120 words. Look v3 trial (STRATEGY.md §5). Cover: STRATEGY.md §5.

## Script (draft; voice 3 variants of lines 1–2 first)

| # | Time | Voice | Screen (real media first; something visible on frame 1 of every scene) |
|---|---|---|---|
| 1 | 0–2.5 | "A hole sat in the code behind most websites. For ten years." | php.net security advisory screenshot, full frame; red pen under "unauthenticated remote code execution". Frame 0 = cover. |
| 2 | 2.5–5.5 | "AI found it. Then hackers needed forty-five minutes." | Cut to Fortune / Cloudflare quote, "45 min" in Geist 800 over it. |
| 3 | 5.5–12 | "It's called PHP2Shell. Two bugs in PHP itself, the language under WordPress, Drupal and Joomla." | Wiz post header → the three CMS logos as real login screens (screenshots), quick cuts on each name. |
| 4 | 12–16 | "One request, no password, and it runs your code on their server." | Terminal-style replay of the request built from the advisory's description (no working exploit shown); *no password* in Instrument Serif Italic. |
| 5 | 16–22 | "Two teams found it separately, with AI. Wiz used Gemini and GPT. Calif used GPT." | Wiz disclosure timeline (Aug 19 → Oct 21) as the real page, push in; Calif credit in mono. |
| 6 | 22–28 | "Patches went out October 21st. Cloudflare saw tens of thousands of attacks in forty-five minutes. Millions by night." | php.net 8.5.12 release page → counter rides over a dimmed screenshot: 10,000s → millions. |
| 7 | 28–36 | "Now, the headline. 'Seventy percent of the internet.' The fine print: PHP runs 69% of sites whose language is known. Running PHP isn't the danger. *Unpatched* PHP is." | Fortune headline, red strike through "70% of the internet"; W3Techs page with 69.2% circled; *Unpatched* in italic. |
| 8 | 36–41 | "AI finds the bug in weeks. Attackers need minutes. You've got hours." | Repeatable line, big type on #FAFAFA. |
| 9 | 41–45 | "We read the fine print. Catch the Error." | End card ≥ 3 s; last frame echoes the advisory so it loops. |

On-screen numbers (max 3): **45 min**, **69.2%**, **10 years**. Patched versions (8.5.12 / 8.4.27 / 8.3.36 / 8.2.35) go in
the caption and a small mono line on scene 7, not as a red-pen number.

## Facts → source (all checked 2026-10-27)
- CVE-2026-109618 + CVE-2026-109619, unauthenticated RCE; fixed in 8.5.12, 8.4.27, 8.3.36, 8.2.35 on Oct 21 2026;
  "no complete mitigations, updating is the only safe choice" — php.net release notes + security advisory.
- Every PHP version of the last decade affected (back to 5.4); RCE shown on latest WordPress, Drupal, Joomla images;
  found with Wiz Atlas, Gemini 4 Argon, GPT-5.6 Sol; first bug Aug 19, reported Aug 24 — wiz.io/blog/php2shell-php-rce.
- Calif found the first issue Aug 1 with GPT-5.6 Sol (OpenAI Patch the Planet); AWS: "broadly exploited in the wild";
  Cloudflare CEO: tens of thousands of attempts within 45 min, hundreds of thousands in 2 h, millions by the evening
  of Oct 21 — Fortune, Oct 21 2026. **To do:** find Matthew Prince's own post for the Cloudflare numbers (primary).
- "70%": Wiz's claim, no method given. W3Techs: "PHP is used by 69.2% of all the websites whose server-side
  programming language we know" (Oct 2026).
- Careful wording: "ten years" = Wiz's "every PHP version released in the last decade". Don't say "70% of sites are
  vulnerable" or show a working exploit.

## Real media to capture (Playwright screenshots, credited in mono)
php.net advisory + 8.5.12 release page · Wiz blog header + timeline · Fortune headline · W3Techs PHP page ·
WordPress/Drupal/Joomla login screens · Cloudflare CEO post (once found).

## Hook variants to voice
A. "A hole sat in the code behind most websites. For ten years."
B. "Two AIs found the same hole in the internet. Hackers needed forty-five minutes."
C. "Seventy percent of the internet got hacked? Not quite. But it's bad."
