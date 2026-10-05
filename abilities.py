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

        "critical_strike": {
            "name": "Critical Strike",
            "level": 10,
            "type": "active",
            "cost": 45,
            "cooldown": 2,
            "description": (
                "A devastating melee attack with massive damage "
                "but reduced accuracy."
            ),
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

        "greater_heal": {
            "name": "Greater Heal",
            "level": 10,
            "type": "active",
            "cost": 40,
            "cooldown": 2,
            "description": "Restore a large portion of your HP.",
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

        "vanish": {
            "name": "Vanish",
            "level": 10,
            "type": "active",
            "cost": 30,
            "cooldown": 3,
            "description": (
                "Evade the next enemy attack and empower "
                "your next Sneak Attack."
            ),
        },

        "poison_blade": {
            "name": "Poison Blade",
            "level": 10,
            "type": "active",
            "cost": 25,
            "cooldown": 2,
            "description": (
                "Strike an enemy and poison it for three turns."
            ),
        },
    },
}