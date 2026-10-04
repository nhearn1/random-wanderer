# crafting.py
class Workshop:
    """
    Minimal crafting system.
      - Healing Tonic: herbs(1) + mushrooms(1)
      - Tempered Edge: ore(2) + 30g -> +1 weapon tier
      - Reinforced Plate: ore(2) + driftwood(1) + 30g -> +1 armor tier
      - Shield Boss: ore(1) + 20g -> +1 shield tier
    """
    def __init__(self, player, inventory):
        self.player = player
        self.inventory = inventory

    def menu(self):
        while True:
            print("\n-- Workshop (Crafting) --")
            print("Gold:", self.player.gold)
            print("1) Brew Healing Tonic (herbs x1 + mushrooms x1)")
            print("2) Tempered Edge (+1 weapon tier)  [ore x2 + 30g]")
            print("3) Reinforced Plate (+1 armor tier)[ore x2 + driftwood x1 + 30g]")
            print("4) Shield Boss (+1 shield tier)    [ore x1 + 20g]")
            print("0) Leave")
            c = input("> ").strip()
            if c == "0": return
            elif c == "1":
                if self.inventory.items.get("herbs",0) >= 1 and self.inventory.items.get("mushrooms",0) >= 1:
                    self.inventory.remove("herbs",1); self.inventory.remove("mushrooms",1)
                    self.inventory.add("Healing Tonic",1)
                    print("Brewed a Healing Tonic.")
                else:
                    print("Missing ingredients.")
            elif c == "2":
                if self.inventory.items.get("ore",0) >= 2 and self.player.gold >= 30:
                    self.inventory.remove("ore",2); self.player.gold -= 30
                    self.player.weapon_tier += 1
                    print("Your weapon is tempered. (+1 tier)")
                else:
                    print("You need ore x2 and 30 gold.")
            elif c == "3":
                if self.inventory.items.get("ore",0) >= 2 and self.inventory.items.get("driftwood",0) >= 1 and self.player.gold >= 30:
                    self.inventory.remove("ore",2); self.inventory.remove("driftwood",1); self.player.gold -= 30
                    self.player.armor_tier += 1
                    print("Your armor is reinforced. (+1 tier)")
                else:
                    print("You need ore x2, driftwood x1 and 30 gold.")
            elif c == "4":
                if self.inventory.items.get("ore",0) >= 1 and self.player.gold >= 20:
                    self.inventory.remove("ore",1); self.player.gold -= 20
                    self.player.shield_tier += 1
                    print("Your shield is upgraded. (+1 tier)")
                else:
                    print("You need ore x1 and 20 gold.")
            else:
                print("Invalid.")
