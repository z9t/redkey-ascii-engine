# Codex build report — RedKey ASCII morph

Date: 2026-06-27
Target: `redkey-ascii-morph.html`

Constraint note: browser opening was explicitly disallowed, so verification here
is static code review plus JavaScript parse validation. Run the manual checks on
localhost: `python3 -m http.server 8745`, then open
`http://localhost:8745/redkey-ascii-morph.html`.

## 1. Offline frame-stepped render engine

Status: done.

Implemented fixed-frame transition rendering via `renderTransition()`, using
`renderFps` and `transDur` to step frames. WebM export uses WebCodecs VP8 with
explicit timestamps and a small self-contained WebM muxer. PNG frame-sequence
export uses a no-compression ZIP writer. Apply-to-video uses a selected video,
seeks frame-by-frame, and renders through the current ASCII pipeline.

What to test:
- `▶ render transition` downloads `redkey-transition.webm`.
- `PNG seq` downloads `redkey-transition-frames.zip` with expected frame count.
- `apply video` outputs a WebM approximately matching source duration.
- `video PNGs` outputs one PNG per stepped video frame.
- `?a=...&b=...&dur=...&chaos=...&ease=...&render=1` still triggers transition render.

## 2. Transition effects

Status: done.

Added `colour match`, `size pulse`, and `size↔noise` controls in `CTRL` and the
transition `GROUPS` entry. Colour match samples three luminance-band colours
from A/B and lerps them during export. Size pulse is render-time font scaling,
not `cell` rebuilding. Size-noise varies glyph font size per cell.

What to test:
- A/B with visibly different footage should shift band colours over the render.
- `size pulse` should grow then shrink around the transition midpoint.
- `size↔noise` should create per-cell size variation without grid stutter.

## 3. Text source

Status: done.

Added `text` layer mode with text value, font-family field, Local Font Access API
picker fallback, and bold toggle. Text renders into the layer source field and
uses the shared `text` transform for position and scale.

What to test:
- Select A or B, click `text`, type a word, and confirm it drives glyph density.
- Change font name or pick a local font in a supported browser.
- Toggle bold and adjust transform target `text` scale/position.

## 4. Shared transform selector

Status: done.

Added `TRANSFORMS` for `feedback`, `text`, `A`, and `B`. The `transform` group
has one slider set plus target selector. Feedback now reads the shared feedback
transform; layer manual media scaling reads A/B transforms.

What to test:
- Feedback target moves/scales feedback when `fbOpacity` is above zero.
- Text target moves/scales text source.
- A/B targets affect media only when that layer's scale mode is `manual`.
- Copy/load preset preserves transform state.

## 5. Fit / Fill / Stretch

Status: done.

Added per-layer `fitmode` with `fit`, `fill`, `stretch`, and `manual`. The mode
is handled in `fillMedia()` for image, video, and screen-backed video sources.

What to test:
- Use a non-matching-aspect image/video and switch each mode.
- Confirm `manual` responds to the selected layer transform.
- Confirm existing video/image drop and media bank still work.

## 6. Screen capture source

Status: done for browser-native capture; native bridge blocked by platform.

Added `screen` source mode through `getDisplayMedia()`. The stream is assigned
to the active layer's video path and sampled through the existing layer pipeline.
NDI/Syphon remain explicit native-bridge stubs because browsers cannot read them
directly.

What to test:
- Click `screen`, grant permission, and confirm the captured window/screen
appears as a layer source.
- Stop sharing and confirm the layer falls back cleanly.

## 7. Particle mode

Status: done as basic version.

Added `particleMode` plus gravity, wind, turbulence, attract/repel, drag, and
lifespan controls. The fixed grid remains default; particle mode swaps only the
render stage behind the existing `sampleLayer → combine → frame` architecture.

What to test:
- Set `particle mode` to 1 and confirm glyphs move.
- Adjust gravity/wind/turbulence and confirm motion changes.
- Move `attract/repel` positive/negative and confirm convergence/repulsion from
the canvas centre.

## Existing feature spot-check list

- A/B source selection, noise, image, video, eject.
- Blend B checkbox and blend modes.
- Per-slider sine/random/smooth modulation.
- Min/max slider ranges.
- Randomise, feedback, media bank LRU/remove.
- Script-to-colour chips and script randomise.
- Copy/load preset, reset, record, hide/show tuner.
- URL transition render API.

## Static verification performed

- JavaScript extracted from the HTML parsed successfully with `new Function(...)`.
- Targeted grep review checked for removed feedback-only slider references,
  transition render route, ZIP/WebM helpers, screen/text/source wiring, and reset
  default handling.

Console-clean confirmation: not confirmed at runtime because browser execution
was disallowed. The file is syntactically valid JavaScript; runtime console
cleanliness must be verified on localhost.
