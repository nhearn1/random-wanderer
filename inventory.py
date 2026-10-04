class Inventory:
    def __init__(self):
        self.items = {}
        # Non-consumable progression is tracked on the Character (tiers), but we show here for convenience.
        # Consumables: e.g., 'Healing Tonic'
        # Monster parts: strings like 'goblin ear', 'bone shard', etc.

    def add(self, item, qty=1):
        self.items[item] = self.items.get(item, 0) + qty
        print(f"+ {qty}x {item} added to inventory.")

    def remove(self, item, qty=1):
        if self.items.get(item, 0) >= qty:
            self.items[item] -= qty
            if self.items[item] <= 0:
                del self.items[item]
            print(f"- {qty}x {item} removed from inventory.")
            return True
        print("Not enough items.")
        return False

    def count(self, item):
        return self.items.get(item, 0)

    def show(self, player=None):
        print("\nInventory (Gold: {}g)".format(player.gold if player else "?"))
        print("-"*24)
        if not self.items:
            print("(empty)")
        else:
            for k, v in self.items.items():
                print(f"{k}: {v}")
        if player:
            print("\nEquipment")
            print("-"*24)
            print(f"Weapon Tier: {player.weapon_tier}")
            print(f"Armor  Tier: {player.armor_tier}")
            print(f"Shield Tier: {player.shield_tier}")
