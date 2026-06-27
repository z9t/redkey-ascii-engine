#!/bin/bash
# make-transition.sh — glyph-dissolve transition between two scenes via the RedKey ASCII engine.
# usage: ./make-transition.sh scene1.(mp4|png) scene2.(mp4|png) [dur=1.2] [chaos=0.7] [ease=smooth]
set -e
ENGINE="$(cd "$(dirname "$0")/.." && pwd)"
S1="$1"; S2="$2"; DUR="${3:-1.2}"; CHAOS="${4:-0.7}"; EASE="${5:-smooth}"
[ -z "$S2" ] && { echo "usage: $0 scene1 scene2 [dur] [chaos] [ease]"; exit 1; }

# 1. boundary frames INTO the engine folder (same-origin for the canvas)
frame() { case "$1" in *.png|*.jpg|*.jpeg) cp "$1" "$2";; *) shift 2; esac; }
case "$S1" in *.png|*.jpg|*.jpeg) cp "$S1" "$ENGINE/s1-last.png";; *) ffmpeg -y -sseof -0.1 -i "$S1" -frames:v 1 "$ENGINE/s1-last.png";; esac
case "$S2" in *.png|*.jpg|*.jpeg) cp "$S2" "$ENGINE/s2-first.png";; *) ffmpeg -y -i "$S2" -frames:v 1 "$ENGINE/s2-first.png";; esac

# 2. ensure the local server (engine needs http://, not file://)
pgrep -f "http.server 8745" >/dev/null || ( cd "$ENGINE" && python3 -m http.server 8745 >/dev/null 2>&1 & )
sleep 1

# 3. auto-render the dissolve → downloads ~/Downloads/redkey-transition.webm
URL="http://localhost:8745/redkey-ascii-morph.html?a=s1-last.png&b=s2-first.png&dur=$DUR&chaos=$CHAOS&ease=$EASE&render=1"
echo "rendering ${DUR}s glyph dissolve (chaos=$CHAOS, ease=$EASE)…"
open "$URL"

echo
echo "→ WebM will save to ~/Downloads/redkey-transition.webm (real-time, ~${DUR}s + a moment)"
echo "→ then splice between the scenes:"
echo "   ffmpeg -y -i ~/Downloads/redkey-transition.webm -c:v libx264 -pix_fmt yuv420p trans.mp4"
echo "   ffmpeg -y -i \"$S1\" -i trans.mp4 -i \"$S2\" -filter_complex \"[0:v][1:v][2:v]concat=n=3:v=1[v]\" -map \"[v]\" reel.mp4"
