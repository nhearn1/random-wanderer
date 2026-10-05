# devtools.py


class DeveloperTools:
    """
    Developer/testing utilities.

    These tools bypass normal game progression and are intended
    only for testing mechanics during development.
    """

    def __init__(self, player, inventory):
        self.player = player
        self.inventory = inventory

    # ============================================================
    # MAIN MENU
    # ============================================================

    def menu(self):
        while True:
            print("\n=== DEVELOPER MENU ===")

            print(
                f"Player: {self.player.name} | "
                f"Lv {self.player.level} | "
                f"{self.player.role}"
            )

            print("1) Set Level")
            print("2) Set Class")
            print("3) Restore HP / Resource")
            print("4) Add Gold")
            print("5) Add Crafting Materials")
            print("6) Set Equipment Tiers")
            print("7) Show Character Stats")
            print("0) Back")

            choice = input("> ").strip()

            if choice == "0":
                return

            if choice == "1":
                self._set_level()

            elif choice == "2":
                self._set_class()

            elif choice == "3":
                self._restore()

            elif choice == "4":
                self._add_gold()

            elif choice == "5":
                self._add_materials()

            elif choice == "6":
                self._set_equipment()

            elif choice == "7":
                self.player.show_stats()

            else:
                print("Invalid choice.")

    # ============================================================
    # LEVEL
    # ============================================================

    def _set_level(self):
        try:
            level = int(
                input(
                    "Set level to: "
                ).strip()
            )

        except ValueError:
            print("Enter a valid number.")
            return

        if level < 1:
            print("Level must be at least 1.")
            return

        self.player.level = level
        self.player.xp = 0

        print(
            f"Level set to "
            f"{self.player.level}."
        )

        # If we move below class level, reset to Wanderer.
        if level < 5:
            self._reset_class()

    # ============================================================
    # CLASS
    # ============================================================

    def _set_class(self):
        if self.player.level < 5:
            print(
                "Set the player to at least "
                "Level 5 first."
            )
            return

        print("\nChoose test class:")
        print("1) Warrior")
        print("2) Mage")
        print("3) Rogue")
        print("0) Cancel")

        choice = input("> ").strip()

        if choice == "0":
            return

        # Remove previous class bonuses before
        # applying a different test class.
        self._reset_class()

        if choice == "1":
            self.player.role = "Warrior"

            self.player.max_hp += 10
            self.player.defense += 1

            self.player.resource_type = "Energy"
            self.player.max_resource = 100

        elif choice == "2":
            self.player.role = "Mage"

            self.player.max_hp = max(
                1,
                self.player.max_hp - 5
            )

            self.player.attack += 2

            self.player.resource_type = "Mana"
            self.player.max_resource = 100

        elif choice == "3":
            self.player.role = "Rogue"

            self.player.max_hp += 5
            self.player.attack += 1

            self.player.resource_type = "Energy"
            self.player.max_resource = 100

        else:
            print("Invalid choice.")
            return

        self.player.class_selected = True

        self.player.hp = self.player.max_hp
        self.player.resource = self.player.max_resource

        print(
            f"Test class set to "
            f"{self.player.role}."
        )

    def _reset_class(self):
        """
        Remove class-specific bonuses and return the player
        to Wanderer state.

        This only reverses the bonuses applied when selecting
        the base class. Normal level-up stat gains remain.
        """

        if self.player.role == "Warrior":
            self.player.max_hp = max(
                1,
                self.player.max_hp - 10
            )

            self.player.defense = max(
                0,
                self.player.defense - 1
            )

        elif self.player.role == "Mage":
            self.player.max_hp += 5

            self.player.attack = max(
                1,
                self.player.attack - 2
            )

        elif self.player.role == "Rogue":
            self.player.max_hp = max(
                1,
                self.player.max_hp - 5
            )

            self.player.attack = max(
                1,
                self.player.attack - 1
            )

        self.player.role = "Wanderer"
        self.player.class_selected = False

        self.player.resource_type = None
        self.player.resource = 0
        self.player.max_resource = 0

        self.player.cooldowns.clear()
        self.player.status_effects.clear()

        self.player.guard_active = False
        self.player.dodge_bonus = 0.0

        self.player.hp = min(
            self.player.hp,
            self.player.max_hp
        )

    # ============================================================
    # RESTORE
    # ============================================================

    def _restore(self):
        self.player.hp = self.player.max_hp

        if self.player.resource_type:
            self.player.resource = (
                self.player.max_resource
            )

        self.player.cooldowns.clear()
        self.player.status_effects.clear()

        self.player.guard_active = False
        self.player.dodge_bonus = 0.0

        print("HP fully restored.")

        if self.player.resource_type:
            print(
                f"{self.player.resource_type} "
                "fully restored."
            )

        print(
            "Temporary combat effects cleared."
        )

    # ============================================================
    # GOLD
    # ============================================================

    def _add_gold(self):
        try:
            amount = int(
                input(
                    "Gold to add: "
                ).strip()
            )

        except ValueError:
            print("Enter a valid number.")
            return

        if amount < 0:
            print(
                "Use a positive number."
            )
            return

        self.player.gold += amount

        print(
            f"Added {amount} gold. "
            f"Total: {self.player.gold}"
        )

    # ============================================================
    # MATERIALS
    # ============================================================

    def _add_materials(self):
        try:
            amount = int(
                input(
                    "Amount of each material "
                    "to add: "
                ).strip()
            )

        except ValueError:
            print("Enter a valid number.")
            return

        if amount <= 0:
            print(
                "Amount must be greater "
                "than zero."
            )
            return

        materials = [
            "herbs",
            "mushrooms",
            "ore",
            "driftwood",
        ]

        for material in materials:
            self.inventory.add(
                material,
                amount
            )

        print(
            f"Added {amount} of each "
            "crafting material."
        )

    # ============================================================
    # EQUIPMENT
    # ============================================================

    def _set_equipment(self):
        print(
            "\nEnter equipment tiers "
            "(0-3)."
        )

        try:
            weapon = int(
                input(
                    "Weapon tier: "
                ).strip()
            )

            armor = int(
                input(
                    "Armor tier: "
                ).strip()
            )

            shield = int(
                input(
                    "Shield tier: "
                ).strip()
            )

        except ValueError:
            print(
                "Equipment tiers must "
                "be numbers."
            )
            return

        tiers = [
            weapon,
            armor,
            shield,
        ]

        if any(
            tier < 0 or tier > 3
            for tier in tiers
        ):
            print(
                "Equipment tiers must "
                "be between 0 and 3."
            )
            return

        self.player.weapon_tier = weapon
        self.player.armor_tier = armor
        self.player.shield_tier = shield

        print(
            "Equipment tiers updated:"
        )

        print(
            f"Weapon {weapon} | "
            f"Armor {armor} | "
            f"Shield {shield}"
        )