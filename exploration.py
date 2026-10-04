
# exploration.py
import random
from data import REGIONS, MONSTERS
from enemy import Enemy
from combat import fight

class Explorer:
    def __init__(self, player, inventory):
        self.player = player
        self.inventory = inventory
        self.current_region = "woods"
        self._rest_streak = 0
        self._monster_chance = 0.6  # base monster chance

    def choose_region(self):
        print("\nChoose a region:")
        # Build a display list that includes locked placeholders as "?????"
        display_options = []
        for key, info in REGIONS.items():
            req = info.get("story_stage_req", 0)
            if self.player.story_stage >= req:
                # unlocked
                display_options.append(("region", key, f"{key.title()} — {info['desc']}"))
            else:
                display_options.append(("locked", key, "????? — [Locked]"))
        for i, (_, _, label) in enumerate(display_options, start=1):
            print(f"{i}) {label}")
        print("0) Stay here")

        choice = input("> ").strip()
        if choice == "0":
            return
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(display_options):
                kind, key, _ = display_options[idx]
                if kind == "locked":
                    print("That destination is unknown for now.")
                    return
                self.current_region = key
                print(f"You head to the {self.current_region.title()}.")
        except ValueError:
            print("Staying where you are.")

    def explore_loop(self):
        region = REGIONS[self.current_region]
        print(f"\nExploring the {self.current_region.title()}... (press Q to return)")
        while True:
            print("[E]ncounter  [L]ook  [S]tats  [V]Inventory  [R]est  [Q]uit explore > ", end="")
            cmd = input("").strip().lower()

            if cmd == "q":
                self._rest_streak = 0
                self._monster_chance = 0.6
                break
            elif cmd == "l":
                print(region["desc"]);  continue
            elif cmd == "s":
                self.player.show_stats();  continue
            elif cmd == "v":
                self.inventory.show(self.player);  continue
            elif cmd == "r":
                self._handle_rest_with_ambush(region);  continue

            # Default action: encounter
            self._rest_streak = 0
            self.random_encounter(region)

    def _handle_rest_with_ambush(self, region):
        heal_amt = max(2, int(self.player.max_hp * 0.15))
        old = self.player.hp
        self.player.hp = min(self.player.max_hp, self.player.hp + heal_amt)
        print(f"You rest and recover {self.player.hp - old} HP. ({self.player.hp}/{self.player.max_hp})")

        self._rest_streak += 1
        base = 0.15
        extra = 0.15 * (self._rest_streak - 1)
        ambush_chance = min(0.75, base + extra)
        if random.random() < ambush_chance:
            print("You are ambushed!")
            self._rest_streak = 0
            self._monster_chance = 0.6
            self._spawn_and_fight(region)
        else:
            print("...It stays quiet.")

    def random_encounter(self, region):
        roll = random.random()
        if roll < self._monster_chance:
            self._monster_chance = 0.6  # reset when a monster spawns
            self._spawn_and_fight(region)
        elif roll < self._monster_chance + 0.2:
            res = random.choice(["herbs", "ore", "driftwood", "mushrooms"])
            self.inventory.add(res, 1)
            print(f"You found some {res}.")
            self._monster_chance = min(0.9, self._monster_chance + 0.1)
        else:
            print("Nothing happens... you catch your breath.")
            self._monster_chance = min(0.9, self._monster_chance + 0.1)

    def _spawn_and_fight(self, region):
        count = 1 if random.random() < 0.6 else (2 if random.random() < 0.7 else 3)
        chosen_names = [random.choice(region["monsters"]) for _ in range(count)]
        enemies = [self._scaled_enemy(name) for name in chosen_names]

        outcome = fight(self.player, enemies, inventory=self.inventory)
        if outcome == "won":
            # End-of-fight gold/items only; XP on kill was granted during combat
            total_gold = 0
            for e in enemies:
                if hasattr(e, "gold_range"):
                    total_gold += random.randint(*e.gold_range)
                if getattr(e, "drop", None):
                    self.inventory.add(e.drop, 1)
            self.player.gold += total_gold
            if total_gold:
                print(f"You loot {total_gold} gold.")
        elif outcome == "lost":
            print("You wake up back in town with 1 HP...")
            self.player.hp = 1

    def _scaled_enemy(self, mname):
        m = MONSTERS[mname]
        lvl = max(1, self.player.level)
        hp = int(m["hp"] + m.get("hp_per_level", 0) * (lvl - 1))
        atk = int(m["atk"] + m.get("atk_per_level", 0) * (lvl - 1))
        dfn = int(m["def"] + m.get("def_per_level", 0) * (lvl - 1))
        return Enemy(name=mname, hp=hp, atk=atk, defense=dfn,
                     xp=m.get("xp",1), gold_range=m.get("gold",(1,3)), drop=m.get("drop", None))
