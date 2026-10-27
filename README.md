# videos-post — CatchTheError

| Path | What |
| --- | --- |
| `PLAYBOOK.md` | How a CatchTheError video is researched, scripted, voiced, mixed and animated |
| `brand/` | Logo v3 "ct(e)": layers, paper ground, end-card sting, motion library — see `brand/README.md` |
| `videos/case-021-gpt-6-1-terra/` | Case 021 GPT-6.1 Terra — look v4 "paper", 1080×1920, 50.4 s (current template) |
| `videos/case-017-artcraft/` | Case 017 "Someone cloned Adobe in a week?" — 1080×1920, 69.7 s |
| `.claude/skills/` | HyperFrames agent skills (hyperframes, hyperframes-cli, hyperframes-registry, media-use) |

```bash
cd videos/case-017-artcraft
npx hyperframes@0.8.192 preview      # edit in the Studio
npx hyperframes@0.8.192 check
npx hyperframes@0.8.192 render -q delivery -o renders/case-017-artcraft-9x16.mp4
```
