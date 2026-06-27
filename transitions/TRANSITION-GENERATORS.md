# RedKey transition generators — future implementations + research brief

Menu of equations/algorithms for **dividing / splitting / and-or / intersecting**
one frame into another as a glyph dissolve. Companion to `TRANSITIONS.md`
(the transitions session's keyed / fractal / DBM trio).

## Unifying frame: arrival-time field + field algebra

Every transition reduces to a scalar **arrival-time field `T[i] ∈ [0,1]`** over the
grid: reveal where `p ≥ T[i]`, paint the glyph burn-front along `|p − T[i]|`.
"and / or / intersect" is then **field algebra** over two (or more) fields:

- **AND / intersect** → `min(F,G)` or `F·G`  (reveal only where both agree)
- **OR / union** → `max(F,G)`, or **smooth-min** `smin(F,G,k)` for organic blends
- **XOR / seam** → `|F−G|`  (reveal the boundary between two reveals)
- **mask / difference** → `F·(1−G)`

This makes every generator below composable with every other.

## The generators

### 1. PDE growth fronts (organic, alive)
- **Eikonal / Fast Marching** ★ — `|∇T| = 1/F(x)`; front speed `F` = content-driven
  (fast on background, slow on edges). Clean generalization of the Dijkstra geodesic.
  **← first implementation (this folder).**
- **Reaction–diffusion (Gray–Scott)** ★ — Turing spots/stripes/labyrinths; feed-rate
  seeded from luminance → the dissolve grows the artwork's texture.
- **Cahn–Hilliard / Allen–Cahn** — spinodal "unmixing" of A and B phases.
- **FitzHugh–Nagumo excitable media** — rotating spiral / target waves.

### 2. Space partitioning (divide / shatter) ★
- **Weighted (power) Voronoi** — sites on feature points/edges; reveal cell-by-cell.
- **Quadtree / k-d / BSP** — subdivide more where the image is busy (content-aware blocks).
- **Delaunay shatter** — triangulate features, reveal triangles outward (glass break).
- **Apollonian gasket / circle packing** — nested circles by radius.

### 3. Fractals & basins (wild boundaries)
- **Newton's-method fractal** — basins of `z − f(z)/f′(z)`; fractal intersect lines.
- **Escape-time (Mandelbrot/Julia)** — `T` = escape iteration count.
- **DLA (diffusion-limited aggregation)** — particle cousin of DBM; frost/coral.

### 4. Content-aware cuts (smartest split/intersect) ★
- **Watershed segmentation** — flood from minima; image divides along ridge lines.
- **Graph min-cut / max-flow (s–t cut)** — the optimal seam between A- and B-regions.
- **Seam carving** — DP least-energy seams; reveal peels around the subject.
- **Spectral / normalized cut** — partition by the Fiedler vector (`Lv = λv`).

### 5. Flow & warp (advected, morphing)
- **Curl-noise flow field** — divergence-free streamlines; swirly, mass-conserving.
- **Optical flow A→B** ★ — dissolve along the true correspondence between frames.
- **Domain warping** — fBm warped by fBm; marbled/liquid fronts.
- **Phyllotaxis (Vogel spiral, golden angle 137.5°)** — sunflower-seed reveal.

### 6. Better ordering (cheap quality bump)
- **Blue-noise / void-and-cluster** — evenly-spread threshold map; replaces white-noise stagger.
- **Error-diffusion / Ostromoukhov** — halftone reveal order.
- **Metaballs / SDF smooth-min** — implicit blobs that merge and split (great with field algebra).

### 7. Cellular automata
- **Life / Larger-than-Life / Generations** — glider fronts.
- **Cyclic CA / Greenberg–Hastings / Belousov–Zhabotinsky** — spirals and demons.

## Priority (payoff ÷ effort)
1. Eikonal / Fast-Marching  2. Gray–Scott RD  3. weighted Voronoi + quadtree
4. min-cut / seam-carving  5. blue-noise ordering (apply everywhere, free win)

## Research questions (for the `research` delegation)
For **each** generator: (a) canonical paper/reference + the governing equation;
(b) recommended parameter ranges for a *visual* (not scientific) result;
(c) browser-JS real-time feasibility on a 60×60–150×150 grid (cost, any GPU need);
(d) how to make it **content-aware** (drive from luminance/edges/saliency);
(e) prior art in generative art / VJ / motion design; (f) the cleanest reference
implementation to port. Deliver as a corpus alongside the earlier motion-design/CV
transition corpus.
