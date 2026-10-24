#!/usr/bin/env bash
# Cut Moonshot AI's official K3.1 Pro demo videos (kimi.ai blog, Oct 23 2026) into vertical 1080x1920 shots.
# Usage: scripts/cut_footage.sh <dir with the downloaded *-1080.mp4 files>
set -euo pipefail
SRC=${1:?source dir}
OUT=$(dirname "$0")/../assets/footage
mkdir -p "$OUT"
cut() { # name source start duration crop_x
  ffmpeg -v error -y -ss "$3" -t "$4" -i "$SRC/$2-1080.mp4" -an \
    -vf "crop=608:1080:$5:0,scale=1080:1920:flags=lanczos,fps=30" \
    -c:v libx264 -preset slow -crf 16 -pix_fmt yuv420p -g 15 -movflags +faststart "$OUT/$1.mp4"
  echo "$1 $(ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUT/$1.mp4")"
}
# The walking simulator is research footage with Moonshot's version labels burned in over the figure's
# head, so it stays uncropped 16:9 (shown framed on black) instead of being cropped to vertical.
wide() { # name source start duration [keep: output seconds to keep after the black-frame drop]
  # signalstats/select drops the single black frames Moonshot left between controller versions.
  ffmpeg -v error -y -ss "$3" -t "$4" -i "$SRC/$2-1080.mp4" -an \
    -vf "fps=30,signalstats,metadata=mode=select:key=lavfi.signalstats.YAVG:value=40:function=greater,setpts=N/30/TB,scale=1080:608:flags=lanczos" \
    ${5:+-t $5} -c:v libx264 -preset slow -crf 16 -pix_fmt yuv420p -g 15 -movflags +faststart "$OUT/$1.mp4"
  echo "$1 $(ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUT/$1.mp4")"
}
wide walk-collapse  walking-sim  4.0 3.6 2.5
wide walk-stumble   walking-sim  6.85 7.45
wide walk-fixed     walking-sim 24.0 5.9

cut airport-wire    airport-rainforest   0.8  1.6 656
cut airport-render  airport-rainforest  10.6  1.8 656
cut lamp-print      modular-lamp-trimesh 15.0 1.4 656
cut lamp-lit        modular-lamp-trimesh 21.6 1.4 656
cut palace-leap     celestial-palace    21.0  1.4 656
cut palace-dragon   celestial-palace    35.0  2.0 420
