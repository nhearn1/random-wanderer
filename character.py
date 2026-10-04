
# character.py
class Character:
    def __init__(self, name):
        self.name = name

        # Progression
        self.role = "Wanderer"
        self.class_selected = False
        self.subclass = None
        self.subclass_selected = False

        # Story & feature locks
        self.story_stage = 0          # drives story act progression
        self.main_story_unlocked = False  # set to True by Pub Owner at Lv 5+
        self.ending_unlocked = False
        self.ng_plus = False

        # Core stats
        self.level = 1
        self.hp = 20
        self.max_hp = 20
        self.gold = 50
        self.xp = 0
        self.attack = 4
        self.defense = 2
        
        # Combat resources
        self.resource_type = None
        self.resource = 0
        self.max_resource = 0

        # Equipment tiers
        self.weapon_tier = 0
        self.armor_tier = 0
        self.shield_tier = 0

    def show_stats(self):
        role_str = self.role if self.role else "Wanderer"
        sub_str = f" / {self.subclass}" if self.subclass else ""
        xp_needed = self.level * 15
        print(f"Name: {self.name}  |  Role: {role_str}{sub_str}")
        print(f"Level: {self.level}  XP: {self.xp}/{xp_needed}")
        print(f"HP: {self.hp}/{self.max_hp}")
        effective_defense = self.defense + self.armor_tier + self.shield_tier
        if self.resource_type:
            print(f"{self.resource_type}: {self.resource}/{self.max_resource}")
        print(f"ATK: {self.attack}  DEF: {self.defense} (Effective: {effective_defense})")
        print(f"Gold: {self.gold}")
        print(f"Tiers: Weapon {self.weapon_tier} | Armor {self.armor_tier} | Shield {self.shield_tier}")
        print(f"Story Stage: {self.story_stage}  Main Story: {'Unlocked' if self.main_story_unlocked else 'Locked'}")

    def gain_xp(self, amount):
        self.xp += amount
        while self.xp >= self.level * 15:
            self.xp -= self.level * 15
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
            print(f"*** {self.name} leveled up to {self.level}! ***")

        # Class unlocks (keep your existing implementations if different)
        if self.level >= 5 and not self.class_selected and self.role == "Wanderer":
            self.choose_advanced_class()
        if self.level >= 20 and self.class_selected and not self.subclass_selected:
            self.choose_subclass()

    # Stubs so this file is drop-in even if your project has fuller versions.
    def choose_advanced_class(self):
        while True:
            print("\n*** Choose Your Class ***")
            print("1) Warrior — durable melee fighter")
            print("2) Mage    — powerful magic and healing")
            print("3) Rogue   — agile fighter focused on burst damage")

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

        print(f"\n*** You are now a {self.role}! ***")

    def choose_subclass(self):
        print("(subclass selection occurs here in your full build)")
        self.subclass_selected = True
        self.subclass = "Veteran"
