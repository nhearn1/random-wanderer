
# combat.py
import random

def _hit_success(base=0.80, modifier=0.0):
    return random.random() < max(0.05, min(0.98, base + modifier))

def _calc_damage(atk, defense, mult=1.0):
    raw = max(1, atk - defense + random.randint(-1, 2))
    return max(1, int(raw * mult))

def _use_item(player, inventory):
    if not inventory or inventory.count("Healing Tonic") <= 0:
        print("You have no usable items.")
        return False
    ans = input("Use Healing Tonic to fully restore HP? (y/n) ").strip().lower()
    if ans.startswith('y'):
        inventory.remove("Healing Tonic", 1)
        player.hp = player.max_hp
        print("You feel refreshed! HP fully restored.")
        return True
    return False

def fight(player, enemies, inventory=None):
    enemies = enemies if isinstance(enemies, list) else [enemies]
    turn = 1
    while player.hp > 0 and any(e.hp > 0 for e in enemies):
        alive = [e for e in enemies if e.hp > 0]
        print(f"\nTurn {turn}")
        print(f"Your HP: {player.hp}/{player.max_hp}")
        for i, e in enumerate(alive, start=1):
            print(f"  [{i}] {e.name} HP: {e.hp}")

        print("(A)ttack  (B)Abilities  (I)tem  (R)un  (S)tats  (V)Inventory")
        move = input("> ").strip().lower()
        acted = False

        if move.startswith('s'):
            player.show_stats();  continue
        if move.startswith('v'):
            inventory.show(player) if inventory else print("No inventory.");  continue
        if move.startswith('i'):
            if _use_item(player, inventory): acted = True
        elif move.startswith('a'):
            target = alive[0] if len(alive) == 1 else None
            if not target:
                try:
                    tidx = int(input("Attack which target? # ").strip()) - 1
                    target = alive[tidx]
                except Exception:
                    print("You hesitate...")
            if target:
                if _hit_success():
                    mult = 1.0 + 0.20 * player.weapon_tier
                    dmg = _calc_damage(player.attack, target.defense, mult)
                    target.hp -= dmg
                    print(f"You hit the {target.name} for {dmg}.")
                    acted = True
                    if target.hp <= 0:
                        print(f"The {target.name} is defeated!")
                        player.gain_xp(getattr(target, "xp", 0))  # XP immediately on kill
                else:
                    print("Your attack missed!");  acted = True
        elif move.startswith('b'):
            print("(Abilities menu placeholder)")
        elif move.startswith('r'):
            if random.random() < 0.5:
                print("You fled successfully.");  return "fled"
            else:
                print("You failed to run!");  acted = True
        else:
            print("You hesitate...")

        if acted:
            for e in alive:
                if e.hp <= 0:  continue
                if _hit_success():
                    edmg = _calc_damage(e.atk, player.defense + player.shield_tier)
                    player.hp = max(0, player.hp - edmg)
                    print(f"The {e.name} hits you for {edmg}.")
                else:
                    print(f"The {e.name} misses.")
            turn += 1

    if player.hp <= 0:
        print("You were defeated...");  return "lost"
    print("Enemies defeated!")
    return "won"
