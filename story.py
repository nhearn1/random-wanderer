# story.py

import random

from combat import fight
from data import MONSTERS
from enemy import Enemy


# ================================================================
# STORY DATA
# ================================================================

STORY_STAGES = {
    0: {
        "title": "Prologue",
        "speaker": "Pub Owner",
        "text": (
            "Stranger, the woods are restless... "
            "something massive prowls at dusk."
        ),
        "objective": (
            "Begin Act I and investigate the Woods."
        ),
    },
    1: {
        "title": "Act I — The Restless Woods",
        "speaker": "Guild Scribe",
        "text": (
            "Target: Corrupted Alpha Bear, "
            "deep in the Woods."
        ),
        "objective": (
            "Defeat the Corrupted Alpha Bear."
        ),
        "boss": "corrupted alpha bear",
        "bumps": (1.10, 1.05, 1.0),
    },
    2: {
        "title": "Act II — Raiders at the Beach",
        "speaker": "Harbor Master",
        "text": (
            "Cut off the Warlord and the "
            "raiders scatter."
        ),
        "objective": (
            "Defeat the Pirate Warlord."
        ),
        "boss": "pirate warlord",
        "bumps": (1.12, 1.05, 1.0),
    },
    3: {
        "title": "Act III — The Undead Plains",
        "speaker": "Ranger",
        "text": (
            "Skulls drum in the grass. "
            "The Undead Chieftain commands "
            "from a cairn."
        ),
        "objective": (
            "Defeat the Undead Chieftain."
        ),
        "boss": "undead chieftain",
        "bumps": (1.15, 1.08, 1.0),
    },
    4: {
        "title": "Act IV — Black Glass",
        "speaker": "Scout",
        "text": (
            "Thin air, black glass armor, "
            "cruel magic."
        ),
        "objective": (
            "Defeat the Dark Mage General."
        ),
        "boss": "dark mage general",
        "bumps": (1.18, 1.10, 1.0),
    },
    5: {
        "title": "The Trial",
        "speaker": "High Knight",
        "text": (
            "Steel answers only to steel. "
            "Face the Trial Knight in the arena."
        ),
        "objective": (
            "Defeat the Trial Knight."
        ),
        "boss": "trial knight",
        "bumps": (1.20, 1.12, 1.10),
    },
    6: {
        "title": "The Corruption",
        "speaker": "Seer",
        "text": (
            "All threads knot here. "
            "Break the Avatar and choose your path."
        ),
        "objective": (
            "Defeat the Corruption Avatar."
        ),
        "boss": "corruption avatar",
        "bumps": (1.25, 1.12, 1.10),
    },
    7: {
        "title": "Finale — Choose Your Path",
        "speaker": "Kaelen",
        "text": (
            "You've seen the rot in the crown. "
            "Choose."
        ),
        "objective": (
            "Decide how your journey ends."
        ),
    },
    8: {
        "title": "Epilogue",
        "speaker": "Narrator",
        "text": (
            "Your journey has reached its end. "
            "The realm remembers the path you chose."
        ),
        "objective": (
            "Story complete."
        ),
    },
}


# Minimum level required to undertake each story stage.
#
# Story-stage advancement still controls region unlocks. This means
# beating a boss can unlock the next region even if the player is
# not yet high enough level to undertake the next Guild contract.
STORY_LEVEL_REQUIREMENTS = {
    0: 5,   # Guild Hall / Prologue
    1: 5,   # Corrupted Alpha Bear
    2: 7,   # Pirate Warlord
    3: 9,   # Undead Chieftain
    4: 12,  # Dark Mage General
    5: 15,  # Trial Knight
    6: 18,  # Corruption Avatar
    7: 20,  # Finale
}


VICTORY_SCENES = {
    1: {
        "speaker": "Guild Scribe",
        "text": (
            "Impressive. Raiders mass at the "
            "Beach—stop their Warlord."
        ),
    },
    2: {
        "speaker": "High Knight",
        "text": (
            "Undead banners rise across the "
            "Plains. Break their Chieftain."
        ),
    },
    3: {
        "speaker": "High Knight",
        "text": (
            "A Dark Mage General gathers power "
            "in the Mountains. End him."
        ),
    },
    4: {
        "speaker": "King's Herald",
        "text": (
            "To the Capital. Prove yourself "
            "in trial before the court."
        ),
    },
    5: {
        "speaker": "Seer",
        "text": (
            "The corruption itself gathers form. "
            "Strike at its Avatar."
        ),
    },
    6: {
        "speaker": "Kaelen",
        "text": (
            "You've seen the rot in the crown. "
            "Choose."
        ),
    },
}


ENDING_SCENES = {
    "Hero": {
        "speaker": "King",
        "text": (
            "Kneel. Rise a hero of the realm."
        ),
    },
    "Rebel": {
        "speaker": "Kaelen",
        "text": (
            "Then we break the old order together."
        ),
    },
    "Wanderer": {
        "speaker": "Pub Owner",
        "text": (
            "Some legends slip quietly out "
            "the back door."
        ),
    },
}


# ================================================================
# STORY
# ================================================================

class Story:
    """
    Shared main-story controller.

    Story stages:
      0 = Prologue
      1 = Corrupted Alpha Bear
      2 = Pirate Warlord
      3 = Undead Chieftain
      4 = Dark Mage General
      5 = Trial Knight
      6 = Corruption Avatar
      7 = Finale choice
      8 = Epilogue
    """

    def __init__(
        self,
        player,
        inventory,
        explorer,
    ):
        self.player = player
        self.inventory = inventory
        self.explorer = explorer

        self.last_message = None
        self.ending_name = None

    # ============================================================
    # GUI-SAFE STORY INFORMATION
    # ============================================================

    def get_stage_info(self):
        """Return information for the current story stage."""

        return STORY_STAGES.get(
            self.player.story_stage,
            STORY_STAGES[8],
        )

    def get_last_message(self):
        """Return the most recent story message."""

        return self.last_message

    def clear_last_message(self):
        """Clear the current story message."""

        self.last_message = None

    def can_enter_guild_hall(self):
        """Return whether the Guild Hall is unlocked."""

        return (
            self.player.level >= 5
            and self.player.main_story_unlocked
        )

    # ============================================================
    # STORY LEVEL REQUIREMENTS
    # ============================================================

    def get_required_level(
        self,
        stage=None,
    ):
        """Return the minimum level for a story stage."""

        if stage is None:
            stage = self.player.story_stage

        return STORY_LEVEL_REQUIREMENTS.get(
            stage,
            1,
        )

    def meets_level_requirement(
        self,
        stage=None,
    ):
        """Return whether the player meets a story level gate."""

        return (
            self.player.level
            >= self.get_required_level(
                stage
            )
        )

    def get_level_progress(self):
        """Return GUI-safe level-gate information."""

        required_level = (
            self.get_required_level()
        )

        return {
            "current_level": (
                self.player.level
            ),
            "required_level": (
                required_level
            ),
            "unlocked": (
                self.player.level
                >= required_level
            ),
        }

    # ============================================================
    # STORY START
    # ============================================================

    def begin_story(self):
        """Begin Act I from the Prologue."""

        if not self.can_enter_guild_hall():

            return {
                "success": False,
                "message": (
                    "The Guild Hall remains "
                    "closed to you."
                ),
            }

        if self.player.story_stage != 0:

            return {
                "success": False,
                "message": (
                    "The main story has "
                    "already begun."
                ),
            }

        if not self.meets_level_requirement(
            0
        ):

            return {
                "success": False,
                "message": (
                    "You must reach Level 5 "
                    "before beginning Act I."
                ),
            }

        self.player.story_stage = 1

        self.last_message = {
            "speaker": "Guild Scribe",
            "text": (
                "Your first contract is waiting. "
                "Hunt the Corrupted Alpha Bear "
                "in the Woods."
            ),
        }

        return {
            "success": True,
            "message": (
                "Act I has begun."
            ),
        }

    # ============================================================
    # BOSS GENERATION
    # ============================================================

    def create_current_boss(self):
        """
        Create the boss encounter for the current story stage.

        Returns an Enemy object or None.

        Level requirements are enforced here so the progression
        gate cannot be bypassed by another interface.
        """

        stage = self.player.story_stage

        if not self.meets_level_requirement(
            stage
        ):
            return None

        info = STORY_STAGES.get(
            stage
        )

        if not info:
            return None

        boss_name = info.get(
            "boss"
        )

        if not boss_name:
            return None

        bump_hp, bump_atk, bump_def = (
            info.get(
                "bumps",
                (1.0, 1.0, 1.0),
            )
        )

        enemy = self._scaled_enemy(
            boss_name
        )

        enemy.hp = int(
            enemy.hp * bump_hp
        )

        enemy.atk = int(
            enemy.atk * bump_atk
        )

        enemy.defense = int(
            enemy.defense * bump_def
        )

        return enemy

    # ============================================================
    # BOSS VICTORY
    # ============================================================

    def complete_current_boss(
        self,
        enemy,
    ):
        """
        Award story-boss gold and advance the story.

        XP has already been awarded by combat when the boss died.
        Story bosses intentionally do not use normal exploration
        drop rewards.
        """

        stage = self.player.story_stage

        if stage not in range(
            1,
            7,
        ):

            return {
                "success": False,
                "message": (
                    "There is no story boss "
                    "to complete at this stage."
                ),
            }

        gold_reward = 0

        if hasattr(
            enemy,
            "gold_range",
        ):

            gold_reward = random.randint(
                *enemy.gold_range
            )

            self.player.gold += (
                gold_reward
            )

        victory_scene = (
            VICTORY_SCENES.get(
                stage
            )
        )

        self.player.story_stage += 1

        self.last_message = (
            victory_scene
        )

        return {
            "success": True,
            "gold": gold_reward,
            "new_stage": (
                self.player.story_stage
            ),
            "message": (
                "Story advanced to Stage "
                f"{self.player.story_stage}."
            ),
        }

    # ============================================================
    # FINALE
    # ============================================================

    def choose_ending(
        self,
        ending_name,
    ):
        """
        Complete one of the three non-combat endings.

        Valid choices:
        Hero, Rebel, Wanderer
        """

        if self.player.story_stage != 7:

            return {
                "success": False,
                "message": (
                    "The finale is not "
                    "available yet."
                ),
            }

        if not self.meets_level_requirement(
            7
        ):

            return {
                "success": False,
                "message": (
                    "You must reach Level 20 "
                    "before choosing your ending."
                ),
            }

        if ending_name not in (
            "Hero",
            "Rebel",
            "Wanderer",
        ):

            return {
                "success": False,
                "message": (
                    "That ending does not exist."
                ),
            }

        scene = ENDING_SCENES[
            ending_name
        ]

        self.last_message = scene

        self._end(
            ending_name
        )

        return {
            "success": True,
            "ending": ending_name,
            "speaker": scene["speaker"],
            "message": scene["text"],
        }

    def create_kaelen_boss(self):
        """Create the optional Kaelen finale encounter."""

        if self.player.story_stage != 7:
            return None

        if not self.meets_level_requirement(
            7
        ):
            return None

        enemy = self._scaled_enemy(
            "kaelen"
        )

        enemy.hp = int(
            enemy.hp * 1.22
        )

        enemy.atk = int(
            enemy.atk * 1.18
        )

        enemy.defense = int(
            enemy.defense * 1.12
        )

        return enemy

    def complete_kaelen_duel(
        self,
        enemy,
    ):
        """Complete the Wanderer ending after defeating Kaelen."""

        if self.player.story_stage != 7:

            return {
                "success": False,
                "message": (
                    "The Kaelen duel is not "
                    "available."
                ),
            }

        if not self.meets_level_requirement(
            7
        ):

            return {
                "success": False,
                "message": (
                    "You must reach Level 20 "
                    "before challenging Kaelen."
                ),
            }

        gold_reward = 0

        if hasattr(
            enemy,
            "gold_range",
        ):

            gold_reward = random.randint(
                *enemy.gold_range
            )

            self.player.gold += (
                gold_reward
            )

        self.last_message = {
            "speaker": "Narrator",
            "text": (
                "You carve your own ending "
                "in steel and silence."
            ),
        }

        self._end(
            "Wanderer"
        )

        return {
            "success": True,
            "ending": "Wanderer",
            "gold": gold_reward,
            "message": (
                "Kaelen defeated. "
                "Wanderer ending unlocked."
            ),
        }

    # ============================================================
    # ENEMY SCALING
    # ============================================================

    def _scaled_enemy(
        self,
        name,
    ):
        """Create a story enemy scaled to player level."""

        monster = MONSTERS[
            name
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
            name=name,
            hp=hp,
            atk=attack,
            defense=defense,
            xp=monster.get(
                "xp",
                30,
            ),
            gold_range=monster.get(
                "gold",
                (10, 25),
            ),
            drop=monster.get(
                "drop",
            ),
        )

    # ============================================================
    # ENDING
    # ============================================================

    def _end(
        self,
        ending_name,
    ):
        """Mark the story complete."""

        self.ending_name = (
            ending_name
        )

        self.player.ending_unlocked = (
            True
        )

        self.player.story_stage = 8

    # ============================================================
    # CLI COMPATIBILITY
    # ============================================================

    def menu(self):
        """Terminal Guild Hall interface."""

        while True:

            print(
                "\n-- Guild Hall "
                "(Main Story) --"
            )

            print(
                "Story Stage: "
                f"{self.player.story_stage}"
            )

            stage = (
                self.player.story_stage
            )

            info = (
                self.get_stage_info()
            )

            self._scene(
                info["speaker"],
                info["text"],
            )

            if stage == 0:

                print(
                    "1) Begin Act I "
                    "(Hunt the Corrupted "
                    "Alpha Bear)"
                )

                print(
                    "0) Leave"
                )

                if (
                    input("> ").strip()
                    == "1"
                ):

                    self.begin_story()

                else:

                    return

            elif stage in range(
                1,
                7,
            ):

                required_level = (
                    self.get_required_level(
                        stage
                    )
                )

                if not (
                    self.meets_level_requirement(
                        stage
                    )
                ):

                    print(
                        "\nThe Guild will "
                        "authorize this contract "
                        f"at Level {required_level}."
                    )

                    print(
                        "Current Level: "
                        f"{self.player.level}"
                    )

                    input(
                        "\nPress Enter "
                        "to leave..."
                    )

                    return

                enemy = (
                    self.create_current_boss()
                )

                outcome = fight(
                    self.player,
                    [enemy],
                    inventory=self.inventory,
                )

                if outcome == "won":

                    self.complete_current_boss(
                        enemy
                    )

                    if self.last_message:

                        self._scene(
                            self.last_message[
                                "speaker"
                            ],
                            self.last_message[
                                "text"
                            ],
                        )

                return

            elif stage == 7:

                if not (
                    self.meets_level_requirement(
                        7
                    )
                ):

                    print(
                        "\nThe finale requires "
                        "Level 20."
                    )

                    print(
                        "Current Level: "
                        f"{self.player.level}"
                    )

                    input(
                        "\nPress Enter "
                        "to leave..."
                    )

                    return

                print(
                    "\nFinale — choose "
                    "your ending:"
                )

                print(
                    "1) Accept the King's "
                    "honor (Hero)"
                )

                print(
                    "2) Side with Kaelen "
                    "(Rebel)"
                )

                print(
                    "3) Walk away "
                    "(Wanderer)"
                )

                print(
                    "4) Challenge Kaelen "
                    "(optional duel)"
                )

                print(
                    "0) Leave"
                )

                choice = input(
                    "> "
                ).strip()

                if choice == "1":

                    result = (
                        self.choose_ending(
                            "Hero"
                        )
                    )

                    self._scene(
                        result["speaker"],
                        result["message"],
                    )

                    return

                if choice == "2":

                    result = (
                        self.choose_ending(
                            "Rebel"
                        )
                    )

                    self._scene(
                        result["speaker"],
                        result["message"],
                    )

                    return

                if choice == "3":

                    result = (
                        self.choose_ending(
                            "Wanderer"
                        )
                    )

                    self._scene(
                        result["speaker"],
                        result["message"],
                    )

                    return

                if choice == "4":

                    enemy = (
                        self.create_kaelen_boss()
                    )

                    outcome = fight(
                        self.player,
                        [enemy],
                        inventory=self.inventory,
                    )

                    if outcome == "won":

                        self.complete_kaelen_duel(
                            enemy
                        )

                        self._scene(
                            "Narrator",
                            (
                                "You carve your "
                                "own ending in "
                                "steel and silence."
                            ),
                        )

                    return

                return

            else:

                print(
                    "Story complete. "
                    "(Epilogue)"
                )

                print(
                    "0) Leave"
                )

                input(
                    "> "
                )

                return

    def _scene(
        self,
        speaker,
        text,
    ):
        """Print CLI story dialogue."""

        print(
            f"\n[{speaker}] {text}"
        )