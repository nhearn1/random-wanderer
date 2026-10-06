# character.py


class Character:
    def __init__(
        self,
        name,
        gender="male",
        appearance=1,
        gui_mode=False
    ):
        self.name = name

        # ========================================================
        # APPEARANCE
        # ========================================================

        self.gender = gender
        self.appearance = appearance

        # ========================================================
        # INTERFACE STATE
        # ========================================================

        self.gui_mode = gui_mode
        self.class_selection_pending = False

        # ========================================================
        # PROGRESSION
        # ========================================================

        self.role = "Wanderer"
        self.class_selected = False

        self.subclass = None
        self.subclass_selected = False

        # ========================================================
        # STORY & FEATURE LOCKS
        # ========================================================

        self.story_stage = 0
        self.main_story_unlocked = False
        self.ending_unlocked = False
        self.ng_plus = False

        # ========================================================
        # CORE STATS
        # ========================================================

        self.level = 1

        self.hp = 20
        self.max_hp = 20

        self.gold = 50
        self.xp = 0

        self.attack = 4
        self.defense = 2

        # ========================================================
        # COMBAT RESOURCES
        # ========================================================

        self.resource_type = None
        self.resource = 0
        self.max_resource = 0

        # ========================================================
        # COMBAT STATE
        # ========================================================

        self.cooldowns = {}
        self.status_effects = {}

        self.guard_active = False
        self.dodge_bonus = 0.0

        # ========================================================
        # EQUIPMENT
        # ========================================================

        self.weapon_tier = 0
        self.armor_tier = 0
        self.shield_tier = 0

    # ============================================================
    # STATS
    # ============================================================

    def show_stats(self):
        effective_defense = (
            self.defense
            + self.armor_tier
            + self.shield_tier
        )

        # Warrior Lv7 passive:
        # Improved Fighting Stance
        if (
            self.role == "Warrior"
            and self.level >= 7
        ):
            effective_defense += 1

        print(
            f"\nName: {self.name} | "
            f"Role: {self.role}"
        )

        print(
            f"Level: {self.level}  "
            f"XP: {self.xp}/{self.xp_to_next()}"
        )

        print(
            f"HP: {self.hp}/{self.max_hp}"
        )

        if self.resource_type:
            print(
                f"{self.resource_type}: "
                f"{self.resource}/"
                f"{self.max_resource}"
            )

        print(
            f"ATK: {self.attack}  "
            f"DEF: {self.defense} "
            f"(Effective: {effective_defense})"
        )

        print(
            f"Gold: {self.gold}"
        )

        print(
            f"Tiers: Weapon {self.weapon_tier} | "
            f"Armor {self.armor_tier} | "
            f"Shield {self.shield_tier}"
        )

        print(
            f"Story Stage: {self.story_stage} | "
            f"Ending Unlocked: {self.ending_unlocked}"
        )

    # ============================================================
    # XP / LEVELING
    # ============================================================

    def xp_to_next(self):
        return self.level * 15

    def gain_xp(self, amount):
        self.xp += amount

        while self.xp >= self.xp_to_next():
            self.xp -= self.xp_to_next()

            self.level += 1

            self.max_hp += 5
            self.hp = self.max_hp

            self.attack += 1
            self.defense += 1

            if self.class_selected:

                if self.role == "Warrior":
                    self.defense += 1

                elif self.role == "Mage":
                    self.attack += 1

                elif self.role == "Rogue":
                    self.attack += 1

            print(
                f"*** {self.name} leveled up "
                f"to {self.level}! ***"
            )

        # --------------------------------------------------------
        # CLASS SELECTION
        # --------------------------------------------------------

        if (
            self.level >= 5
            and not self.class_selected
            and self.role == "Wanderer"
        ):
            if self.gui_mode:
                self.class_selection_pending = True
            else:
                self.choose_advanced_class()

        # --------------------------------------------------------
        # SUBCLASS SELECTION
        # --------------------------------------------------------

        if (
            self.level >= 20
            and self.class_selected
            and not self.subclass_selected
        ):
            self.choose_subclass()

    # ============================================================
    # CLASS APPLICATION
    # ============================================================

    def select_advanced_class(
        self,
        role
    ):
        """
        Apply an advanced class.

        This is the shared class-selection logic used by both
        the CLI and graphical interfaces.

        Returns True if the class was successfully selected.
        """

        # A class may only be selected once.
        if self.class_selected:
            return False

        # Class selection is a level-5 feature.
        if self.level < 5:
            return False

        valid_roles = {
            "Warrior",
            "Mage",
            "Rogue",
        }

        if role not in valid_roles:
            return False

        # --------------------------------------------------------
        # WARRIOR
        # --------------------------------------------------------

        if role == "Warrior":

            self.role = "Warrior"

            self.max_hp += 10
            self.defense += 1

            self.resource_type = "Energy"
            self.max_resource = 100

        # --------------------------------------------------------
        # MAGE
        # --------------------------------------------------------

        elif role == "Mage":

            self.role = "Mage"

            self.max_hp -= 5
            self.attack += 2

            self.resource_type = "Mana"
            self.max_resource = 100

        # --------------------------------------------------------
        # ROGUE
        # --------------------------------------------------------

        elif role == "Rogue":

            self.role = "Rogue"

            self.max_hp += 5
            self.attack += 1

            self.resource_type = "Energy"
            self.max_resource = 100

        # --------------------------------------------------------
        # FINALIZE CLASS SELECTION
        # --------------------------------------------------------

        self.class_selected = True
        self.class_selection_pending = False

        self.resource = self.max_resource
        self.hp = self.max_hp

        return True

    # ============================================================
    # CLI CLASS SELECTION
    # ============================================================

    def choose_advanced_class(self):
        """CLI advanced-class selection."""

        while True:

            print(
                "\n*** Choose Your Class ***"
            )

            print(
                "1) Warrior — durable melee fighter"
            )

            print(
                "2) Mage    — powerful magic and healing"
            )

            print(
                "3) Rogue   — agile fighter focused "
                "on burst damage"
            )

            choice = input("> ").strip()

            role_map = {
                "1": "Warrior",
                "2": "Mage",
                "3": "Rogue",
            }

            role = role_map.get(
                choice
            )

            if role:

                if self.select_advanced_class(
                    role
                ):

                    print(
                        f"\n*** You are now a "
                        f"{self.role}! ***"
                    )

                    return

            print(
                "Invalid choice."
            )

    # ============================================================
    # SUBCLASS SELECTION
    # ============================================================

    def choose_subclass(self):
        """
        Placeholder until the Lv20 subclass system
        is implemented.
        """

        print(
            "(subclass selection occurs here "
            "in your full build)"
        )

        self.subclass_selected = True
        self.subclass = "Veteran"