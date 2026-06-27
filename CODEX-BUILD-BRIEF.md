# Codex build brief — RedKey ASCII engine: implement FUTURE-IDEAS

**Target file:** `/Users/max/Documents/redkey/ascii-foreign-scripts/redkey-ascii-morph.html` (single self-contained HTML; vanilla JS canvas; no build step).
**Test:** serve over http (NOT file://) — `cd <folder> && python3 -m http.server 8745` → open `http://localhost:8745/redkey-ascii-morph.html`. The canvas taints under file://, so always test on localhost.
**Spec source:** implement every item in `FUTURE-IDEAS.md` (read it fully). This brief adds priority, constraints, and acceptance criteria.

## HARD CONSTRAINTS
- **Do NOT break any existing feature.** Existing: two source Layers A/B (noise/video/image) + blend modes; per-slider motion (∿ sine / ◇ random / ~ smooth between each row's min↔max); settable min/max; 🎲 randomise; feedback layer; media bank (2×5, LRU, remove); script→colour chips + randomise; accordion groups; draggable + minimisable panel; copy/load preset; ● record; transition render (`▶ render transition`) + the `?a&b&dur&chaos&ease&render=1` URL API.
- **Match the existing architecture/style:** the `CTRL` object (each control `{v,min,max,step,l, mSine,mRand,mSmooth}`), `GROUPS` accordions, `makeRow`, the Layer objects `LA/LB`, `applyPreset`, the rAF `loop`. New controls go in `CTRL` + a `GROUPS` entry; new sources extend the Layer system; keep everything keyboard-light and self-contained.
- **Preserve the RedKey palette** (red #dc2626 / tan #b8aa98 / white #fafafa) as defaults.
- Keep it a single HTML file, no external deps (except the existing CDN-free approach). Performance: must stay smooth at ~1080p.
- Update `FUTURE-IDEAS.md` to mark each item shipped as you complete it. Append a one-line `~/know/recent-work/2026-06` entry.

## BUILD ORDER (priority)
1. **Offline frame-stepped render engine** — the keystone (unlocks 3 things). Render deterministically by stepping frames (fixed dt), not real-time: for an N-second clip at F fps, advance the sim by 1/F each step, draw, capture the frame; encode to WebM (and offer a PNG/ZIP frame-sequence option). Then route BOTH:
   - **transition mode** → render the A→B dissolve frame-stepped (faster-than-realtime), and
   - **apply-ASCII-to-video** → select a video, step every source frame through the current settings, output the full ASCII-ified clip at source length.
2. **Transition effect enhancements** (improve the dissolve): **colour-match A→B** (sample ~3 representative colours from frame A and ~3 from frame B; lerp the band colours A→B across the transition); **mid-point glyph-size pulse** (`sin(π·p)` size bump at the halfway point, via render-time font scale — NOT by changing `cell`/rebuilding the grid); **size↔noise** optional toggle (drive per-cell glyph size from the noise/source value).
3. **Text input source** — a 4th layer source mode: type text → render as the source field; **system font picker** (Local Font Access API `queryLocalFonts()` w/ permission, else a font-name field), **scale** + **bold** (no italics).
4. **Shared transform + target selector** — one set of XY-position + X/Y-scale sliders with a target dropdown (**feedback / text / layer A / layer B**); replaces the feedback-only fb-pos/scale sliders; each consumer reads its own `{x,y,sx,sy}`.
5. **Fit / Fill / Stretch (+ manual)** scaling modes per layer for video/images (contain / cover / distort / manual-transform) — in `fillMedia()`.
6. **Live sources** — screen/window capture via `getDisplayMedia()` as a layer source (browser-native, do this). NDI / Syphon need a native bridge — leave a clearly-marked stub + note, do NOT attempt the native side.
7. **Particle-system mode** — biggest/last. Optional render mode that promotes glyphs from the fixed grid to moving particles with velocity, gravity, wind, turbulence, attractors/repellers (converge/repel), drag, lifespan. Reference engine: `/Users/max/Documents/projects/sites/z9t.me/z9t-root-rend-preview/app.js` (three.js particles + attractors/faults/forces). Keep the RedKey glyphs + colour bands + this control panel; swap the grid renderer for a particle renderer behind a mode toggle. If time-boxed, ship a basic version (gravity + wind + one attractor/repeller) and note what's left.

## ACCEPTANCE CRITERIA (the gate checks these)
For EACH item: (a) it works on localhost without console errors, (b) it did not break any pre-existing feature (spot-check: blend, motion, feedback, bank, transition URL API still work), (c) it follows the CTRL/GROUPS/Layer architecture, (d) RedKey defaults preserved.
- Offline render: produces a WebM whose duration ≈ requested and is NOT gated by real-time playback; apply-to-video outputs a clip ≈ source length; frame-sequence option produces N frames.
- Colour-match: the band colours visibly shift from A's palette to B's over a transition.
- Size pulse: glyphs grow then shrink across the transition WITHOUT a grid rebuild stutter.
- Text source: renders a typed word in a chosen system font, bold + scale work.
- Shared transform: one XY/scale set drives the selected target (feedback/text/A/B).
- Fit/Fill/Stretch: each mode visibly changes how a non-matching-aspect image/video maps to the frame.
- Screen capture: a window/screen stream appears as a live layer source.
- Particle mode: glyphs move under gravity/wind and converge/repel toward/from a point (basic acceptable, note gaps).

## DELIVERABLE
Edit `redkey-ascii-morph.html` in place. When done, write `CODEX-BUILD-REPORT.md` in this folder: per-item status (done/partial/blocked), what to test, any deviations, and console-clean confirmation. The gate (independent reviewer) will verify against the ACCEPTANCE CRITERIA before this is accepted as complete.
