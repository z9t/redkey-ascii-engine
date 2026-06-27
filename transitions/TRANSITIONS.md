# RedKey content-aware scene-dissolve transitions

> **Credit:** the content-aware dissolve approach below was developed by the
> **RedKey-transitions Claude session**. The canonical, unified tool (one engine
> with **mode + tendency sliders**) is being built by that session and will land
> here when it stabilises. This note captures the *ideas* so the rest of us can
> use and reason about them; it does not vendor the in-flight prototype files.

## Why content-aware

A plain noise-threshold dissolve ignores the picture. These transitions **read the
frame** and reveal it intelligently: the background "mass" goes first and the
dissolve **tendrils into the subject**, following its edges — so the cut feels
related to the piece instead of cutting across it. A **glyph burn-front** (RedKey
red `#dc2626` / tan `#b8aa98` / white `#fafafa`) flares along the advancing edge.

## Shared machinery

- **Frame analysis** — per-cell luminance + a 16-bin histogram; the dominant mode
  is the "background mass". Sobel-ish edge strength marks structure.
- **Content seed** — growth starts at the *centroid of the dominant-luminance
  region* (a real point on the piece), overridable via `?seedx,?seedy`.
- **Per-cell flip time `T[i]`** computed by the chosen mode (below), then rendered
  as: draw B underneath, draw A on top, punch A out where `p ≥ T[i]` (so B shows
  through), then paint the glyph burn-front with a `sin(πφ)` bell (alpha + size
  grow then fall) along cells near the front.

## The three tendencies

| mode | mechanism | feel |
|------|-----------|------|
| **keyed** (`keyed-dissolve`) | dominant luminance band flips **early**, the rest **late**, value-noise stagger (`keybias`, `spread`) | clean keyed cut — background evaporates, subject holds longest |
| **fractal** (`keyed-dissolve-fractal`) | **Dijkstra geodesic** front from the seed; cost cheap on background, **resistant on content** + fractal-noise tendrils (`noise`, `resist`) | a front that races the background and fingers into the subject |
| **DBM** (`keyed-dissolve-dbm`) | **dielectric-breakdown**: harmonic potential (SOR-relaxed) with growth prob ∝ `φ^η` steered toward edges (`eta`, `content`, `fill`), then a content-weighted geodesic secondary fill | organic lightning / dendrites that crawl the artwork |

## Rendering (already cross-pollinated)

`render-dissolve.js` (transitions session) renders headlessly with Playwright by
driving **this engine's URL API** (`redkey-ascii-morph.html?a=&b=&dur=&chaos=&ease=&render=1`)
— i.e. their renderer already sits on top of the morph engine + URL API in this
folder. Pair it with the unified content-aware tool when that lands.

## Recommended for the reel

For the RedKey reel scene-to-scene cuts, the **content-aware dissolve** is the
recommended transition (over a flat noise dissolve). Mode/tendency and timing
defaults: see the transitions session's advice (pidge thread
`msg_20260627_073025` → `…074059` → `…092208`).
