"""Class ability definitions and shared ability data."""

ABILITIES = {
    "Warrior": {
        "guard": {
            "name": "Guard",
            "level": 5,
            "cost": 20,
            "cooldown": 0,
            "description": "Reduce damage from the next incoming attack.",
        },
        "mighty_strike": {
            "name": "Mighty Strike",
            "level": 5,
            "cost": 25,
            "cooldown": 0,
            "description": "Deliver a powerful melee attack.",
        },
    },

    "Mage": {
        "small_heal": {
            "name": "Small Heal",
            "level": 5,
            "cost": 20,
            "cooldown": 0,
            "description": "Restore a portion of your HP.",
        },
        "fire_bolt": {
            "name": "Fire Bolt",
            "level": 5,
            "cost": 15,
            "cooldown": 0,
            "description": "Launch a magical attack at one enemy.",
        },
    },

    "Rogue": {
        "sneak_attack": {
            "name": "Sneak Attack",
            "level": 5,
            "cost": 30,
            "cooldown": 0,
            "description": "Deal increased damage, especially on the opening turn.",
        },
        "nimble_feet": {
            "name": "Nimble Feet",
            "level": 5,
            "cost": 20,
            "cooldown": 0,
            "description": "Temporarily improve your chance to dodge attacks.",
        },
    },
}