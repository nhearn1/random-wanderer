# combat.py
import random
from abilities import ABILITIES


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

    if ans.startswith("y"):
        inventory.remove("Healing Tonic", 1)
        player.hp = player.max_hp
        print("You feel refreshed! HP fully restored.")
        return True

    return False


def _ability_menu(player):
    """Return the selected ability key, or None if cancelled."""

    class_abilities = ABILITIES.get(player.role, {})

    available = [
        (key, ability)
        for key, ability in class_abilities.items()
        if player.level >= ability["level"]
    ]

    if not available:
        print("You have no abilities available.")
        return None

    print(f"\n-- {player.role} Abilities --")
    print(f"{player.resource_type}: {player.resource}/{player.max_resource}")

    for i, (key, ability) in enumerate(available, start=1):
        print(
            f"{i}) {ability['name']} "
            f"[{ability['cost']} {player.resource_type}]"
        )
        print(f"   {ability['description']}")

    print("0) Back")

    choice = input("> ").strip()

    if choice == "0":
        return None

    try:
        idx = int(choice) - 1

        if 0 <= idx < len(available):
            return available[idx][0]
    except ValueError:
        pass

    print("Invalid choice.")
    return None


def _choose_target(alive, prompt="Choose target # "):
    """Return an enemy target, or None if selection fails."""

    if len(alive) == 1:
        return alive[0]

    try:
        idx = int(input(prompt).strip()) - 1

        if 0 <= idx < len(alive):
            return alive[idx]

    except ValueError:
        pass

    print("Invalid target.")
    return None


def _use_ability(player, ability_key, alive, turn):
    """Execute a class ability. Return True if the player's turn was used."""

    ability = ABILITIES[player.role][ability_key]
    cost = ability["cost"]

    if player.resource < cost:
        print(
            f"Not enough {player.resource_type}. "
            f"You need {cost}, but have {player.resource}."
        )
        return False

    # --------------------
    # WARRIOR
    # --------------------

    if ability_key == "guard":
        player.resource -= cost
        player.guard_active = True
        print("You raise your guard and brace for the next attack.")
        return True

    if ability_key == "mighty_strike":
        target = _choose_target(alive)

        if not target:
            return False

        player.resource -= cost

        if _hit_success():
            mult = 1.5 + (0.20 * player.weapon_tier)
            dmg = _calc_damage(player.attack, target.defense, mult)
            target.hp -= dmg

            print(
                f"Mighty Strike hits the {target.name} "
                f"for {dmg} damage!"
            )

            if target.hp <= 0:
                print(f"The {target.name} is defeated!")
                player.gain_xp(getattr(target, "xp", 0))

        else:
            print("Mighty Strike misses!")

        return True

    # --------------------
    # MAGE
    # --------------------

    if ability_key == "small_heal":
        if player.hp >= player.max_hp:
            print("Your HP is already full.")
            return False

        player.resource -= cost

        heal = max(1, int(player.max_hp * 0.25))
        old_hp = player.hp
        player.hp = min(player.max_hp, player.hp + heal)
        healed = player.hp - old_hp

        print(f"You restore {healed} HP.")
        return True

    if ability_key == "fire_bolt":
        target = _choose_target(alive)

        if not target:
            return False

        player.resource -= cost

        if _hit_success(base=0.90):
            mult = 1.35
            dmg = _calc_damage(player.attack, target.defense, mult)
            target.hp -= dmg

            print(
                f"Fire Bolt scorches the {target.name} "
                f"for {dmg} damage!"
            )

            if target.hp <= 0:
                print(f"The {target.name} is defeated!")
                player.gain_xp(getattr(target, "xp", 0))

        else:
            print("Fire Bolt misses!")

        return True

    # --------------------
    # ROGUE
    # --------------------

    if ability_key == "sneak_attack":
        target = _choose_target(alive)

        if not target:
            return False

        player.resource -= cost

        # x1.5 normally, x3 on first combat turn
        mult = 3.0 if turn == 1 else 1.5
        mult += 0.20 * player.weapon_tier

        if _hit_success():
            dmg = _calc_damage(player.attack, target.defense, mult)
            target.hp -= dmg

            print(
                f"Sneak Attack hits the {target.name} "
                f"for {dmg} damage!"
            )

            if target.hp <= 0:
                print(f"The {target.name} is defeated!")
                player.gain_xp(getattr(target, "xp", 0))

        else:
            print("Sneak Attack misses!")

        return True

    if ability_key == "nimble_feet":
        player.resource -= cost
        player.dodge_bonus = 0.20

        print("You become light on your feet. Dodge chance increased!")
        return True

    print("That ability has not been implemented yet.")
    return False


def fight(player, enemies, inventory=None):
    enemies = enemies if isinstance(enemies, list) else [enemies]

    turn = 1

    while player.hp > 0 and any(e.hp > 0 for e in enemies):

        alive = [e for e in enemies if e.hp > 0]

        print(f"\nTurn {turn}")
        print(f"Your HP: {player.hp}/{player.max_hp}")

        if player.resource_type:
            print(
                f"{player.resource_type}: "
                f"{player.resource}/{player.max_resource}"
            )

        for i, e in enumerate(alive, start=1):
            print(f"  [{i}] {e.name} HP: {e.hp}")

        print(
            "(A)ttack  (B)Abilities  (I)tem  "
            "(R)un  (S)tats  (V)Inventory"
        )

        move = input("> ").strip().lower()
        acted = False

        # --------------------
        # NON-TURN ACTIONS
        # --------------------

        if move.startswith("s"):
            player.show_stats()
            continue

        if move.startswith("v"):
            if inventory:
                inventory.show(player)
            else:
                print("No inventory.")
            continue

        # --------------------
        # ITEM
        # --------------------

        if move.startswith("i"):
            if _use_item(player, inventory):
                acted = True

        # --------------------
        # NORMAL ATTACK
        # --------------------

        elif move.startswith("a"):

            target = alive[0] if len(alive) == 1 else None

            if not target:
                try:
                    tidx = int(
                        input("Attack which target? # ").strip()
                    ) - 1

                    target = alive[tidx]

                except (ValueError, IndexError):
                    print("You hesitate...")

            if target:

                if _hit_success():

                    mult = 1.0 + (0.20 * player.weapon_tier)

                    dmg = _calc_damage(
                        player.attack,
                        target.defense,
                        mult
                    )

                    target.hp -= dmg

                    print(
                        f"You hit the {target.name} "
                        f"for {dmg}."
                    )

                    acted = True

                    if target.hp <= 0:
                        print(
                            f"The {target.name} "
                            "is defeated!"
                        )

                        player.gain_xp(
                            getattr(target, "xp", 0)
                        )

                else:
                    print("Your attack missed!")
                    acted = True

        # --------------------
        # ABILITY
        # --------------------

        elif move.startswith("b"):

            ability_key = _ability_menu(player)

            if ability_key:
                acted = _use_ability(
                    player,
                    ability_key,
                    alive,
                    turn
                )

        # --------------------
        # RUN
        # --------------------

        elif move.startswith("r"):

            if random.random() < 0.5:
                print("You fled successfully.")
                return "fled"

            else:
                print("You failed to run!")
                acted = True

        else:
            print("You hesitate...")

        # ====================================================
        # ENEMY PHASE
        # ====================================================

        if acted:

            for e in alive:

                if e.hp <= 0:
                    continue

                # Rogue dodge bonus modifies enemy accuracy
                if _hit_success(
                    modifier=-player.dodge_bonus
                ):

                    total_defense = (
                        player.defense
                        + player.armor_tier
                        + player.shield_tier
                    )

                    edmg = _calc_damage(
                        e.atk,
                        total_defense
                    )

                    # Warrior Guard
                    if player.guard_active:
                        reduction = min(
                            0.75,
                            0.40
                            + (0.05 * player.shield_tier)
                        )

                        edmg = max(
                            1,
                            int(edmg * (1.0 - reduction))
                        )

                        player.guard_active = False

                        print(
                            "Your guard absorbs "
                            "part of the blow!"
                        )

                    player.hp = max(
                        0,
                        player.hp - edmg
                    )

                    print(
                        f"The {e.name} hits you "
                        f"for {edmg}."
                    )

                else:
                    print(f"The {e.name} misses.")

            # Nimble Feet currently lasts one enemy phase
            if player.dodge_bonus > 0:
                player.dodge_bonus = 0.0

            # --------------------
            # RESOURCE REGEN
            # --------------------

            if player.resource_type:

                regen = 10
                old_resource = player.resource

                player.resource = min(
                    player.max_resource,
                    player.resource + regen
                )

                gained = (
                    player.resource - old_resource
                )

                if gained:
                    print(
                        f"You recover {gained} "
                        f"{player.resource_type}."
                    )

            turn += 1

    # ========================================================
    # COMBAT RESULT
    # ========================================================

    if player.hp <= 0:
        print("You were defeated...")
        return "lost"

    print("Enemies defeated!")
    return "won"