#!/bin/bash
# Reconstruit le showreel : images 4K (Chromium) + bande-son (numpy) + encodage (ffmpeg).
# Prérequis : node + playwright, python3 + numpy, ffmpeg, polices Inter / Inter Display / JetBrains Mono.
set -e
cd "$(dirname "$0")"; TMP=${TMP_DIR:-/tmp/showreel_4k}; mkdir -p "$TMP"
for w in 0 1 2 3; do node render.js "$TMP/frames" $w 4 & done; wait
python3 music.py "$TMP/music.wav"
ffmpeg -v error -y -framerate 60 -i "$TMP/frames/f_%05d.jpg" -i "$TMP/music.wav" -vf format=yuv420p \
  -c:v libx264 -preset slow -crf 22 -maxrate 32M -bufsize 64M -profile:v high -level 5.2 -g 120 -aq-mode 3 \
  -color_primaries bt709 -color_trc bt709 -colorspace bt709 -c:a aac -b:a 256k -movflags +faststart -shortest ../showreel_4k_2160p60.mp4
