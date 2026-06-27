#!/usr/bin/env python3
"""Theme a single profile. Usage: theme-profile.py <profile> <hex_color> <character> <catchphrase> <country>"""
import sys, os

SKINS_DIR = "/Users/max/.hermes/skins"
PROFILES_DIR = "/Users/max/.hermes/profiles"
ITERM_DIR = "/Users/max/Library/Application Support/iTerm2/DynamicProfiles"

if len(sys.argv) < 6:
    print("Usage: theme-profile.py <profile> <hex> <character> <catchphrase> <country>")
    sys.exit(1)

profile, hex_color, character, catchphrase, country = sys.argv[1:6]

# Generate skin
color_key = hex_color[1:]
skin = f"""name: {profile}_{color_key}
description: {profile} — {character}

colors:
  banner_border: "{hex_color}"
  banner_title: "{hex_color}"
  banner_accent: "{hex_color}"
  ui_accent: "{hex_color}"
  input_rule: "{hex_color}"
  response_border: "{hex_color}"
  session_label: "{hex_color}"

branding:
  agent_name: "{character}"
  welcome: "{catchphrase}"
  response_label: "◆ {profile} "
  prompt_symbol: "◆"

tool_prefix: "┊"
"""

os.makedirs(SKINS_DIR, exist_ok=True)
with open(os.path.join(SKINS_DIR, f"{profile}_{color_key}.yaml"), 'w') as f:
    f.write(skin)

# Generate SOUL
soul = f"""# Personality

You are {character}. {catchphrase}

## Style
- Be direct without being cold
- Speaks with {country} character
- Observe first, act decisively
- Inhabit your voice fully — become {character}

## What to avoid
- Fluff and filler
- Breaking character under pressure
- Overexplaining the obvious
"""

os.makedirs(os.path.join(PROFILES_DIR, profile), exist_ok=True)
with open(os.path.join(PROFILES_DIR, profile, "SOUL.md"), 'w') as f:
    f.write(soul)

# Generate iTerm profile
import json
r, g, b = int(hex_color[1:3], 16)/255, int(hex_color[3:5], 16)/255, int(hex_color[5:7], 16)/255
iterm = {"Profiles": [{
    "Name": profile,
    "Command": f"hermes -p {profile} chat",
    "Initial Text": f"/skin {profile}_{color_key}\\n",
    "Tab Color": {"Red Component": r, "Green Component": g, "Blue Component": b}
}]}
os.makedirs(ITERM_DIR, exist_ok=True)
with open(os.path.join(ITERM_DIR, f"hermes-{profile}.json"), 'w') as f:
    json.dump(iterm, f, indent=2)

print(f"Themed {profile} as {character} ({hex_color})")
print(f"  Skin: ~/.hermes/skins/{profile}_{color_key}.yaml")
print(f"  SOUL: ~/.hermes/profiles/{profile}/SOUL.md")
print(f"  iTerm: DynamicProfiles/hermes-{profile}.json")
