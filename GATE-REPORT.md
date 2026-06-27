# GATE REPORT — RedKey ASCII morph (Codex build)

Reviewer: independent gate (static code review + syntax + grep + server reachability).
Target: `redkey-ascii-morph.html` (285 lines, single self-contained HTML).
Method: read actual code (not the self-report), diffed against `redkey-ascii-morph.BEFORE-codex-20260627.html`, `node --check` on extracted inline script, grep wiring confirmation, `curl` localhost. Canvas pixels NOT visually rendered (cannot — see human-QA list).

## JS syntax
**PASS.** Extracted inline `<script>` (42,094 chars) → `node --check` passes. Server live: `curl http://localhost:8745/redkey-ascii-morph.html` → 200.

## Per-item verdicts

**1. Offline frame-stepped render — PASS.**
`renderTransition()` (L233) steps `frames=round(transDur*renderFps)` deterministically; `loop()` is suspended via `if(rendering)return` (L180) so it is NOT real-time gated. `encodeWebM()` (L227) uses WebCodecs `VideoEncoder` VP8 with explicit per-frame timestamps; `makeWebM()` (L226) is a hand-rolled EBML/WebM muxer. PNG-seq via `encodeZip()`+`makeZip()` (L230-231, stored ZIP + crc32). Apply-to-video: `renderVideoFile()` (L235) seeks an input clip frame-by-frame (`seekVideo`, L234), `frames=round(duration*fps)`. All four buttons wired (L209-213). Real frame-stepping confirmed.

**2. Transition effects — PASS.**
Colour-match: `samplePaletteFromLayer()` (L217) averages 3 luminance bands from A and B; `lerpHex()` (L216) lerps per-band across `p`, gated by `transColor>=.5` (L233). Size pulse: `fontScale:1+transPulse*sin(π·p)` passed into `frame(opts)` → applied via `ctx.font` scale (L166/170), NO `cell`/grid rebuild. Size↔noise: `sizeNoise` opt → per-cell `fs=(CELL-4)*fontScale*(1+sizeNoise*(tgt[i]-.5))` (L173). All three are CTRL+GROUPS entries (L77, "transition" group L195). Effects apply during export draw (correct scope).
**IMPORTANT for QA:** `loop()` calls `frame()` with no opts, so all three of `transColor`/`transPulse`/`transSizeNoise` are **inert in the live preview** — they are consumed ONLY inside `renderTransition`'s draw closure. Colour-match and size-pulse need transition progress `p` so this is unavoidable; size↔noise is render-only by design. A tester poking these sliders on the live canvas will see nothing happen — verify them in the **exported WebM/PNG-seq**, not the live panel. This is not a dead stub (they are wired and used in the render path).

**3. Text source — PASS.**
`btext` button (L47) → `textInto()` (L135); layer mode `"text"` sampled by `fillText()` (L123) which honours `TRANSFORMS.text`, bold and font-family. UI: `textval`/`fontname`/`textbold`/`fontpick` (L49-51) all wired (L247-250). `fontpick` calls `queryLocalFonts()` with try/catch fallback to manual font-name field (L250). `mkLayer()` carries text/font/bold (L115).

**4. Shared transform + target selector — PASS.**
`TRANSFORMS={feedback,text,A,B}` (L85); one slider set `trX/trY/trScaleX/trScaleY` (in NOMOTION) + `trtarget` dropdown injected into transform group (L201). `loadTransformToCTRL`/`saveTransformFromCTRL` (L199-200) move values per target; slider input calls save (L190). Feedback reads `TRANSFORMS.feedback` (L165); A/B manual fit reads `trFor(L)` (L121); text reads `TRANSFORMS.text`. Old `fbScaleX/fbScaleY/fbX/fbY` sliders fully removed (0 refs) and replaced. Minor (non-bug): `k.startsWith("tr")` save-trigger also fires for `transDur/transChaos/...` but only re-writes unchanged trX/Y → no effect.

**5. Fit/Fill/Stretch (+ manual) — PASS.**
`fitmode` select (L46) → `active.fit`. `fillMedia()` (L118-122) implements `fit`=contain, `fill`=cover, `manual`=transform-driven; `stretch` is the default fall-through (`w=cols,h=rows` = distort), which is correct. Per-layer (`L.fit`), persisted in preset (`_fitA/_fitB`).

**6. Screen capture — PASS.**
`bscreen` (L47) → `screenInto()` (L136) uses `navigator.mediaDevices.getDisplayMedia()`, assigns stream to `L.video`, mode `"screen"` sampled through the same `fillMedia` path (L126); track `ended` falls back to noise. Unsupported-browser guard present. NDI/Syphon left as a clearly-marked UI note stub (L206) per brief.

**7. Particle mode — PASS (basic, as scoped).**
`particleMode` toggle + gravity/wind/turb/attract/drag/lifespan in CTRL (L78) and "particles" group (L195). `frame()` branches on `particleMode>=.5` (L166-168): `ensureParticles`, per-particle velocity with `pGravity`/`pWind`/`pTurb`, single centre attractor via `pAttract` (signed = converge/repel), `pDrag`, `pLife` respawn. Keeps RedKey glyph pools + band colours. Single-point/centre attractor only — noted as intended basic scope in FUTURE-IDEAS.

## Non-breakage (pre-existing features)
- Two-layer A/B + blend modes — **PASS** (`combine()` L129-130, 7 modes intact).
- Per-slider motion mSine/mRand/mSmooth — **PASS** (`applyMod` L177, makeRow checkboxes L193).
- Settable min/max — **PASS** (mn/mx handlers L191-192).
- 🎲 randomise — **PASS** (L253, skips NOMOTION).
- Feedback — **PASS** (now via TRANSFORMS.feedback; functional).
- Media bank LRU + remove — **PASS** (addVideo/removeBank/renderBank, MAXBANK=10).
- Scripts→colour chips + randomise — **PASS** (renderChips L266, randscripts L267).
- Accordion GROUPS — **PASS** (L195-197).
- Draggable / minimise panel — **PASS** (h1 drag L268, hide/show L263-264).
- Copy/load preset — **PASS** (copy now also serializes _transforms/_fit/_text; applyPreset restores them L258-260).
- ● record — **PASS** (MediaRecorder L261).
- Transition URL API `?a&b&dur&chaos&ease&render=1` — **PASS** (L273-283, applyPreset+loadLayerImgUrl+auto render).

No removed/broken pre-existing code paths found.

## Overall verdict: ACCEPTED-WITH-NOTES
All 7 build items are genuinely implemented and wired into the render/loop (no dead stubs); all listed pre-existing features have intact code paths; JS parses; page serves 200. Acceptance is "with notes" only because correctness of two runtime artifacts cannot be confirmed by static review and require eyes-on/playback.

## Needs human visual QA (eyes-on-canvas / runtime only)
1. **WebM muxer validity** — the hand-rolled EBML/VP8 container (`makeWebM`) must actually play back (VLC/Chrome) at ≈ requested duration; muxer bugs won't show in `node --check`. PNG-seq ZIP is the stated fallback if it fails.
2. **WebCodecs availability** — `encodeWebM` throws (caught, shown in status) on browsers without `VideoEncoder` (Safari/older FF); confirm graceful fallback to PNG seq.
3. **Colour-match shift** — confirm band colours visibly migrate A→B over a real transition with differing footage.
4. **Size pulse** — confirm grow/shrink at midpoint with NO grid-rebuild stutter.
5. **Screen capture** — confirm `getDisplayMedia` permission prompt + live stream appears as a layer.
6. **Particle motion** — confirm glyphs move and converge/repel from centre under attract sign.
7. **Apply-to-video** — confirm output length ≈ source and frame count = round(duration*fps); cross-origin/tainted input would throw in `fillMedia.getImageData` (test with same-origin localhost media).
8. **Console-clean** — runtime console errors cannot be confirmed statically; verify on localhost per the report's own caveat.
