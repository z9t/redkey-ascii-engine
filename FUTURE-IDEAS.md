# RedKey ASCII engine — future ideas

> SHIPPED 2026-06-27: full Codex build pass into `redkey-ascii-morph.html`.
> The file is still single self-contained HTML, keeps the RedKey red/tan/white
> defaults, and routes new controls through `CTRL`, `GROUPS`, `Layer`,
> `makeRow`, `applyPreset`, and the rAF `loop`.

## Shipped in this pass

### Offline frame-stepped render engine

Status: shipped.

- `▶ render transition` now steps a fixed number of frames from
  `transDur * renderFps` instead of waiting on real-time playback.
- WebM export uses WebCodecs VP8 frames with explicit timestamps and a small
  in-file WebM muxer.
- `PNG seq` exports a stored ZIP of PNG frames.
- `apply video` selects a source video, seeks through it frame-by-frame, applies
  the current ASCII pipeline, and exports WebM at the source duration.
- `video PNGs` exports the same apply-to-video pass as a PNG ZIP.

### Transition effect enhancements

Status: shipped.

- `colour match` samples three luminance-band representative colours from layer
  A and layer B and lerps glyph band colours across the transition.
- `size pulse` applies a render-time `sin(pi*p)` font-scale bump without
  changing `cell` or rebuilding the grid.
- `size↔noise` optionally varies per-cell glyph font size from source value.

### Text input source

Status: shipped.

- Layer A/B can use `text` as a source mode.
- The active layer has text, font-family, and bold controls.
- `fonts` uses `queryLocalFonts()` when the browser grants it; otherwise the
  font-name field is the fallback.
- Text position and X/Y scale come from the shared transform target `text`.

### Shared transform with target selector

Status: shipped.

- The transform group has one slider set for `pos X`, `pos Y`, `scale X`,
  `scale Y`.
- The target selector writes those values into separate transforms for
  `feedback`, `text`, `layer A`, and `layer B`.
- Feedback now reads the shared `feedback` transform instead of old dedicated
  feedback position/scale sliders.

### Fit / Fill / Stretch scaling modes

Status: shipped.

- Each layer has `fit`, `fill`, `stretch`, and `manual` scaling modes.
- `fit` contains, `fill` covers/crops, `stretch` distorts to the ASCII field,
  and `manual` reads the layer A/B shared transform.

### Live video input as a layer source

Status: shipped for browser-native screen/window capture; native bridge items
remain future.

- `screen` uses `navigator.mediaDevices.getDisplayMedia()` and routes the live
  stream through the same layer sampling, blend, glyph, feedback, render, and
  preview paths as video/image.
- NDI and Syphon are intentionally left as native-bridge stubs in the UI note;
  the browser cannot read them directly.

### Proper particle system

Status: shipped as a basic in-canvas particle mode.

- `particle mode` switches the renderer from fixed grid glyphs to moving glyph
  particles while preserving RedKey glyph pools, band colours, blend buffers,
  feedback, and the existing panel.
- Controls include gravity, wind, turbulence, attract/repel, drag, and lifespan.
- The attractor/repeller is currently the canvas centre; multi-point attractors,
  cursor attractors, and the larger three.js reference engine remain future
  polish.

## Future polish left

- Add browser-side validation of the generated WebM muxer across Chrome,
  Safari, and Firefox; PNG ZIP remains the compatibility fallback.
- Add a richer particle engine with multiple attractors/repellers, cursor
  targeting, source-luminance targeting, and explicit respawn modes.
- Add a local native bridge if NDI or Syphon input becomes required.
