# crafting.py


class Workshop:
    """
    Crafting and equipment upgrade system.

    Recipes:
      - Healing Tonic:
            herbs x1 + mushrooms x1

      - Tempered Edge:
            ore x2 + 30g
            increases weapon tier by 1

      - Reinforced Plate:
            ore x2 + driftwood x1 + 30g
            increases armor tier by 1

      - Shield Boss:
            ore x1 + 20g
            increases shield tier by 1

    Equipment upgrades are currently capped at Tier 3.
    """

    MAX_EQUIPMENT_TIER = 3

    def __init__(self, player, inventory):
        self.player = player
        self.inventory = inventory

    def menu(self):
        """Display the Workshop crafting menu."""

        while True:
            print("\n-- Workshop (Crafting) --")
            print(f"Gold: {self.player.gold}")

            print(
                "1) Brew Healing Tonic "
                "[herbs x1 + mushrooms x1]"
            )

            print(
                "2) Tempered Edge "
                "(+1 weapon tier) "
                "[ore x2 + 30g]"
            )

            print(
                "3) Reinforced Plate "
                "(+1 armor tier) "
                "[ore x2 + driftwood x1 + 30g]"
            )

            print(
                "4) Shield Boss "
                "(+1 shield tier) "
                "[ore x1 + 20g]"
            )

            print("0) Leave")

            choice = input("> ").strip()

            if choice == "0":
                return

            if choice == "1":
                self._brew_healing_tonic()

            elif choice == "2":
                self._upgrade_weapon()

            elif choice == "3":
                self._upgrade_armor()

            elif choice == "4":
                self._upgrade_shield()

            else:
                print("Invalid choice.")

    # ============================================================
    # CONSUMABLES
    # ============================================================

    def _brew_healing_tonic(self):
        """Craft one Healing Tonic."""

        herbs = self.inventory.count("herbs")
        mushrooms = self.inventory.count("mushrooms")

        if herbs < 1 or mushrooms < 1:
            print(
                "You need herbs x1 and "
                "mushrooms x1."
            )
            return

        self.inventory.remove("herbs", 1)
        self.inventory.remove("mushrooms", 1)

        self.inventory.add(
            "Healing Tonic",
            1
        )

        print("Brewed a Healing Tonic.")

    # ============================================================
    # EQUIPMENT UPGRADES
    # ============================================================

    def _upgrade_weapon(self):
        """Increase weapon tier by one."""

        if (
            self.player.weapon_tier
            >= self.MAX_EQUIPMENT_TIER
        ):
            print(
                "Your weapon is already "
                "at the maximum tier."
            )
            return

        if (
            self.inventory.count("ore") < 2
            or self.player.gold < 30
        ):
            print(
                "You need ore x2 and "
                "30 gold."
            )
            return

        self.inventory.remove("ore", 2)
        self.player.gold -= 30

        self.player.weapon_tier += 1

        print(
            "Your weapon is tempered. "
            f"(Tier {self.player.weapon_tier})"
        )

    def _upgrade_armor(self):
        """Increase armor tier by one."""

        if (
            self.player.armor_tier
            >= self.MAX_EQUIPMENT_TIER
        ):
            print(
                "Your armor is already "
                "at the maximum tier."
            )
            return

        if (
            self.inventory.count("ore") < 2
            or self.inventory.count("driftwood") < 1
            or self.player.gold < 30
        ):
            print(
                "You need ore x2, "
                "driftwood x1, and 30 gold."
            )
            return

        self.inventory.remove("ore", 2)
        self.inventory.remove(
            "driftwood",
            1
        )

        self.player.gold -= 30
        self.player.armor_tier += 1

        print(
            "Your armor is reinforced. "
            f"(Tier {self.player.armor_tier})"
        )

    def _upgrade_shield(self):
        """Increase shield tier by one."""

        if (
            self.player.shield_tier
            >= self.MAX_EQUIPMENT_TIER
        ):
            print(
                "Your shield is already "
                "at the maximum tier."
            )
            return

        if (
            self.inventory.count("ore") < 1
            or self.player.gold < 20
        ):
            print(
                "You need ore x1 and "
                "20 gold."
            )
            return

        self.inventory.remove("ore", 1)
        self.player.gold -= 20

        self.player.shield_tier += 1

        print(
            "Your shield is upgraded. "
            f"(Tier {self.player.shield_tier})"
        )