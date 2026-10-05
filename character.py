# character.py


class Character:
    def __init__(self, name):
        self.name = name

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

        # Generic status-effect container.
        self.status_effects = {}

        # Existing temporary combat states.
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

        # Class selection
        if (
            self.level >= 5
            and not self.class_selected
            and self.role == "Wanderer"
        ):
            self.choose_advanced_class()

        # Subclass selection
        if (
            self.level >= 20
            and self.class_selected
            and not self.subclass_selected
        ):
            self.choose_subclass()

    # ============================================================
    # CLASS SELECTION
    # ============================================================

    def choose_advanced_class(self):
        while True:
            print("\n*** Choose Your Class ***")

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

            if choice == "1":
                self.role = "Warrior"

                self.max_hp += 10
                self.defense += 1

                self.resource_type = "Energy"
                self.max_resource = 100

                break

            elif choice == "2":
                self.role = "Mage"

                self.max_hp -= 5
                self.attack += 2

                self.resource_type = "Mana"
                self.max_resource = 100

                break

            elif choice == "3":
                self.role = "Rogue"

                self.max_hp += 5
                self.attack += 1

                self.resource_type = "Energy"
                self.max_resource = 100

                break

            else:
                print("Invalid choice.")

        self.class_selected = True

        self.resource = self.max_resource
        self.hp = self.max_hp

        print(
            f"\n*** You are now a "
            f"{self.role}! ***"
        )

    # ============================================================
    # SUBCLASS SELECTION
    # ============================================================

    def choose_subclass(self):
        # Placeholder until the Lv20 subclass system is implemented.
        print(
            "(subclass selection occurs here "
            "in your full build)"
        )

        self.subclass_selected = True
        self.subclass = "Veteran"