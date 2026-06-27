#!/usr/bin/env python3
"""Regenerate all profile skins, iTerm configs, and SOUL.md from the master profile map."""
import json, os, shutil

PROFILE_MAP = "/Users/max/.hermes/profiles/seek/skills/hermes-profile-skinning/profile-theming-system/references/profile-map.json"
SKINS_DIR = "/Users/max/.hermes/skins"
ITERM_DIR = "/Users/max/Library/Application Support/iTerm2/DynamicProfiles"
PROFILES_DIR = "/Users/max/.hermes/profiles"

SPINNER_VERBS = {
    "Sherlock Holmes": ["deducing", "observing", "analyzing", "noticing", "connecting", "elementary"],
    "Gandalf": ["guarding", "warding", "counseling", "watching", "guiding", "barring passage"],
    "Herman the German": ["inspecting", "approving", "rejecting", "checking", "verifying", "validating"],
    "Tony Stark": ["fabricating", "soldering", "iterating", "building", "prototyping", "shipping"],
    "Daedalus": ["designing", "blueprinting", "plotting", "constructing", "engineering", "architecting"],
    "Professor X": ["scanning", "reading", "knowing", "sensing", "connecting", "understanding"],
    "Yoda": ["teaching", "learning", "training", "meditating", "guiding", "illuminating"],
    "Indiana Jones": ["excavating", "discovering", "searching", "uncovering", "investigating", "recovering"],
    "Edna Mode": ["sketching", "draping", "styling", "designing", "cutting", "fitting"],
    "Hayao Miyazaki": ["animating", "storyboarding", "drawing", "painting", "dreaming", "creating"],
    "Steve Jobs": ["reimagining", "simplifying", "perfecting", "polishing", "revealing", "launching"],
    "Judge Dredd": ["judging", "sentencing", "ruling", "evaluating", "verdicting", "enforcing"],
    "The Oracle": ["considering", "weighing", "illuminating", "revealing", "choosing", "knowing"],
    "Atticus Finch": ["deliberating", "arguing", "reasoning", "defending", "advocating", "considering"],
    "Elle Woods": ["researching", "briefing", "arguing", "winning", "outfitting", "excelling"],
    "Aragorn": ["tracking", "ranging", "scouting", "seeking", "finding", "traversing"],
    "Neo": ["hacking", "loading", "bending", "perceiving", "awakening", "transcending"],
    "James Bond": ["securing", "defusing", "infiltrating", "extracting", "intercepting", "neutralizing"],
    "Scotty": ["optimizing", "tuning", "upgrading", "calibrating", "boosting", "engineering"],
}

EMOJIS = {
    "Sherlock Holmes": "🕵️",
    "Gandalf": "🧙",
    "Herman the German": "🛡️",
    "Tony Stark": "⚡",
    "Daedalus": "🏛️",
    "Professor X": "🧠",
    "Yoda": "🌿",
    "Indiana Jones": "🗺️",
    "Edna Mode": "👠",
    "Hayao Miyazaki": "🐉",
    "Steve Jobs": "✨",
    "Judge Dredd": "⚖️",
    "The Oracle": "🔮",
    "Atticus Finch": "📜",
    "Elle Woods": "💅",
    "Aragorn": "🗡️",
    "Neo": "🟢",
    "James Bond": "🔫",
    "Scotty": "🚀",
}


def generate_skin(profile, data):
    color = data["color"]
    character = data["character"]
    emoji = EMOJIS.get(character, "◆")
    verbs = SPINNER_VERBS.get(character, ["processing", "analyzing", "computing"])

    return f"""# {profile} skin — {character}
name: {profile}_{color[1:]}
description: {profile} — {character}

colors:
  banner_border: "{color}"
  banner_title: "{color}"
  banner_accent: "{color}"
  ui_accent: "{color}"
  input_rule: "{color}"
  response_border: "{color}"
  session_label: "{color}"

spinner:
  waiting_faces:
{chr(10).join(f'    - "{f}"' for f in [emoji, emoji * 2, emoji * 3])}
  thinking_faces:
{chr(10).join(f'    - "{f}"' for f in [emoji, "◉", "◎"])}
  thinking_verbs:
{chr(10).join(f'    - "{v}"' for v in verbs)}
  wings:
    - ["⟨", "⟩"]
    - ["⟪", "⟫"]

branding:
  agent_name: "{character}"
  welcome: "{data['catchphrase']}"
  response_label: " {emoji} {character} "
  prompt_symbol: "{emoji}"

tool_prefix: "┊"

tool_emojis:
  terminal: "⚙"
  web_search: "🔍"
  read_file: "📄"
"""


def generate_soul(profile, data):
    character = data["character"]
    catchphrase = data["catchphrase"]
    country = data["country"]

    voices = {
        "Sherlock Holmes": ("analytical", "direct", "deductive", "observe", "deduce", "fluff", "speculation", "bluster"),
        "Gandalf": ("wise", "poetic", "measured", "guide", "protect", "haste", "triviality", "blunt force"),
        "Herman the German": ("stern", "precise", "binary", "inspect", "approve", "ambiguity", "sloppiness", "excuses"),
    }

    style_adj = voices.get(character, ["direct", "helpful", "professional", "analyze", "deliver", "fluff", "confusion", "overpromising"])
    
    char_name = character.upper()
    return f"""# Personality

You are {character} — {catchphrase}

## Style
- Be {style_adj[0]} without being cold
- Speak with {style_adj[1]} precision
- {style_adj[3]} first, then {style_adj[4]}
- Your home is {country}
- Inhabit your voice fully — become {character}

## What to avoid
- {style_adj[5]}
- {style_adj[6]}
- {style_adj[7]}
- Breaking character under pressure
"""


def generate_iterm(profile, data):
    color = data["color"]
    skin_name = f"{profile}_{color[1:]}"
    r, g, b = int(color[1:3], 16) / 255, int(color[3:5], 16) / 255, int(color[5:7], 16) / 255
    
    return {
        "Profiles": [{
            "Name": profile,
            "Guid": f"{profile}-{data['character'].replace(' ','-').lower()}",
            "Command": f"hermes -p {profile} chat",
            "Initial Text": f"/skin {skin_name}\\n",
            "Tab Color": {
                "Red Component": r,
                "Green Component": g,
                "Blue Component": b
            }
        }]
    }


def main():
    with open(PROFILE_MAP) as f:
        profiles = json.load(f)

    os.makedirs(SKINS_DIR, exist_ok=True)
    os.makedirs(ITERM_DIR, exist_ok=True)

    for profile, data in profiles.items():
        # Skin YAML
        skin_path = os.path.join(SKINS_DIR, f"{profile}_{data['color'][1:]}.yaml")
        with open(skin_path, 'w') as f:
            f.write(generate_skin(profile, data))
        print(f"  ✓ skin: {os.path.basename(skin_path)}")

        # SOUL.md
        soul_path = os.path.join(PROFILES_DIR, profile, "SOUL.md")
        with open(soul_path, 'w') as f:
            f.write(generate_soul(profile, data))
        print(f"  ✓ SOUL: {profile}")

        # iTerm dynamic profile
        iterm_path = os.path.join(ITERM_DIR, f"hermes-{profile}.json")
        with open(iterm_path, 'w') as f:
            json.dump(generate_iterm(profile, data), f, indent=2)
        print(f"  ✓ iTerm: hermes-{profile}.json")

    print(f"\nAll {len(profiles)} profiles regenerated.")


if __name__ == "__main__":
    main()
