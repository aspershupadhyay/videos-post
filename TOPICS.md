# Topic bank

Scored with `STRATEGY.md` §1 (stakes, twist, real media, freshness, spine; 0–2 each). Leads from news roundups are
**unverified** until checked against the primary source; re-score and prune every session.
Last refresh: 2026-10-28 (Case 023 added; M6 iMac "5× vs M4" and the 11× graphics claim noted as follow-ups).

| Score | Topic | Spine (draft) | Primary source to verify | Status |
|---|---|---|---|---|
| 10 | **Apple M6 MacBook Pro: "13× faster at A.I."** | Against a 2020 M1; vs last year's M5 it's 1.3×; and it's time to first token. | Apple Newsroom Oct 27 2026 footnote 3 + the ad's last frame (verified) | **Case 023, delivered** |
| 7 | **"Up to 11× faster graphics" (same ad)** | Blender ray tracing vs an M1, a chip with no hardware ray tracing. | Apple Newsroom (verified); Apple M3 launch for hardware RT | in Case 023's caption; a short on its own? |
| 8 | **Mixture of Experts explained (Llama 4 Maverick)** | Zuckerberg's AI uses 17B of 400B per token; all 400B still sit in memory; the "experts" sort by syntax, not topic. | Meta Llama 4 blog; Mixtral arXiv 2401.04088 (verified) | **Case 024, carousel delivered** |
| 9 | **OpenAI agents: CPU-cache channel (a test) + the DNS breakout (not)** | They were told to talk through the cache; the real escape was a model using DNS, and the auto-stop failed for 2.5 h. | alignment.openai.com DNS report (verified); OfficeChai/VGTimes for the cache test | **Case 022, delivered** |
| 9 | **OpenAI's agents weakened their own monitors** | OpenAI's coding agents switched off the systems watching them, and one denied it, but OpenAI rated neither top severity. | OpenAI's Oct 20 2026 post (CNBC blocks fetch; find OpenAI's own) | partly verified via TechXplore/CNBC; next up |
| 8 | **PHP2Shell**: AI found a 10-year-old hole; attacks in 45 min | See spine in the spec. | php.net, wiz.io, W3Techs, Fortune (verified) | **Case 019, storyboarded** `videos/case-019-php2shell/SPEC.md` |
| 8 | **AI agents "ace" benchmarks by exploiting loopholes** | A 10-line file makes every SWE-bench Verified test pass; 100% on Terminal-Bench with a fake curl. | rdi.berkeley.edu/blog/trustworthy-benchmarks; arXiv 2605.12673 | from Apr 2026, evergreen; series opener |
| 8 | **Ads arrive in ChatGPT's image generator** | Free ChatGPT now puts ads where you make images. Here's what they look like. | OpenAI announcement + real screenshots | verify |
| 7 | **"Block a model if it could kill 50+ people"**: Anthropic's bill proposal | An AI company is asking to be regulated, and here's the number in the fine print. | the bill text | verify; careful framing |
| 9 | **GPT-6.1 Terra launch: "Shown at actual speed. Some sections omitted."** | Half price, 3× faster (OpenAI's own), the demo footnote. | OpenAI film; BleepingComputer; dev.to; Simon Willison | **Case 021, delivered** |
| 9 | **Viral cliff "AI" HUD clip** (568K views on X) | Readout claims 300 m; Apple LiDAR reaches 5 m; no source named; real slope AI is cameras + drones. | Apple Newsroom; Sci. Rep. 2026; Nat. Commun. 2025 | **Case 020, delivered** |
| 7 | **Viral-claim check series** ("the headline vs the paper") | One viral AI headline per week, checked against its source in 40 s. | per episode | format; repeatable |

## Series ideas (consistency builds followers)
- **"Worth hearing"** (insight clips, Case 025): one expert's sharp argument from a real debate, uncut, with our
  cover + captions. Track its 3-s hold against the fact-checks before making it a series.
- **"Benchmark fine print"**: who ran the test, on what, and what got left out. One chart per episode.
- **"Read the terms"**: what free AI products do with your data, your images or your ads.
- **"Patch this now"**: AI-found security bugs that affect ordinary people's sites and apps.

Sources for the 2026-10-27 leads: onei.ai AI Weekly #13 (Oct 19–25), dev.to "Top 5 AI news this week (Oct 2026)",
MarketingProfs AI Update Oct 9, letsdatascience.com / Crypto Briefing on the Berkeley benchmark study.
