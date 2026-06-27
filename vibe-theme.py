#!/usr/bin/env python3
"""
Create a fully themed Hermes profile from minimal inputs.
Usage: vibe-theme.py <profile_name> --main <hex> --accent <hex> --vibe "<description>" [--workarea "<path>"]

Example:
  vibe-theme.py proofreader --main "#E85D04" --accent "#4DCCBD" \\
    --vibe "shy librarian who gets really angry when people spell incorrectly" \\
    --workarea "~/Documents/Code/spellchecker"
"""
import sys, os, json, argparse

SKINS_DIR = "/Users/max/.hermes/skins"
PROFILES_DIR = "/Users/max/.hermes/profiles"
ITERM_DIR = "/Users/max/Library/Application Support/iTerm2/DynamicProfiles"

# Archetype database — vibe patterns → character suggestions
ARCHETYPES = {
    "quiet furious perfectionist bookish grammar pedantic librarian": {
        "character": "Severus Snape",
        "from": "Harry Potter",
        "country": "British",
        "verbs": ["checking grammar", "correcting spelling", "glaring at errors", "proofreading", "silently judging", "deducting points"],
        "emoji": "📚",
        "catchphrase": "Obviously."
    },
    "fast witty sarcastic builder maker inventor": {
        "character": "Tony Stark",
        "from": "Iron Man",
        "country": "American",
        "verbs": ["fabricating", "iterating", "prototyping", "building", "soldering", "shipping"],
        "emoji": "⚡",
        "catchphrase": "Let's build something."
    },
    "wise mysterious guide mentor calm patient": {
        "character": "Gandalf",
        "from": "Lord of the Rings",
        "country": "Middle-earth",
        "verbs": ["guiding", "counseling", "watching", "warding", "illuminating", "guarding"],
        "emoji": "🧙",
        "catchphrase": "A wizard is never late."
    },
    "furious angry gatekeeper strict enforcer judge": {
        "character": "Judge Dredd",
        "from": "Judge Dredd",
        "country": "Mega-City One",
        "verbs": ["judging", "sentencing", "ruling", "evaluating", "verdicting", "enforcing"],
        "emoji": "⚖️",
        "catchphrase": "I am the law."
    },
    "wild chaotic creative experimental unhinged crazy": {
        "character": "Doc Brown",
        "from": "Back to the Future",
        "country": "American",
        "verbs": ["inventing", "experimenting", "flux-capacitator-ing", "jiggawatt-calculating", "timeline-checking", "great scott-ing"],
        "emoji": "⚡",
        "catchphrase": "Great Scott!"
    },
    "elegant precise meticulous designer stylish dramatic": {
        "character": "Edna Mode",
        "from": "The Incredibles",
        "country": "Fictional",
        "verbs": ["sketching", "draping", "designing", "styling", "cutting", "fitting"],
        "emoji": "👠",
        "catchphrase": "No capes, darling!"
    },
    "gentle poetic nature calm beauty peaceful": {
        "character": "Hayao Miyazaki",
        "from": "Studio Ghibli",
        "country": "Japanese",
        "verbs": ["animating", "storyboarding", "dreaming", "drawing", "painting", "creating"],
        "emoji": "🐉",
        "catchphrase": "The wind is rising."
    },
    "determined gritty survivor resourceful scrappy": {
        "character": "Ellen Ripley",
        "from": "Alien",
        "country": "Space",
        "verbs": ["surviving", "fighting", "securing", "purging", "nuking", "rebuilding"],
        "emoji": "🛸",
        "catchphrase": "Get away from her, you bitch!"
    },
    "mysterious noir detective cynical tired overworked": {
        "character": "Sam Spade",
        "from": "The Maltese Falcon",
        "country": "American",
        "verbs": ["investigating", "suspecting", "searching", "shadowing", "drinking coffee", "casing the joint"],
        "emoji": "🔍",
        "catchphrase": "It's a dark world."
    },
    "cheerful optimistic hopeful bright friendly warm": {
        "character": "Ted Lasso",
        "from": "Ted Lasso",
        "country": "American",
        "verbs": ["believing", "encouraging", "cheering", "supporting", "coaching", "grinning"],
        "emoji": "⚽",
        "catchphrase": "Believe!"
    },
    "stoic tough silent strong protective loyal": {
        "character": "The Mandalorian",
        "from": "Star Wars",
        "country": "Mandalore",
        "verbs": ["tracking", "protecting", "hunting", "securing", "bounty-collecting", "armor-polishing"],
        "emoji": "🪖",
        "catchphrase": "This is the way."
    },
    "childlike wonder curious explorer adventurer brave": {
        "character": "Chihiro",
        "from": "Spirited Away",
        "country": "Japanese",
        "verbs": ["exploring", "discovering", "wandering", "helping", "believing", "transforming"],
        "emoji": "🐉",
        "catchphrase": "I'm not afraid anymore."
    },
}


def find_character(vibe):
    """Match vibe description to best archetype."""
    vibe_lower = vibe.lower()
    best_match = None
    best_score = 0

    for archetype_key, data in ARCHETYPES.items():
        keywords = archetype_key.split()
        score = sum(1 for kw in keywords if kw in vibe_lower or any(syn in vibe_lower for syn in [kw]))
        if score > best_score:
            best_score = score
            best_match = data

    if best_match and best_score > 0:
        return best_match

    # Fallback: random from database
    import random
    with open(os.path.join(os.path.dirname(__file__), "..", "references", "character-database.json")) as f:
        import json as j
        all_chars = j.load(f)
    return random.choice(all_chars)


def main():
    parser = argparse.ArgumentParser(description="Create a vibe-themed Hermes profile")
    parser.add_argument("profile", help="Profile name")
    parser.add_argument("--main", required=True, help="Main colour hex (e.g. #E85D04)")
    parser.add_argument("--accent", required=True, help="Accent/highlight colour hex (e.g. #4DCCBD)")
    parser.add_argument("--vibe", help="Vibe description (e.g. 'shy librarian who hates bad spelling'). Required unless --auto or --schitzo.")
    parser.add_argument("--workarea", help="Default working directory")
    parser.add_argument("--auto", action="store_true", default=False, help="Auto-assign a character matching the vibe")
    parser.add_argument("--schitzo", action="store_true", default=False, help="Random character from the full database — different every time")
    args = parser.parse_args()

    if not args.vibe and not args.schitzo:
        parser.error("Either --vibe, --auto, or --schitzo is required")

    # Load character database
    import json as json2
    db_path = os.path.join(os.path.dirname(__file__), "..", "references", "character-database.json")
    with open(db_path) as f:
        char_db = json2.load(f)

    # Schitzo mode — totally random, mixed decorative scripts
    if args.schitzo:
        import random
        char = random.choice(char_db)
        # Pick 3 random scripts for decoration
        all_scripts = list(char.get("all_scripts", {}).values())
        if all_scripts:
            random.shuffle(all_scripts)
            char["mixed_decor"] = all_scripts[:4]
        else:
            char["mixed_decor"] = ["夢", "ψυχή", "мир", "จันทร์"]
        print(f"🎲 Schitzo mode: {char['name']} ({char['from']}) — {char['catchphrase']}")
    elif args.vibe:
        char = find_character(args.vibe)
    else:
        parser.error("Either --vibe or --schitzo is required")

    print(f"\nThemed: {char['name']} ({char['from']}) — {char['catchphrase']}")

    # Generate skin with decorative scripts
    skin_name = f"{args.profile}_{args.main[1:]}"
    
    # Get decorative glyphs
    decor = char.get("mixed_decor", char.get("decorative_glyphs", ["◆", "◇", "○"]))
    decor_str = " ".join(decor)
    wing_left = decor[0] if len(decor) > 0 else "⟨"
    wing_right = decor[-1] if len(decor) > 1 else "⟩"
    
    skin = f"""name: {skin_name}
description: {char['name']} — {char['catchphrase']}

colors:
  banner_border: "{args.main}"
  banner_title: "{args.main}"
  banner_accent: "{args.accent}"
  ui_accent: "{args.accent}"
  input_rule: "{args.main}"
  response_border: "{args.accent}"
  session_label: "{args.accent}"
  status_bar_bg: "{args.main}"
  ui_label: "{args.accent}"
  session_border: "{args.accent}"

spinner:
  waiting_faces: ["{char['emoji']}", "{char['emoji']*2}", "{char['emoji']*3}"]
  thinking_faces: ["{wing_left}", "{wing_right}", "{decor[1] if len(decor) > 1 else '◇'}", "{decor[2] if len(decor) > 2 else '○'}"]
  thinking_verbs: {json.dumps(char['verbs'])}
  wings: [["{wing_left} ", " {wing_right}"], ["{decor[1] if len(decor) > 1 else '◇'} ", " {decor[-1] if len(decor) > 1 else '◇'}"]]

branding:
  agent_name: "{char['name']}"
  welcome: "{char['native_greeting']} — {char['catchphrase']}"
  response_label: " {wing_left} {char['name']} {wing_right} "
  prompt_symbol: "{char['emoji']}"

# Banner with native script + decorative glyphs
banner_logo: |
  {decor_str}
  [#{args.accent[1:]}]{char['native_greeting']}[/] — [#{args.main[1:]}]{char['name']}[/]

tool_prefix: "┊"

tool_emojis:
  terminal: "{decor[0] if len(decor) > 0 else '◇'}"
  web_search: "{decor[1] if len(decor) > 1 else '◇'}"
  read_file: "{decor[2] if len(decor) > 2 else '◇'}"
"""

    os.makedirs(SKINS_DIR, exist_ok=True)
    skin_path = os.path.join(SKINS_DIR, f"{skin_name}.yaml")
    with open(skin_path, 'w') as f:
        f.write(skin)

    # Generate SOUL
    soul = f"""# Personality

You are {char['name']}. {char['native_greeting']} — {char['catchphrase']}

## Style
- Inhabit the voice of {char['name']} fully
- You hail from {char['country']}
- {args.vibe}

## What to avoid
- Breaking character
- Being generic or bland
- Forgetting who you are
"""

    soul_path = os.path.join(PROFILES_DIR, args.profile, "SOUL.md")
    os.makedirs(os.path.dirname(soul_path), exist_ok=True)
    with open(soul_path, 'w') as f:
        f.write(soul)

    # Generate iTerm profile
    def hex_to_rgb(h):
        return int(h[1:3], 16)/255, int(h[3:5], 16)/255, int(h[5:7], 16)/255

    r, g, b = hex_to_rgb(args.main)
    iterm = {"Profiles": [{
        "Name": args.profile,
        "Command": f"hermes -p {args.profile} chat",
        "Initial Text": f"/skin {skin_name}\\n",
        "Tab Color": {"Red Component": r, "Green Component": g, "Blue Component": b}
    }]}
    if args.workarea:
        iterm["Profiles"][0]["Custom Directory"] = "Yes"
        iterm["Profiles"][0]["Directory"] = args.workarea

    iterm_path = os.path.join(ITERM_DIR, f"hermes-{args.profile}.json")
    with open(iterm_path, 'w') as f:
        json.dump(iterm, f, indent=2)

    print(f"\n✨ {args.profile} themed as {char['name']}")
    print(f"   Skin:    ~/.hermes/skins/{skin_name}.yaml")
    print(f"   SOUL:    ~/.hermes/profiles/{args.profile}/SOUL.md")
    print(f"   iTerm:   DynamicProfiles/hermes-{args.profile}.json")
    print(f"   Launch:  hermes -p {args.profile} chat")
    print(f"\n   Then:    hermes profile alias {args.profile} --name <short_name>")


if __name__ == "__main__":
    main()
