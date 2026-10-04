"""Class ability definitions and shared ability data."""


ABILITIES = {
    # ============================================================
    # WARRIOR
    # ============================================================
    "Warrior": {
        "guard": {
            "name": "Guard",
            "level": 5,
            "type": "active",
            "cost": 20,
            "cooldown": 0,
            "description": "Reduce damage from the next incoming attack.",
        },

        "mighty_strike": {
            "name": "Mighty Strike",
            "level": 5,
            "type": "active",
            "cost": 25,
            "cooldown": 0,
            "description": "Deliver a powerful melee attack.",
        },

        "improved_fighting_stance": {
            "name": "Improved Fighting Stance",
            "level": 7,
            "type": "passive",
            "cost": 0,
            "cooldown": 0,
            "description": "Passively increases damage and defense.",
        },
    },

    # ============================================================
    # MAGE
    # ============================================================
    "Mage": {
        "small_heal": {
            "name": "Small Heal",
            "level": 5,
            "type": "active",
            "cost": 20,
            "cooldown": 0,
            "description": "Restore a portion of your HP.",
        },

        "fire_bolt": {
            "name": "Fire Bolt",
            "level": 5,
            "type": "active",
            "cost": 15,
            "cooldown": 0,
            "description": "Launch a magical attack at one enemy.",
        },

        "lightning_bolt": {
            "name": "Lightning Bolt",
            "level": 7,
            "type": "active",
            "cost": 30,
            "cooldown": 2,
            "description": "Strike one enemy with powerful lightning.",
        },
    },

    # ============================================================
    # ROGUE
    # ============================================================
    "Rogue": {
        "sneak_attack": {
            "name": "Sneak Attack",
            "level": 5,
            "type": "active",
            "cost": 30,
            "cooldown": 0,
            "description": (
                "Deal increased damage, especially on the opening turn."
            ),
        },

        "nimble_feet": {
            "name": "Nimble Feet",
            "level": 5,
            "type": "active",
            "cost": 20,
            "cooldown": 0,
            "description": "Temporarily improve your chance to dodge attacks.",
        },

        "double_strike": {
            "name": "Double Strike",
            "level": 7,
            "type": "active",
            "cost": 35,
            "cooldown": 1,
            "description": "Attack the same enemy twice in rapid succession.",
        },
    },
}