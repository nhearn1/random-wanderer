# quests.py

from data import REGIONS, MONSTERS


# ================================================================
# QUEST DATA
# ================================================================

QUESTS = [
    {
        "name": "Spider Season",
        "need": {
            "spider fang": 3,
        },
        "xp": 25,
        "gold": 55,
    },
    {
        "name": "Bones for the Shrine",
        "need": {
            "bone shard": 4,
        },
        "xp": 30,
        "gold": 65,
    },
    {
        "name": "Orc Troubles",
        "need": {
            "orc tusk": 2,
        },
        "xp": 35,
        "gold": 80,
    },
    {
        "name": "Shadow Studies",
        "need": {
            "shadow essence": 1,
        },
        "xp": 45,
        "gold": 95,
    },
]


# ================================================================
# QUEST BOARD
# ================================================================

class QuestBoard:

    def __init__(
        self,
        player,
        inventory,
    ):
        self.player = player
        self.inventory = inventory

        # Only one side quest may be active at a time.
        self.active = None

    # ============================================================
    # GUI-SAFE QUEST INFORMATION
    # ============================================================

    def get_available_quests(self):
        """
        Return all quests currently accessible to the player.

        Availability is based on whether the required monster drop
        can be obtained in a region unlocked by story progression.
        """

        return [
            quest
            for quest in QUESTS
            if self._quest_is_accessible(
                quest
            )
        ]

    def get_active_quest(self):
        """Return the active quest, or None."""

        return self.active

    def get_quest_progress(
        self,
        quest=None,
    ):
        """
        Return inventory progress toward a quest.

        If no quest is supplied, use the active quest.
        """

        if quest is None:
            quest = self.active

        if quest is None:
            return []

        progress = []

        for item, required in (
            quest["need"].items()
        ):

            have = self.inventory.count(
                item
            )

            progress.append(
                {
                    "item": item,
                    "have": have,
                    "required": required,
                    "complete": (
                        have >= required
                    ),
                }
            )

        return progress

    # ============================================================
    # GUI-SAFE QUEST ACTIONS
    # ============================================================

    def accept_quest(
        self,
        quest,
    ):
        """
        Attempt to accept a quest.

        Returns a result dictionary and does not request terminal
        input.
        """

        if self.active is not None:

            return {
                "success": False,
                "message": (
                    "You already have an "
                    "active quest."
                ),
            }

        if quest not in QUESTS:

            return {
                "success": False,
                "message": (
                    "That quest does not exist."
                ),
            }

        if not self._quest_is_accessible(
            quest
        ):

            return {
                "success": False,
                "message": (
                    "That quest is not "
                    "available yet."
                ),
            }

        self.active = quest

        return {
            "success": True,
            "message": (
                f"Accepted: "
                f"{quest['name']}"
            ),
        }

    def abandon_active(self):
        """
        Abandon the active quest.

        Collected items remain in inventory.
        """

        if self.active is None:

            return {
                "success": False,
                "message": (
                    "No active quest "
                    "to abandon."
                ),
            }

        quest_name = (
            self.active["name"]
        )

        self.active = None

        return {
            "success": True,
            "message": (
                f"Abandoned: "
                f"{quest_name}"
            ),
        }

    def can_turn_in(
        self,
        quest=None,
    ):
        """Return True if all quest requirements are met."""

        if quest is None:
            quest = self.active

        if quest is None:
            return False

        return all(
            self.inventory.count(item)
            >= qty
            for item, qty
            in quest["need"].items()
        )

    def turn_in_active(self):
        """
        Complete the active quest if requirements are met.

        Required items are removed, XP and gold are awarded,
        and the active quest is cleared.
        """

        if self.active is None:

            return {
                "success": False,
                "message": (
                    "No active quest."
                ),
            }

        if not self.can_turn_in(
            self.active
        ):

            return {
                "success": False,
                "message": (
                    "You don't have all "
                    "required items yet."
                ),
            }

        completed_quest = self.active

        for item, qty in (
            completed_quest[
                "need"
            ].items()
        ):

            self.inventory.remove(
                item,
                qty,
            )

        xp_reward = (
            completed_quest["xp"]
        )

        gold_reward = (
            completed_quest["gold"]
        )

        # Clear before gain_xp in case leveling triggers
        # another GUI state such as class selection.
        self.active = None

        self.player.gain_xp(
            xp_reward
        )

        self.player.gold += (
            gold_reward
        )

        return {
            "success": True,
            "message": (
                "Quest complete! "
                f"+{xp_reward} XP, "
                f"+{gold_reward} gold."
            ),
            "quest": completed_quest,
            "xp": xp_reward,
            "gold": gold_reward,
        }

    # ============================================================
    # QUEST ACCESSIBILITY
    # ============================================================

    def _quest_is_accessible(
        self,
        quest,
    ):
        """
        Determine whether the quest's required drops can currently
        be obtained from an unlocked region.
        """

        for item in quest["need"]:

            for region, info in (
                REGIONS.items()
            ):

                required_stage = (
                    info.get(
                        "story_stage_req",
                        0,
                    )
                )

                if (
                    self.player.story_stage
                    < required_stage
                ):
                    continue

                for monster in (
                    info["monsters"]
                ):

                    monster_data = (
                        MONSTERS.get(
                            monster,
                            {},
                        )
                    )

                    if (
                        monster_data.get(
                            "drop"
                        )
                        == item
                    ):
                        return True

        return False

    # ============================================================
    # CLI DISPLAY HELPERS
    # ============================================================

    def show_requirements(
        self,
        quest,
    ):
        """Print quest requirements for the CLI."""

        print("Requirements:")

        for progress in (
            self.get_quest_progress(
                quest
            )
        ):

            print(
                f" - "
                f"{progress['item']}: "
                f"{progress['have']}/"
                f"{progress['required']}"
            )

    # ============================================================
    # CLI QUEST ACCEPTANCE
    # ============================================================

    def accept_quest_menu(self):
        """Display the CLI quest selection menu."""

        if self.active:

            print(
                "Active quest: "
                f"{self.active['name']}"
            )

            self.show_requirements(
                self.active
            )

            return

        available = (
            self.get_available_quests()
        )

        if not available:

            print(
                "No quests are available "
                "to you yet. Progress the "
                "story or explore."
            )

            return

        print(
            "Available quests "
            "(one at a time):"
        )

        for index, quest in enumerate(
            available,
            start=1,
        ):

            print(
                f"{index}) "
                f"{quest['name']} — "
                f"reward: "
                f"{quest['xp']} XP, "
                f"{quest['gold']} gold"
            )

        print("0) Back")

        choice = input(
            "> "
        ).strip()

        if choice == "0":
            return

        try:

            index = int(choice) - 1

            quest = available[index]

        except (
            ValueError,
            IndexError,
        ):

            print(
                "No such quest."
            )

            return

        result = self.accept_quest(
            quest
        )

        print(
            result["message"]
        )

        if result["success"]:

            self.show_requirements(
                self.active
            )

    # ============================================================
    # CLI QUEST ABANDON
    # ============================================================

    def abandon_quest(self):
        """CLI confirmation for abandoning a quest."""

        if not self.active:

            print(
                "No active quest "
                "to abandon."
            )

            return

        answer = input(
            "Abandon "
            f"'{self.active['name']}'? "
            "(y/n) "
        ).strip().lower()

        if answer.startswith("y"):

            result = (
                self.abandon_active()
            )

            print(
                result["message"]
            )

    # ============================================================
    # PUB / MAIN STORY
    # ============================================================

    def unlock_main_story(self):
        """
        Unlock the main story through the Pub.

        Kept here for compatibility with the existing CLI.
        """

        if (
            self.player.main_story_unlocked
        ):

            print(
                'Pub Owner: "You\'ve already '
                "got the Guild Hall's "
                'attention. Follow up there."'
            )

            return

        if self.player.level < 5:

            print(
                'Pub Owner: "You\'re green '
                "yet. Come back when you've "
                "seen a bit more of the world "
                '(Lv 5)."'
            )

            return

        print(
            "\n[Pub Owner] "
            '"Word is the Guild Hall is '
            "looking for capable sorts."
        )

        print(
            "Something big's stirring out "
            "in the Woods. If you're willing, "
            'they\'ll brief you."'
        )

        self.player.main_story_unlocked = (
            True
        )

        # Keep story_stage at 0.
        # The Guild Hall begins Act I.

        print(
            "*** Main Story Unlocked! "
            "Visit the Guild Hall in town. ***"
        )

    # ============================================================
    # PUB REST
    # ============================================================

    def rest(self):
        """
        Fully restore HP and class resources for 10 gold.

        This method remains compatible with the existing CLI.
        """

        if self.player.gold < 10:

            print(
                "You don't have enough "
                "gold to rest."
            )

            return False

        self.player.gold -= 10

        self.player.hp = (
            self.player.max_hp
        )

        if self.player.resource_type:

            self.player.resource = (
                self.player.max_resource
            )

        print(
            "You rent a room and rest."
        )

        print(
            "HP fully restored!"
        )

        if self.player.resource_type:

            print(
                f"{self.player.resource_type} "
                "fully restored!"
            )

        return True

    # ============================================================
    # CLI PUB MENU
    # ============================================================

    def pub_menu(self):
        """Display the existing CLI Pub menu."""

        while True:

            print(
                "\n-- Pub --"
            )

            print(
                "1) Check/Accept Quests"
            )

            print(
                "2) Turn In Active Quest"
            )

            print(
                "3) Rest (10g) — "
                "fully recover"
            )

            print(
                "4) Abandon Active Quest"
            )

            print(
                "5) Ask about rumors "
                "(Main Story)"
            )

            print(
                "0) Leave"
            )

            choice = input(
                "> "
            ).strip()

            if choice == "0":
                return

            if choice == "1":

                self.accept_quest_menu()

            elif choice == "2":

                result = (
                    self.turn_in_active()
                )

                print(
                    result["message"]
                )

                if (
                    not result["success"]
                    and self.active
                ):

                    self.show_requirements(
                        self.active
                    )

            elif choice == "3":

                self.rest()

            elif choice == "4":

                self.abandon_quest()

            elif choice == "5":

                self.unlock_main_story()

            else:

                print(
                    "Invalid."
                )