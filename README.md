# RedKey ASCII / glyph engine

A single self-contained browser tool that renders images, video, screen capture,
text, or noise as a live field of **real glyphs from 20 world scripts**
(CJK / Thai / Tibetan / Arabic / Hebrew / Greek / …) in the RedKey palette
(red `#dc2626` / tan `#b8aa98` / white `#fafafa`).

## Run
The canvas taints under `file://`, so serve over http:
```
./serve.command           # double-click, or:
python3 -m http.server 8745
# open http://localhost:8745/redkey-ascii-morph.html
```

## Headline file
`redkey-ascii-morph.html` — two source layers A/B with blend modes, an organic
fbm/warp/ridged/cellular noise engine (real scale), per-slider motion
(∿ sine / ◇ random / ~ smooth between each row's min↔max), feedback/trails,
media bank (2×5 LRU), text source + system fonts, fit/fill/stretch, screen
capture, a basic particle mode, copy/load presets, WebM/PNG-seq export, an
**offline frame-stepped transition render** (A→B dissolve), apply-ASCII-to-video,
and a headless URL render API: `?a=&b=&dur=&chaos=&ease=&render=1`.

## Transitions
See `transitions/RECIPE.md` + `make-transition.sh` for scene-dissolve recipes.
The **content-aware scene-dissolve engine** (keyed-dissolve, mode+tendency sliders)
is a sibling work-in-progress from the RedKey-transitions session and will be
added here once it stabilises.

## Skill
`skill/` is the `redkey-ascii-engine` SkillMD skill so an agent can drive the
tool for reel transitions.
