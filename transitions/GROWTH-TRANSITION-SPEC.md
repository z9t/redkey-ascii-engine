# RedKey ASCII growth-transition — build spec + prompt

The signature RedKey scene transition. Authored from Max's spec. This is the thing the
earlier attempts (eikonal, gray-scott, dissolve, noise-mask) all FAILED to be.

---

## 0. The one hard rule (why everything before was wrong)

**It is NOT an opacity fade of a computed shape.** Every field method — eikonal fronts,
reaction-diffusion, keyed dissolves, noise masks — collapses to "compute a scalar field,
fade glyph `globalAlpha` in along it." That is a wipe with glyphs sprinkled on the edge.
**Reject it.**

Here the glyphs **grow by SCALE (0 → 1)** and **spawn** from the content. The motion is
*growth and emission*, not alpha. If you ever write `globalAlpha = field`, you've built
the wrong thing again.

---

## 1. Pipeline (Max's spec, verbatim then expanded)

> Analyse frame → Colour analysis → spatial analysis → find most prominent elements →
> use as shape and x/y position/s to spawn from → use algorithmic organic growth algo to
> begin to spawn from those locations → ascii characters appear via scale 0→1 (1=definable
> variable) → ascii characters continue to spawn along the front of the wave using noise
> overlay in b&w white value at that x/y location to define speed of scale growth from
> 0→1, glyph lifetime and size of spawn front width as definable variables

Expanded:

1. **Analyse frame** — load frame A (source) and frame B (target). Sample each to a working
   grid (e.g. 160×160) plus keep a full-res copy for colour sampling.
2. **Colour analysis** — dominant/background colour (luminance-histogram mode or k-means,
   Lloyd-1982/Wu-1992 in the corpus); per-cell colour for later glyph tinting.
3. **Spatial analysis** — per-cell luminance, edge strength (Sobel/Canny), and a
   **saliency / distinctiveness map** = how distinct each cell is from the background
   (Itti–Koch–Niebur 1998).
4. **Find most prominent elements** — threshold + connected-component / blob-detect the
   saliency map into the few **most prominent regions** (the subject, headline text, logo).
   For each: its **shape (mask)** and **centroid x/y** (and/or several seed points along it).
5. **Spawn origins** — those prominent elements ARE the spawn sources: shape + one or more
   (x,y) seed positions. (Count of origins = definable; default = top N salient blobs.)
6. **Organic growth** — from each origin, grow a front OUTWARD across the frame with an
   *organic* growth algorithm — recommended: **space colonization** (Runions 2005/2007, in
   the corpus — branches grow toward content attractors), or DLA, or an eikonal/FMM front
   with content-weighted speed. The growth yields, per cell, an **arrival order/time**
   (when the front reaches it) and a front geometry.
7. **Glyph spawn + SCALE 0→1** — when the growth front reaches a cell, **spawn an ASCII
   glyph there** and animate its **scale from 0 to MAXSCALE** (MAXSCALE = definable; "1").
   This is a transform scale, **not** opacity. The glyph pops/grows into existence.
8. **Continuous spawn along the wavefront** — the advancing front continuously spawns new
   glyphs at its **leading edge**; the **front width** (how thick the actively-spawning band
   is) is definable.
9. **Noise drives growth speed** — overlay a **b&w noise field**; the **white value at a
   glyph's (x,y)** sets the **speed of its 0→1 scale growth** (bright = fast pop-in, dark =
   slow). Same noise can also jitter spawn timing along the front.
10. **Glyph lifetime** — each glyph has a definable **lifetime**; at end it either rests at
    full scale (if it represents the final image) or scales back 1→0 / hands off (during the
    A→B handover).

### A → B transition arc
- Grow from **A's** prominent origins → A's content assembles in scaling glyphs.
- Hand over: start growth from **B's** prominent origins; A's glyphs reach end-of-lifetime
  and scale back out as B's front sweeps in → B's content assembles. (Crossfade the two
  growth systems over the transition `p`, or sequence: A grows in → hold → B grows over.)

---

## 2. Definable variables (must be live/tunable)

| var | meaning | sensible default |
|-----|---------|------------------|
| `maxScale` | the "1" target glyph scale | 1.0 (×base cell px) |
| `growthSpeed` | base 0→1 scale-growth rate | ~2.5 /s |
| `noiseSpeedRange` | how much noise white-value modulates growth speed | 0.3–2.0× |
| `glyphLifetime` | seconds a glyph lives | 2.0 |
| `frontWidth` | thickness of the active spawn band (cells) | 6 |
| `originCount` | number of prominent-element spawn sources | 3–6 |
| `growthAlgo` | space-colonization \| dla \| eikonal | space-colonization |
| `noiseScale`/`noiseSpeed` | the b&w overlay noise | tune |
| palette | RedKey red `#dc2626` / tan `#b8aa98` / white `#fafafa` (or content-true) | RedKey |
| glyph set | multi-script (CJK/Thai/Tibetan/Arabic/Greek/…) per the engine | — |

---

## 3. Architecture / integration

- New self-contained file: `transitions/growth-transition.html` in **z9t/redkey-ascii-engine**.
- Match the engine conventions: vanilla JS canvas, RedKey palette default, URL API
  `?a=&b=&dur=&p=&maxscale=&growthspeed=&lifetime=&frontwidth=&origins=&algo=&render=1`,
  `?p=` static freeze (simulate the growth to `p` then draw), headless-renderable via the
  existing `transitions/render-dissolve.js` Playwright path.
- Serve over http (canvas taints on file://): `python3 -m http.server 8745`.

## 4. Research anchors (already on disk)

`/Users/max/know/research/motion-design-cv-2026-06-27/` —
- **Space colonization / vein growth**: Runions 2005 (`papers/e__2005__runions...`), Runions 2007.
- **Saliency (most distinct from bg)**: Itti–Koch–Niebur 1998 (`papers/c__1998__itti...`).
- **Edges**: Canny 1986, Sobel 1968. **Blob/segmentation**: Felzenszwalb 2012 distance transform.
- **Organic growth alternatives**: DLA (Witten–Sander 1981), DBM (Niemeyer 1984).
- **Noise overlay**: Perlin 1985/2002, Gustavson 2005 (simplex), iq domain-warp.
- **Colour analysis**: Lloyd 1982 (k-means), Wu 1992 quantization.

## 5. Acceptance criteria (the gate)

1. **No opacity reveal.** Glyphs animate by `scale` 0→1; removing the alpha-mask logic does
   not break the reveal. (If you grep the file for `globalAlpha =` driving the reveal, fail.)
2. Glyphs visibly **spawn FROM the prominent content elements** (subject/headline/logo) and
   grow **outward along an organic front**, not uniformly and not from screen centre.
3. **Per-glyph growth speed varies with the b&w noise** at its (x,y) (visibly: some pop fast,
   some crawl).
4. `maxScale`, `growthSpeed`, `glyphLifetime`, `frontWidth`, `originCount` all change the
   result as described.
5. **A→B**: glyphs assemble A's content, then hand over and reassemble B's content.
6. Verified headless (Playwright still + short mp4); RedKey palette; multi-script glyphs.

---

## 6. BUILD PROMPT (paste into a fresh, clean-context session)

> Build `transitions/growth-transition.html` in the RedKey ASCII engine
> (`~/Documents/redkey/ascii-foreign-scripts/`, repo z9t/redkey-ascii-engine). It is the
> signature RedKey scene transition between two frames A and B.
>
> **Absolute constraint: it is NOT an opacity/alpha fade of a shape.** Glyphs reveal by
> animating **scale 0→1**, spawned from the content. Do not use `globalAlpha` as the reveal.
>
> Pipeline: analyse A and B → colour + spatial (luminance/edge/saliency) analysis → find the
> few most prominent elements (saliency blobs, with shape + centroid x/y) → use those as
> spawn origins → grow an **organic front** outward from them (space colonization toward
> content attractors; fall back to eikonal/DLA) → as the front reaches each cell, **spawn an
> ASCII glyph and grow its scale 0→maxScale** → keep spawning glyphs along the advancing
> **front (width = variable)** → a **b&w noise overlay's white value at each (x,y) sets that
> glyph's scale-growth speed** → each glyph has a **lifetime**. Then hand A→B: grow B's
> content from B's origins as A's glyphs age out.
>
> Definable variables: maxScale, growthSpeed, noiseSpeedRange, glyphLifetime, frontWidth,
> originCount, growthAlgo, noiseScale/Speed, palette (RedKey default), glyph set (multi-script).
>
> Conventions: vanilla JS canvas, self-contained HTML, RedKey palette (#dc2626/#b8aa98/#fafafa),
> URL API `?a&b&dur&p&maxscale&growthspeed&lifetime&frontwidth&origins&algo&render=1`, `?p=`
> static freeze, serve over http://localhost:8745, headless-renderable via
> `transitions/render-dissolve.js`. Research corpus at
> `/Users/max/know/research/motion-design-cv-2026-06-27/` (Runions space-colonization, Itti
> saliency, Canny/Sobel edges, Perlin/Gustavson noise, Lloyd/Wu colour).
>
> Verify headless (a `?p=0.5` still + a short mp4) and check every acceptance criterion in
> `transitions/GROWTH-TRANSITION-SPEC.md` §5 before declaring done. Coordinate with the
> RedKey-transitions Claude session, which owns the dissolve-engine work.
