#!/usr/bin/env bash
# Cut the viral clip (as posted on X by @CodeByPoonam; original maker unknown) into the shots we review.
set -euo pipefail
cd "$(dirname "$0")/.."
SRC=assets/footage/source.mp4
cut() { # name start duration
  ffmpeg -v error -y -ss "$2" -t "$3" -i "$SRC" -an -vf "scale=1080:1920:flags=lanczos,fps=30" \
    -c:v libx264 -preset slow -crf 17 -pix_fmt yuv420p -g 15 -movflags +faststart "assets/footage/$1.mp4"
  echo "$1 $(ffprobe -v error -show_entries format=duration -of csv=p=0 assets/footage/$1.mp4)"
}
still() { ffmpeg -v error -y -ss "$2" -i "$SRC" -frames:v 1 -vf "scale=1080:1920:flags=lanczos" "assets/shots/$1.png"; echo "$1"; }
cut hook    0.8  7.6    # boxes, footprints, red "reject" tags
cut drop   18.6  3.2    # WONDERFUL, the drop counter 133 -> >300, DANGER
cut walk   30.0  2.8    # for the side-by-side
still wonderful 20.75
