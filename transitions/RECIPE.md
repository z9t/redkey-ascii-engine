# RedKey ASCII — Scene Transition Recipe

Make a **glyph-storm dissolve** between two scenes (instead of a hard cut), using the RedKey ASCII engine.
Output is a WebM you splice between the clips. Skill: `redkey-ascii-engine` (`get_skill redkey-ascii-engine`).

## TL;DR
```bash
# from this folder:
./make-transition.sh scene1.mp4 scene2.mp4 1.2 0.7
# → renders ~/Downloads/redkey-transition.webm, then prints the splice command
```

## How it works
- **Layer A = start frame** (last frame of Scene 1), **Layer B = end frame** (first frame of Scene 2).
- The engine eases the **blend 0→1** over `duration`, with a **chaos surge at the midpoint** so it dissolves
  through a multi-script glyph storm in RedKey colours, then resolves into Scene 2.

## Manual steps
```bash
ENGINE=/Users/max/Documents/redkey/ascii-foreign-scripts
# 1. boundary frames INTO the engine folder (must be same-origin for the canvas)
ffmpeg -y -sseof -0.1 -i scene1.mp4 -frames:v 1 "$ENGINE/s1-last.png"
ffmpeg -y -i scene2.mp4 -frames:v 1 "$ENGINE/s2-first.png"
# 2. make sure the local server is up (engine needs http://, not file://)
pgrep -f "http.server 8745" >/dev/null || (cd "$ENGINE" && python3 -m http.server 8745 >/dev/null 2>&1 &)
# 3. auto-render the dissolve (downloads ~/Downloads/redkey-transition.webm)
open "http://localhost:8745/redkey-ascii-morph.html?a=s1-last.png&b=s2-first.png&dur=1.2&chaos=0.7&ease=smooth&render=1"
# 4. splice it between the clips
ffmpeg -y -i ~/Downloads/redkey-transition.webm -c:v libx264 -pix_fmt yuv420p trans.mp4
ffmpeg -y -i scene1.mp4 -i trans.mp4 -i scene2.mp4 -filter_complex "[0:v][1:v][2:v]concat=n=3:v=1[v]" -map "[v]" reel.mp4
```

## URL render API
`?a=<imgA>&b=<imgB>&dur=<sec>&chaos=<0–1.5>&ease=<smooth|linear|in|out>&preset=<inline-json|url>&render=1`
- Images must live **inside the engine folder** (same-origin, or the canvas taints).
- `preset` applies a saved look (from the panel's **copy preset**).
- Headless: drive the same URL with Playwright/puppeteer and allow downloads.

## Making the dissolve "the best"
- **Short** (1–1.5 s) — a transition, not a scene.
- **chaos 0.6–0.8** — a glyph-storm peak in the middle that resolves cleanly.
- **ease=smooth**. Match the energy of the cut.
- **Text-scene reels** (e.g. "DON'T BUILD ON…"): render the text *as frames* and feed them as A/B, so the
  words themselves dissolve through glyphs. Add **feedback** (in a preset) for trails/tunnel on punchy cuts.
- Keep the three RedKey tones (red #dc2626 / tan #b8aa98 / white #fafafa) unless matching a scene palette.

## Coming soon (FUTURE-IDEAS.md)
Colour-match (bands adopt Scene A's palette → Scene B's), mid-point glyph-size pulse, and size↔noise organic
variance — all to make the dissolve adapt to the footage.
