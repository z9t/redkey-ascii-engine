# ASCII Foreign-Scripts — HOWTO

Multi-script ASCII-art generator + Hermes profile theming, built by `seek` (2026-05-27, "seeks heavy"
session). Renders text/glyph art from **20 world scripts** and themes profiles with characters drawn from a
**212-character / 57-country** database. (The original ISF/VDMX shader `multiscript_glyph_field.fs` is
intentionally NOT included here — this folder is the **skill + DB + Python tools** only.)

Canonical home: `~/Documents/Code/ascii-isf/`. Skill: `profile-theming-system`
(installed in the `animator` Hermes profile and Claude Code's `~/.claude/skills/`).

## Files here
| File | What it is |
|---|---|
| `ascii-script.py` | The generator — CLI + web ASCII/glyph art tool |
| `vibe-theme.py` | Pick a character by "vibe" and theme a profile |
| `theme-profile.py` | Theme a profile with a specific named character |
| `regenerate-all.py` | Rebuild all profile skins/SOULs/iTerm tabs from `profile-map.json` |
| `character-database.json` | 212 characters · 12 categories · 57 countries · native greetings (the foreign-scripts data) |
| `profile-map.json` | profile → hex colour / character / group assignments |

## Requirements
- `python3` (3.9+). The web mode serves on `localhost:8080`. No API keys.
- Run from this folder, or `cd ~/Documents/Code/ascii-isf/scripts` (the canonical copies).

## Quick start

### 1. Generate ASCII / glyph art
```bash
python3 ascii-script.py --cli            # render to the terminal
python3 ascii-script.py --web            # live tool at http://localhost:8080
                                         #   colour + threshold controls, WebGL realtime mode
python3 ascii-script.py --help           # all options
```

### 2. Theme a profile by vibe
```bash
python3 vibe-theme.py --vibe "shy librarian"   # matches a character from the 212-char DB
python3 vibe-theme.py --schitzo                # random character
```

### 3. Theme a profile with a specific character
```bash
python3 theme-profile.py <profile> <character>
```

### 4. Rebuild every profile's identity from the master map
```bash
python3 regenerate-all.py                # rebuilds 19 profile skins + SOULs + iTerm tab colours
```
Edit `profile-map.json` first to change colour/character/group assignments.

## The character database
`character-database.json` — 212 eccentric characters across 12 categories (manga, European cinema, Korean,
Australian cult, Bollywood, Latin American, silent era, African, …) and 57 countries. Each entry has a
catchphrase, emoji, verbs, and a **native greeting** (the foreign-script text). This is the data that makes
the ASCII output multi-script.

## As a skill
`profile-theming-system` is now installed in:
- `~/.hermes/profiles/animator/skills/profile-theming-system/` (Hermes `animator` profile)
- `~/.claude/skills/profile-theming-system/` (Claude Code)

Invoke it when creating/theming a Hermes profile — it runs this same pipeline (iTerm tab colour → skin →
SOUL persona) using the scripts + DB above.

## Provenance / related
- Built in seek session `20260527_014110_6c89da` ("seeks heavy").
- Precursor: `build_ascii_idents.py` (LLMIA animated ASCII idents, 2026-04-30) — in `~/Documents/redkey/`.
- Excluded by request: the ISF shader `multiscript_glyph_field.fs` (a VDMX/OBS generator).
