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

    def __init__(
        self,
        player,
        inventory,
    ):
        self.player = player
        self.inventory = inventory

    # ============================================================
    # GUI-SAFE RECIPE INFORMATION
    # ============================================================

    def get_recipes(self):
        """
        Return the current Workshop recipes.

        These dictionaries are presentation-safe and may be used
        by either a graphical interface or another non-CLI system.
        """

        return [
            {
                "key": "healing_tonic",
                "name": "Healing Tonic",
                "description": (
                    "Brew a restorative tonic."
                ),
                "requirements": (
                    "herbs x1 + mushrooms x1"
                ),
                "action": "Craft",
            },
            {
                "key": "weapon",
                "name": "Tempered Edge",
                "description": (
                    "Increase weapon tier by 1."
                ),
                "requirements": (
                    "ore x2 + 30g"
                ),
                "action": "Upgrade",
            },
            {
                "key": "armor",
                "name": "Reinforced Plate",
                "description": (
                    "Increase armor tier by 1."
                ),
                "requirements": (
                    "ore x2 + driftwood x1 + 30g"
                ),
                "action": "Upgrade",
            },
            {
                "key": "shield",
                "name": "Shield Boss",
                "description": (
                    "Increase shield tier by 1."
                ),
                "requirements": (
                    "ore x1 + 20g"
                ),
                "action": "Upgrade",
            },
        ]

    def get_material_counts(self):
        """Return Workshop-relevant inventory quantities."""

        return {
            "herbs": self.inventory.count(
                "herbs"
            ),
            "mushrooms": self.inventory.count(
                "mushrooms"
            ),
            "ore": self.inventory.count(
                "ore"
            ),
            "driftwood": self.inventory.count(
                "driftwood"
            ),
        }

    def get_recipe_status(
        self,
        recipe_key,
    ):
        """
        Return whether a recipe can currently be completed.

        This does not mutate the player or inventory.
        """

        if recipe_key == "healing_tonic":

            can_craft = (
                self.inventory.count("herbs") >= 1
                and self.inventory.count(
                    "mushrooms"
                ) >= 1
            )

            return {
                "available": can_craft,
                "maxed": False,
            }

        if recipe_key == "weapon":

            maxed = (
                self.player.weapon_tier
                >= self.MAX_EQUIPMENT_TIER
            )

            can_craft = (
                not maxed
                and self.inventory.count("ore") >= 2
                and self.player.gold >= 30
            )

            return {
                "available": can_craft,
                "maxed": maxed,
            }

        if recipe_key == "armor":

            maxed = (
                self.player.armor_tier
                >= self.MAX_EQUIPMENT_TIER
            )

            can_craft = (
                not maxed
                and self.inventory.count("ore") >= 2
                and self.inventory.count(
                    "driftwood"
                ) >= 1
                and self.player.gold >= 30
            )

            return {
                "available": can_craft,
                "maxed": maxed,
            }

        if recipe_key == "shield":

            maxed = (
                self.player.shield_tier
                >= self.MAX_EQUIPMENT_TIER
            )

            can_craft = (
                not maxed
                and self.inventory.count("ore") >= 1
                and self.player.gold >= 20
            )

            return {
                "available": can_craft,
                "maxed": maxed,
            }

        return {
            "available": False,
            "maxed": False,
        }

    # ============================================================
    # GUI-SAFE CRAFTING
    # ============================================================

    def craft(self, recipe_key):
        """
        Attempt to complete a Workshop recipe.

        Returns a result dictionary instead of requesting terminal
        input. Both the CLI and GUI use this method so the crafting
        rules remain identical.
        """

        if recipe_key == "healing_tonic":
            return self._brew_healing_tonic()

        if recipe_key == "weapon":
            return self._upgrade_weapon()

        if recipe_key == "armor":
            return self._upgrade_armor()

        if recipe_key == "shield":
            return self._upgrade_shield()

        return {
            "success": False,
            "message": "Unknown Workshop recipe.",
        }

    # ============================================================
    # CONSUMABLES
    # ============================================================

    def _brew_healing_tonic(self):
        """Craft one Healing Tonic."""

        herbs = self.inventory.count(
            "herbs"
        )

        mushrooms = self.inventory.count(
            "mushrooms"
        )

        if (
            herbs < 1
            or mushrooms < 1
        ):
            return {
                "success": False,
                "message": (
                    "You need herbs x1 and "
                    "mushrooms x1."
                ),
            }

        self.inventory.remove(
            "herbs",
            1,
        )

        self.inventory.remove(
            "mushrooms",
            1,
        )

        self.inventory.add(
            "Healing Tonic",
            1,
        )

        return {
            "success": True,
            "message": (
                "Brewed a Healing Tonic."
            ),
        }

    # ============================================================
    # EQUIPMENT UPGRADES
    # ============================================================

    def _upgrade_weapon(self):
        """Increase weapon tier by one."""

        if (
            self.player.weapon_tier
            >= self.MAX_EQUIPMENT_TIER
        ):
            return {
                "success": False,
                "message": (
                    "Your weapon is already "
                    "at the maximum tier."
                ),
            }

        if (
            self.inventory.count("ore") < 2
            or self.player.gold < 30
        ):
            return {
                "success": False,
                "message": (
                    "You need ore x2 and "
                    "30 gold."
                ),
            }

        self.inventory.remove(
            "ore",
            2,
        )

        self.player.gold -= 30

        self.player.weapon_tier += 1

        return {
            "success": True,
            "message": (
                "Your weapon is tempered. "
                f"(Tier "
                f"{self.player.weapon_tier})"
            ),
        }

    def _upgrade_armor(self):
        """Increase armor tier by one."""

        if (
            self.player.armor_tier
            >= self.MAX_EQUIPMENT_TIER
        ):
            return {
                "success": False,
                "message": (
                    "Your armor is already "
                    "at the maximum tier."
                ),
            }

        if (
            self.inventory.count("ore") < 2
            or self.inventory.count(
                "driftwood"
            ) < 1
            or self.player.gold < 30
        ):
            return {
                "success": False,
                "message": (
                    "You need ore x2, "
                    "driftwood x1, and "
                    "30 gold."
                ),
            }

        self.inventory.remove(
            "ore",
            2,
        )

        self.inventory.remove(
            "driftwood",
            1,
        )

        self.player.gold -= 30

        self.player.armor_tier += 1

        return {
            "success": True,
            "message": (
                "Your armor is reinforced. "
                f"(Tier "
                f"{self.player.armor_tier})"
            ),
        }

    def _upgrade_shield(self):
        """Increase shield tier by one."""

        if (
            self.player.shield_tier
            >= self.MAX_EQUIPMENT_TIER
        ):
            return {
                "success": False,
                "message": (
                    "Your shield is already "
                    "at the maximum tier."
                ),
            }

        if (
            self.inventory.count("ore") < 1
            or self.player.gold < 20
        ):
            return {
                "success": False,
                "message": (
                    "You need ore x1 and "
                    "20 gold."
                ),
            }

        self.inventory.remove(
            "ore",
            1,
        )

        self.player.gold -= 20

        self.player.shield_tier += 1

        return {
            "success": True,
            "message": (
                "Your shield is upgraded. "
                f"(Tier "
                f"{self.player.shield_tier})"
            ),
        }

    # ============================================================
    # CLI MENU
    # ============================================================

    def menu(self):
        """Display the Workshop crafting menu."""

        while True:

            print(
                "\n-- Workshop (Crafting) --"
            )

            print(
                f"Gold: {self.player.gold}"
            )

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

            choice = input(
                "> "
            ).strip()

            if choice == "0":
                return

            recipe_map = {
                "1": "healing_tonic",
                "2": "weapon",
                "3": "armor",
                "4": "shield",
            }

            recipe_key = recipe_map.get(
                choice
            )

            if recipe_key is None:

                print(
                    "Invalid choice."
                )

                continue

            result = self.craft(
                recipe_key
            )

            print(
                result["message"]
            )