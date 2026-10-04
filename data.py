
# data.py
# Regions now reveal/select based on story_stage_req
REGIONS = {
    "woods":     {"desc": "Tall trees and dappled light. You hear distant chittering.", "story_stage_req": 0,
                  "monsters": ["goblin", "giant spider", "bear", "bat"]},
    "beach":     {"desc": "Waves crash against the shore; gulls circle overhead.", "story_stage_req": 2,
                  "monsters": ["bandit", "bat", "goblin"]},
    "plains":    {"desc": "Sweeping grasslands and scattered stones.", "story_stage_req": 3,
                  "monsters": ["skeleton", "orc", "bandit"]},
    "mountains": {"desc": "Thin air, rocky paths, and looming peaks.", "story_stage_req": 4,
                  "monsters": ["dark mage", "orc", "bear"]},
    "citadel":   {"desc": "The Shadow Lord's fortress looms beyond a torn sky.", "story_stage_req": 5,
                  "monsters": ["dark mage", "orc", "giant spider", "skeleton", "bandit", "shadow lord"]},
}

# Monsters (baseline + bosses). Adjust numbers to tune difficulty later.
MONSTERS = {
    "goblin":        {"hp": 9,  "atk": 3, "def": 1, "xp": 7,  "gold": (3, 8),   "drop": "goblin ear",  "hp_per_level": 1.0,  "atk_per_level": 0.3, "def_per_level": 0.1},
    "bat":           {"hp": 7,  "atk": 2, "def": 1, "xp": 6,  "gold": (1, 4),   "drop": "bat wing",    "hp_per_level": 1.0,  "atk_per_level": 0.3, "def_per_level": 0.1},
    "skeleton":      {"hp": 12, "atk": 3, "def": 2, "xp": 10, "gold": (3, 7),   "drop": "bone shard",  "hp_per_level": 1.5,  "atk_per_level": 0.4, "def_per_level": 0.15},
    "bandit":        {"hp": 11, "atk": 3, "def": 2, "xp": 11, "gold": (5, 12),  "drop": "bandit token","hp_per_level": 1.5,  "atk_per_level": 0.4, "def_per_level": 0.15},
    "giant spider":  {"hp": 13, "atk": 4, "def": 2, "xp": 12, "gold": (5, 11),  "drop": "spider fang", "hp_per_level": 1.5,  "atk_per_level": 0.4, "def_per_level": 0.15},
    "orc":           {"hp": 16, "atk": 4, "def": 2, "xp": 16, "gold": (6, 14),  "drop": "orc tusk",    "hp_per_level": 2.0,  "atk_per_level": 0.5, "def_per_level": 0.2},
    "bear":          {"hp": 20, "atk": 5, "def": 3, "xp": 20, "gold": (8, 16),  "drop": "bear claw",   "hp_per_level": 2.0,  "atk_per_level": 0.5, "def_per_level": 0.2},
    "dark mage":     {"hp": 14, "atk": 6, "def": 1, "xp": 18, "gold": (6, 12),  "drop": "shadow essence","hp_per_level": 2.0, "atk_per_level": 0.6, "def_per_level": 0.2},
    # Citadel boss for free-roam
    "shadow lord":   {"hp": 26, "atk": 8, "def": 3, "xp": 60, "gold": (20, 40), "drop": None,
                      "hp_per_level": 3.0, "atk_per_level": 0.8, "def_per_level": 0.3},
    # Story bosses
    "corrupted alpha bear": {"hp": 28, "atk": 7, "def": 3, "xp": 45, "gold": (15, 30),
                             "drop": None, "hp_per_level": 2.5, "atk_per_level": 0.6, "def_per_level": 0.25},
    "pirate warlord":       {"hp": 30, "atk": 8, "def": 3, "xp": 50, "gold": (18, 35),
                             "drop": None, "hp_per_level": 2.7, "atk_per_level": 0.7, "def_per_level": 0.25},
    "undead chieftain":     {"hp": 32, "atk": 8, "def": 4, "xp": 55, "gold": (18, 35),
                             "drop": None, "hp_per_level": 2.8, "atk_per_level": 0.7, "def_per_level": 0.3},
    "dark mage general":    {"hp": 26, "atk":10, "def": 3, "xp": 60, "gold": (20, 40),
                             "drop": "shadow essence", "hp_per_level": 2.6, "atk_per_level": 0.9, "def_per_level": 0.25},
    "trial knight":         {"hp": 34, "atk": 9, "def": 5, "xp": 65, "gold": (22, 42),
                             "drop": None, "hp_per_level": 3.0, "atk_per_level": 0.8, "def_per_level": 0.4},
    "corruption avatar":    {"hp": 36, "atk":11, "def": 5, "xp": 70, "gold": (25, 50),
                             "drop": None, "hp_per_level": 3.2, "atk_per_level": 1.0, "def_per_level": 0.45},
    "kaelen":               {"hp": 33, "atk":12, "def": 6, "xp": 75, "gold": (25, 50),
                             "drop": None, "hp_per_level": 3.0, "atk_per_level": 1.0, "def_per_level": 0.5},
}

# Sell values (unchanged — used by shops)
DROP_SELL_VALUES = {
    "goblin ear": 6, "bone shard": 8, "orc tusk": 14, "shadow essence": 20,
    "bandit token": 10, "bat wing": 4, "bear claw": 16, "spider fang": 12,
}
RESOURCE_SELL_VALUES = {"herbs": 6, "ore": 12, "driftwood": 4, "mushrooms": 8}
SELL_VALUES = {**DROP_SELL_VALUES, **RESOURCE_SELL_VALUES}
