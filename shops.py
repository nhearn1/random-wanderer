# shops.py
from data import SELL_VALUES

def _sell_loop(inventory, player):
    print("\nSell Items (50% value shown)")
    print("-" * 32)
    sellables = [(item, qty) for item, qty in inventory.items.items() if item in SELL_VALUES]
    if not sellables:
        print("You have no sellable items.")
        return

    while True:
        # Refresh the list each loop in case quantities change
        sellables = [(item, inventory.items.get(item, 0)) for item, _ in sellables if inventory.items.get(item, 0) > 0]
        if not sellables:
            print("Nothing left to sell.")
            return

        for i, (name, qty) in enumerate(sellables, start=1):
            value = SELL_VALUES[name] // 2
            print(f"{i}) {name} x{qty} — {value}g each")
        print("0) Done selling")
        choice = input("> ").strip()
        if choice == "0":
            break

        try:
            idx = int(choice) - 1
            if not (0 <= idx < len(sellables)):
                raise ValueError
        except ValueError:
            print("Invalid.")
            continue

        item, qty = sellables[idx]
        value = SELL_VALUES[item] // 2

        # If only one, sell automatically; otherwise ask amount
        if qty == 1:
            amt = 1
        else:
            print(f"Sell how many {item}? (1-{qty})")
            amt_in = input("> ").strip()
            try:
                amt = int(amt_in)
                if not (1 <= amt <= qty):
                    raise ValueError
            except ValueError:
                print("Invalid amount.")
                continue

        if inventory.remove(item, amt):
            player.gold += value * amt
            print(f"+{value * amt}g from selling {amt}x {item}.")

def _buy_loop(player, inventory, goods, on_purchase=None):
    print("\nGold:", player.gold)
    while True:
        for i, (name, price, effect) in enumerate(goods, start=1):
            print(f"{i}) {name} - {price}g")
        print("S) Sell Items")
        print("0) Leave")
        choice = input("> ").strip().lower()

        if choice == "0":
            return
        if choice == "s":
            _sell_loop(inventory, player)
            print("\nGold:", player.gold)
            continue

        try:
            idx = int(choice) - 1
            if not (0 <= idx < len(goods)):
                raise ValueError
        except ValueError:
            print("Invalid.")
            continue

        name, price, effect = goods[idx]
        if player.gold < price:
            print("Not enough gold.")
            continue

        player.gold -= price

        # Apply purchase effects (+ auto-equip)
        if effect == "heal_full":
            inventory.add(name, 1)
        elif effect == "atk+1":
            player.attack += 1
        elif effect == "def+1":
            player.defense += 1
        elif effect == "weapon_tier+1":
         player.weapon_tier = min(3, player.weapon_tier + 1)
        elif effect == "armor_tier+1":
         player.armor_tier = min(3, player.armor_tier + 1)
        elif effect == "shield_tier+1":
         player.shield_tier = min(3, player.shield_tier + 1)

        if on_purchase:
            on_purchase(name, effect)

        print(f"Purchased {name}. (Auto-equipped if relevant)")
        print("Gold:", player.gold)

class Town:
    def __init__(self, player, inventory):
        self.player = player
        self.inventory = inventory

    def weapon_smith(self):
        goods = [
            ("Iron Sword (Tier 1)", 35, "weapon_tier:1"),
            ("Steel Sword (Tier 2)", 70, "weapon_tier:2"),
            ("Masterwork Sword (Tier 3)", 140, "weapon_tier:3"),
        ]
        _buy_loop(self.player, self.inventory, goods)

    def armor_smith(self):
        goods = [
            ("Chainmail (Tier +1)", 35, "armor_tier+1"),
            ("Plate Armor (Tier +1)", 70, "armor_tier+1"),
            ("Bulwark Armor (Tier +1)", 140, "armor_tier+1"),
        ]
        _buy_loop(self.player, self.inventory, goods)

    def magic_shop(self):
        goods = [
            ("Healing Tonic", 12, "heal_full"),
            ("Stout Shield (Tier +1)", 30, "shield_tier+1"),
            ("Kite Shield (Tier +1)", 60, "shield_tier+1"),
            ("Tower Shield (Tier +1)", 120, "shield_tier+1"),
        ]
        _buy_loop(self.player, self.inventory, goods)
