# videos-post — CatchTheError

| Path | What |
| --- | --- |
| `PLAYBOOK.md` | How a CatchTheError video is researched, scripted, voiced, mixed and animated |
| `brand/` | Logo 2.0: mark, avatars (paper / rust / teal), lockups, wordmark — `python3 brand/build_logo.py` |
| `videos/case-017-artcraft/` | Case 017 "Someone cloned Adobe in a week?" — 1080×1920, 69.7 s |
| `.claude/skills/` | HyperFrames agent skills (hyperframes, hyperframes-cli, hyperframes-registry, media-use) |

```bash
cd videos/case-017-artcraft
npx hyperframes@0.8.192 preview      # edit in the Studio
npx hyperframes@0.8.192 check
npx hyperframes@0.8.192 render -q delivery -o renders/case-017-artcraft-9x16.mp4
```
