
# quests.py
from data import REGIONS, MONSTERS

QUESTS = [
    {"name": "Spider Season", "need": {"spider fang": 3}, "xp": 25, "gold": 55},
    {"name": "Bones for the Shrine", "need": {"bone shard": 4}, "xp": 30, "gold": 65},
    {"name": "Orc Troubles", "need": {"orc tusk": 2}, "xp": 35, "gold": 80},
    {"name": "Shadow Studies", "need": {"shadow essence": 1}, "xp": 45, "gold": 95},
]

class QuestBoard:
    def __init__(self, player, inventory):
        self.player = player
        self.inventory = inventory
        self.active = None

    def pub_menu(self):
        while True:
            print("\n-- Pub --")
            print("1) Check/Accept Quests")
            print("2) Turn In Active Quest")
            print("3) Rest (10g) — fully heal")
            print("4) Abandon Active Quest")
            print("5) Ask about rumors (Main Story)")
            print("0) Leave")
            choice = input("> ").strip()
            if choice == "0": return
            elif choice == "1": self.accept_quest_menu()
            elif choice == "2": self.turn_in_active()
            elif choice == "3": self.rest()
            elif choice == "4": self.abandon_quest()
            elif choice == "5": self.unlock_main_story()
            else: print("Invalid.")

    def unlock_main_story(self):
        if self.player.main_story_unlocked:
            print("Pub Owner: \"You've already got the Guild Hall's attention. Follow up there.\"")
            return
        if self.player.level < 5:
            print("Pub Owner: \"You're green yet. Come back when you've seen a bit more of the world (Lv 5).\"")
            return
        print("\n[Pub Owner] \"Word is the Guild Hall is looking for capable sorts.")
        print("Something big's stirring out in the Woods. If you're willing, they'll brief you.\"")
        self.player.main_story_unlocked = True
        # Keep story_stage at 0; the Guild Hall will start Act I when you visit.
        print("*** Main Story Unlocked! Visit the Guild Hall in town. ***")

    def rest(self):
        """Fully restore HP and class resources for 10 gold."""

        if self.player.gold < 10:
            print("You don't have enough gold to rest.")
            return

        self.player.gold -= 10

        # Restore HP
        self.player.hp = self.player.max_hp

        # Restore Mana/Energy after class selection
        if self.player.resource_type:
            self.player.resource = self.player.max_resource

        print("You rent a room and rest.")
        print("HP fully restored!")

        if self.player.resource_type:
            print(
                f"{self.player.resource_type} "
                "fully restored!"
            )

    def _quest_is_accessible(self, q):
        for item in q["need"]:
            for region, info in REGIONS.items():
                if self.player.story_stage >= info.get("story_stage_req", 0):
                    for m in info["monsters"]:
                        if MONSTERS.get(m, {}).get("drop") == item:
                            return True
        return False

    def accept_quest_menu(self):
        if self.active:
            print(f"Active quest: {self.active['name']}")
            self.show_requirements(self.active)
            return
        available = [q for q in QUESTS if self._quest_is_accessible(q)]
        if not available:
            print("No quests are available to you yet. Progress the story or explore.")
            return
        print("Available quests (one at a time):")
        for i, q in enumerate(available, start=1):
            print(f"{i}) {q['name']} — reward: {q['xp']} XP, {q['gold']} gold")
        print("0) Back")
        choice = input("> ").strip()
        if choice == "0": return
        try:
            idx = int(choice) - 1
            self.active = available[idx]
            print(f"You accepted: {self.active['name']}")
            self.show_requirements(self.active)
        except Exception:
            print("No such quest.")

    def abandon_quest(self):
        if not self.active:
            print("No active quest to abandon.")
            return
        ans = input(f"Abandon '{self.active['name']}'? (y/n) ").strip().lower()
        if ans.startswith('y'):
            self.active = None
            print("Quest abandoned.")

    def show_requirements(self, quest):
        print("Requirements:")
        for item, qty in quest["need"].items():
            have = self.inventory.items.get(item, 0)
            print(f" - {item}: {have}/{qty}")

    def can_turn_in(self, quest):
        return all(self.inventory.items.get(item, 0) >= qty for item, qty in quest["need"].items())

    def turn_in_active(self):
        if not self.active:
            print("No active quest.")
            return
        if not self.can_turn_in(self.active):
            print("You don't have the required items yet.")
            self.show_requirements(self.active)
            return
        for item, qty in self.active["need"].items():
            self.inventory.remove(item, qty)
        self.player.gain_xp(self.active["xp"])
        self.player.gold += self.active["gold"]
        print(f"Quest complete! +{self.active['xp']} XP, +{self.active['gold']} gold.")
        self.active = None
