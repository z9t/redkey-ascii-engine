---
name: redkey-ascii-engine
description: "Use when generating RedKey multi-script ASCII/glyph visuals, scene transitions, or applying the glyph effect to footage for a reel/video — e.g. dissolving one scene into the next instead of a hard cut. Drives the local redkey-ascii-morph.html engine: real glyphs from 20 world scripts in the RedKey palette (red #dc2626 / tan #b8aa98 / white #fafafa), two source layers A/B with blend, noise/motion/feedback, and a transition render that outputs WebM."
version: 1.0.0
license: MIT
metadata:
  tags: [redkey, ascii, glyph, video, reel, transition, motion-graphics]
  category: creative
---

# RedKey ASCII Engine

A browser-based, multi-script **ASCII/glyph visual engine** for RedKey. Use it to make scene **transitions**
(glyph-storm dissolves between clips), animated glyph backdrops, logo reveals, or to apply the RedKey glyph
look to footage. Output is WebM you can splice into a reel.

**Tool:** `/Users/max/Documents/redkey/ascii-foreign-scripts/redkey-ascii-morph.html`

## When to use
- A reel needs a designed transition between scenes (e.g. "Scene 1 dissolves into Scene 2" with no hard
  cut/STOP) → render a glyph dissolve and splice it between the clips.
- You want a RedKey multi-script glyph background, logo reveal, or to ASCII-ify a clip.

## Launch (REQUIRED — must be over http, not file://)
`file://` taints the canvas so frame-sampling breaks. Serve over localhost:
```bash
cd /Users/max/Documents/redkey/ascii-foreign-scripts
pgrep -f "http.server 8745" >/dev/null || (python3 -m http.server 8745 >/dev/null 2>&1 &)
# engine: http://localhost:8745/redkey-ascii-morph.html   (or double-click serve.command)
```

## Agent quick path — headless transition render (URL API)
The engine auto-renders a transition from URL params and downloads the WebM. Input images must sit **inside
the engine folder** (so they're same-origin and don't taint the canvas).
```
http://localhost:8745/redkey-ascii-morph.html?a=<imgA>&b=<imgB>&dur=<sec>&chaos=<0-1.5>&ease=<smooth|linear|in|out>&render=1
```
- `a` = Layer A = **start frame**, `b` = Layer B = **end frame** (filenames relative to the folder).
- `dur` = transition seconds, `chaos` = mid-point glyph turbulence surge, `render=1` = auto-run + download.
- `preset=<inline-json|url>` optionally applies a saved look (from the panel's **copy preset**).
Open it with `open "<url>"` (macOS) — the browser loads, renders in real-time, and drops
`~/Downloads/redkey-transition.webm`. For fully headless, drive the same URL with a headless browser
(Playwright/puppeteer) and allow downloads.

## Recipe: dissolve Scene 1 → Scene 2 (the reel case)
```bash
D=/Users/max/Documents/redkey/ascii-foreign-scripts
# 1. grab the last frame of scene 1 and the first frame of scene 2
ffmpeg -sseof -0.1 -i scene1.mp4 -frames:v 1 "$D/s1-last.png"
ffmpeg -i scene2.mp4 -frames:v 1 "$D/s2-first.png"
# 2. render the glyph dissolve (short + punchy reads best for a cut: ~1–1.5s, chaos ~0.6–0.8)
open "http://localhost:8745/redkey-ascii-morph.html?a=s1-last.png&b=s2-first.png&dur=1.2&chaos=0.7&render=1"
# 3. (after it saves ~/Downloads/redkey-transition.webm) splice between the clips
ffmpeg -i redkey-transition.webm -c:v libx264 -pix_fmt yuv420p trans.mp4
ffmpeg -i scene1.mp4 -i trans.mp4 -i scene2.mp4 -filter_complex "[0:v][1:v][2:v]concat=n=3:v=1[v]" -map "[v]" reel.mp4
```
**Making the dissolve "the best":** keep it short (1–1.5 s) so it's a transition not a scene; `chaos` 0.6–0.8
gives a glyph-storm peak in the middle then resolves; `ease=smooth`; match the energy of the cut. For a
text-scene reel (e.g. "DON'T BUILD ON…"), feed the rendered text frames as A/B so the words themselves
dissolve through glyphs. Add **feedback** (in the preset) for trails/tunnel on punchier cuts.

## Manual / interactive use (to design a look, then save a preset)
Open the engine, drag in (or load) sources per layer, tune in the panel, then **copy preset** → reuse via
`?preset=`. Key controls: noise types (fbm/warp/ridged/cellular/waves/static, real **noise scale**), Layer
**A/B blend** (mix/multiply/screen/add/max/min/difference), **per-slider motion** (∿ sine / ◇ random / ~
smooth, each between that row's min↔max), **feedback** (opacity + scale X/Y + pos X/Y = trails/tunnel),
colour pickers (the three RedKey tones), script→colour assignment, and **● record** for live capture.

## Pitfalls
- MUST run over `http://localhost`, never `file://` (canvas taint breaks video/frame sampling).
- Input images for the URL API must be **inside the engine folder** (same-origin), else the canvas taints.
- Transition render v1 is **real-time** (a 5 s transition takes 5 s). Frame-stepped faster-than-realtime
  render (also gives apply-ASCII-to-full-video + PNG sequences) is the queued next build (`FUTURE-IDEAS.md`).
- The WebM lands in `~/Downloads/` as `redkey-transition.webm`.

## Files
- Engine: `…/ascii-foreign-scripts/redkey-ascii-morph.html` · relaunch: `serve.command`
- Docs: `…/ascii-foreign-scripts/HOWTO.md`, `FUTURE-IDEAS.md`
- RedKey palette source: `~/Documents/redkey/redkey-claude-design-pack-2026-06-26/designlang/redkey.au/`
