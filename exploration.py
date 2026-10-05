# exploration.py

import random

from data import REGIONS, MONSTERS
from enemy import Enemy
from combat import fight


class Explorer:
    """Handle region selection, exploration, encounters, and rewards."""

    def __init__(self, player, inventory):
        self.player = player
        self.inventory = inventory

        self.current_region = "woods"

        self._rest_streak = 0
        self._monster_chance = 0.6

    # ============================================================
    # REGION HELPERS
    # ============================================================

    def get_current_region(self):
        """Return the data for the currently selected region."""

        return REGIONS[self.current_region]

    def get_available_regions(self):
        """
        Return region information with unlock state.

        GUI code can use this without relying on terminal input.
        """

        regions = []

        for key, info in REGIONS.items():

            required_stage = info.get(
                "story_stage_req",
                0,
            )

            unlocked = (
                self.player.story_stage
                >= required_stage
            )

            regions.append(
                {
                    "key": key,
                    "info": info,
                    "unlocked": unlocked,
                }
            )

        return regions

    def set_region(self, region_key):
        """
        Change region if it exists and is unlocked.

        Return True when the change succeeds.
        """

        if region_key not in REGIONS:
            return False

        region = REGIONS[region_key]

        required_stage = region.get(
            "story_stage_req",
            0,
        )

        if (
            self.player.story_stage
            < required_stage
        ):
            return False

        self.current_region = region_key

        return True

    # ============================================================
    # CLI REGION SELECTION
    # ============================================================

    def choose_region(self):
        """Original terminal-based region selection."""

        print("\nChoose a region:")

        display_options = []

        for region_data in (
            self.get_available_regions()
        ):

            key = region_data["key"]
            info = region_data["info"]
            unlocked = region_data[
                "unlocked"
            ]

            if unlocked:

                display_options.append(
                    (
                        "region",
                        key,
                        (
                            f"{key.title()} — "
                            f"{info['desc']}"
                        ),
                    )
                )

            else:

                display_options.append(
                    (
                        "locked",
                        key,
                        "????? — [Locked]",
                    )
                )

        for index, (
            _,
            _,
            label,
        ) in enumerate(
            display_options,
            start=1,
        ):

            print(
                f"{index}) {label}"
            )

        print("0) Stay here")

        choice = input("> ").strip()

        if choice == "0":
            return

        try:

            index = int(choice) - 1

            if (
                0
                <= index
                < len(display_options)
            ):

                kind, key, _ = (
                    display_options[index]
                )

                if kind == "locked":

                    print(
                        "That destination is "
                        "unknown for now."
                    )

                    return

                if self.set_region(key):

                    print(
                        "You head to the "
                        f"{self.current_region.title()}."
                    )

        except ValueError:

            print(
                "Staying where you are."
            )

    # ============================================================
    # CLI EXPLORATION LOOP
    # ============================================================

    def explore_loop(self):
        """Original terminal exploration loop."""

        region = self.get_current_region()

        print(
            "\nExploring the "
            f"{self.current_region.title()}... "
            "(press Q to return)"
        )

        while True:

            print(
                "[E]ncounter  "
                "[L]ook  "
                "[S]tats  "
                "[V]Inventory  "
                "[R]est  "
                "[Q]uit explore > ",
                end="",
            )

            command = (
                input("")
                .strip()
                .lower()
            )

            if command == "q":

                self.reset_exploration_state()
                break

            elif command == "l":

                print(
                    region["desc"]
                )

                continue

            elif command == "s":

                self.player.show_stats()
                continue

            elif command == "v":

                self.inventory.show(
                    self.player
                )

                continue

            elif command == "r":

                self._handle_rest_with_ambush(
                    region
                )

                continue

            # Default action remains an encounter.
            self._rest_streak = 0

            self.random_encounter(
                region
            )

    # ============================================================
    # SHARED EXPLORATION STATE
    # ============================================================

    def reset_exploration_state(self):
        """Reset temporary exploration probabilities."""

        self._rest_streak = 0
        self._monster_chance = 0.6

    # ============================================================
    # REST
    # ============================================================

    def calculate_rest_heal(self):
        """Return the amount of HP a rest attempts to heal."""

        return max(
            2,
            int(
                self.player.max_hp
                * 0.15
            ),
        )

    def rest(self):
        """
        Perform a rest without starting combat.

        This method is GUI-safe.

        Returns a dictionary describing the result.
        """

        heal_amount = (
            self.calculate_rest_heal()
        )

        old_hp = self.player.hp

        self.player.hp = min(
            self.player.max_hp,
            self.player.hp
            + heal_amount,
        )

        healed = (
            self.player.hp
            - old_hp
        )

        self._rest_streak += 1

        base = 0.15

        extra = (
            0.15
            * (
                self._rest_streak
                - 1
            )
        )

        ambush_chance = min(
            0.75,
            base + extra,
        )

        ambushed = (
            random.random()
            < ambush_chance
        )

        if ambushed:

            self._rest_streak = 0
            self._monster_chance = 0.6

        return {
            "healed": healed,
            "ambushed": ambushed,
            "ambush_chance": (
                ambush_chance
            ),
        }

    def _handle_rest_with_ambush(
        self,
        region,
    ):
        """CLI wrapper around the shared rest rules."""

        result = self.rest()

        print(
            "You rest and recover "
            f"{result['healed']} HP. "
            f"({self.player.hp}/"
            f"{self.player.max_hp})"
        )

        if result["ambushed"]:

            print(
                "You are ambushed!"
            )

            self._spawn_and_fight(
                region
            )

        else:

            print(
                "...It stays quiet."
            )

    # ============================================================
    # ENCOUNTER ROLLING
    # ============================================================

    def roll_encounter(self):
        """
        Roll an exploration encounter without launching combat.

        GUI-safe.

        Returns:
            {
                "type": "monster" | "resource" | "nothing",
                ...
            }
        """

        self._rest_streak = 0

        roll = random.random()

        if (
            roll
            < self._monster_chance
        ):

            self._monster_chance = 0.6

            return {
                "type": "monster",
                "enemies": (
                    self.generate_encounter()
                ),
            }

        if (
            roll
            < self._monster_chance
            + 0.2
        ):

            resource = random.choice(
                [
                    "herbs",
                    "ore",
                    "driftwood",
                    "mushrooms",
                ]
            )

            self.inventory.add(
                resource,
                1,
            )

            self._monster_chance = min(
                0.9,
                self._monster_chance
                + 0.1,
            )

            return {
                "type": "resource",
                "resource": resource,
                "quantity": 1,
            }

        self._monster_chance = min(
            0.9,
            self._monster_chance
            + 0.1,
        )

        return {
            "type": "nothing",
        }

    def random_encounter(
        self,
        region=None,
    ):
        """CLI wrapper around the shared encounter roll."""

        if region is None:
            region = (
                self.get_current_region()
            )

        result = (
            self.roll_encounter()
        )

        if result["type"] == "monster":

            self._fight_enemies(
                result["enemies"]
            )

        elif result["type"] == "resource":

            print(
                "You found some "
                f"{result['resource']}."
            )

        else:

            print(
                "Nothing happens... "
                "you catch your breath."
            )

    # ============================================================
    # ENEMY GENERATION
    # ============================================================

    def generate_encounter(
        self,
        region=None,
    ):
        """
        Generate 1-3 scaled enemies without starting combat.

        This is the bridge used by the Pygame combat screen.
        """

        if region is None:

            region = (
                self.get_current_region()
            )

        # Preserve the original encounter-count probabilities.
        if random.random() < 0.6:

            count = 1

        elif random.random() < 0.7:

            count = 2

        else:

            count = 3

        chosen_names = [
            random.choice(
                region["monsters"]
            )
            for _ in range(count)
        ]

        return [
            self._scaled_enemy(name)
            for name in chosen_names
        ]

    def _scaled_enemy(
        self,
        monster_name,
    ):
        """Create an enemy scaled to the player's level."""

        monster = MONSTERS[
            monster_name
        ]

        level = max(
            1,
            self.player.level,
        )

        hp = int(
            monster["hp"]
            + monster.get(
                "hp_per_level",
                0,
            )
            * (
                level - 1
            )
        )

        attack = int(
            monster["atk"]
            + monster.get(
                "atk_per_level",
                0,
            )
            * (
                level - 1
            )
        )

        defense = int(
            monster["def"]
            + monster.get(
                "def_per_level",
                0,
            )
            * (
                level - 1
            )
        )

        return Enemy(
            name=monster_name,
            hp=hp,
            atk=attack,
            defense=defense,
            xp=monster.get(
                "xp",
                1,
            ),
            gold_range=monster.get(
                "gold",
                (1, 3),
            ),
            drop=monster.get(
                "drop",
                None,
            ),
        )

    # ============================================================
    # COMBAT REWARDS
    # ============================================================

    def award_victory_rewards(
        self,
        enemies,
    ):
        """
        Award post-combat gold and drops.

        XP is intentionally NOT awarded here because XP is granted
        when each enemy is defeated during combat.

        Returns reward information for GUI display.
        """

        total_gold = 0
        drops = []

        for enemy in enemies:

            if hasattr(
                enemy,
                "gold_range",
            ):

                total_gold += (
                    random.randint(
                        *enemy.gold_range
                    )
                )

            drop = getattr(
                enemy,
                "drop",
                None,
            )

            if drop:

                self.inventory.add(
                    drop,
                    1,
                )

                drops.append(
                    drop
                )

        self.player.gold += (
            total_gold
        )

        return {
            "gold": total_gold,
            "drops": drops,
        }

    # ============================================================
    # CLI COMBAT
    # ============================================================

    def _fight_enemies(
        self,
        enemies,
    ):
        """Run existing terminal combat for generated enemies."""

        outcome = fight(
            self.player,
            enemies,
            inventory=self.inventory,
        )

        if outcome == "won":

            rewards = (
                self.award_victory_rewards(
                    enemies
                )
            )

            if rewards["gold"]:

                print(
                    "You loot "
                    f"{rewards['gold']} gold."
                )

        elif outcome == "lost":

            print(
                "You wake up back in town "
                "with 1 HP..."
            )

            self.player.hp = 1

        return outcome

    def _spawn_and_fight(
        self,
        region=None,
    ):
        """
        Preserve the original CLI helper.

        Enemy generation is now separated from combat execution so
        the GUI can use the same generated enemies.
        """

        enemies = (
            self.generate_encounter(
                region
            )
        )

        return self._fight_enemies(
            enemies
        )