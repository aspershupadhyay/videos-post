#!/usr/bin/env bash
# Cut OpenAI's GPT-6.1 Terra launch film (assets/footage/source.mp4, 1920x1080 @ 24 fps, 31.5 s) into the shots we use.
# Clips stay 16:9 at source resolution (the HTML frames them as cards) except the earth zoom, cropped to 9:16.
set -euo pipefail
cd "$(dirname "$0")/.."
SRC=assets/footage/source.mp4
enc="-an -c:v libx264 -preset slow -crf 16 -pix_fmt yuv420p -g 15 -movflags +faststart"
cut() { # name start duration speed [extra-vf]
  ffmpeg -v error -y -ss "$2" -t "$3" -i "$SRC" -vf "setpts=PTS/$4,fps=30${5:+,$5}" $enc "assets/footage/$1.mp4"
  echo "$1 $(ffprobe -v error -show_entries format=duration -of csv=p=0 assets/footage/$1.mp4)"
}
cut toy     23.85 0.60 0.4                                  # hand sets the die-cast tram down (slowed 2x)
cut photo    9.00 3.25 1.6                                  # the Lisbon photo + the prompt being typed (sped 1.6x)
cut earth    1.80 4.15 0.82 "crop=608:1080:656:0,scale=1080:1920:flags=lanczos"  # earth -> Lisbon zoom, 9:16
cut build   12.30 4.90 1                                    # the 3D app building the tram ("Shown at actual speed. Some sections omitted.")
cut app     17.50 3.50 1                                    # the finished model in ChatGPT
cut toytall 23.85 0.60 0.4 "crop=608:1080:700:0,scale=1080:1920:flags=lanczos"  # the toy, 9:16 full-bleed
ffmpeg -v error -y -ss 22.9 -i "$SRC" -frames:v 1 -vf "crop=340:340:790:370" assets/shots/tram-cutout.png
ffmpeg -v error -y -ss 15.0 -i "$SRC" -frames:v 1 assets/shots/footnote-frame.png
# first/last frames: a still sits under every clip so a clip ending early never shows ground
for c in toy toytall photo earth build app; do ffmpeg -v error -y -sseof -0.1 -i assets/footage/$c.mp4 -frames:v 1 -update 1 assets/shots/$c-end.png; done
ffmpeg -v error -y -i assets/footage/toy.mp4 -frames:v 1 assets/shots/toy-start.png
ffmpeg -v error -y -i assets/footage/build.mp4 -frames:v 1 assets/shots/build-start.png
echo stills done
