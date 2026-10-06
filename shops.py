# shops.py

from data import SELL_VALUES


# ================================================================
# SHOP INVENTORY
# ================================================================

WEAPON_GOODS = [
    (
        "Iron Sword (Tier 1)",
        35,
        "weapon_tier:1",
    ),
    (
        "Steel Sword (Tier 2)",
        70,
        "weapon_tier:2",
    ),
    (
        "Masterwork Sword (Tier 3)",
        140,
        "weapon_tier:3",
    ),
]


ARMOR_GOODS = [
    (
        "Chainmail (Tier 1)",
        35,
        "armor_tier:1",
    ),
    (
        "Plate Armor (Tier 2)",
        70,
        "armor_tier:2",
    ),
    (
        "Bulwark Armor (Tier 3)",
        140,
        "armor_tier:3",
    ),
]


SUPPLY_GOODS = [
    (
        "Healing Tonic",
        12,
        "heal_full",
    ),
    (
        "Stout Shield (Tier 1)",
        30,
        "shield_tier:1",
    ),
    (
        "Kite Shield (Tier 2)",
        60,
        "shield_tier:2",
    ),
    (
        "Tower Shield (Tier 3)",
        120,
        "shield_tier:3",
    ),
]


# ================================================================
# SHARED SHOP HELPERS
# ================================================================

def _equipment_tier_from_effect(effect):
    """
    Return equipment type and target tier from an effect string.

    Example:
        "weapon_tier:2" -> ("weapon_tier", 2)

    Return None if the effect is not an equipment-tier effect.
    """

    if ":" not in effect:
        return None

    stat, value = effect.split(
        ":",
        1,
    )

    if stat not in {
        "weapon_tier",
        "armor_tier",
        "shield_tier",
    }:
        return None

    try:
        tier = int(value)

    except ValueError:
        return None

    return stat, tier


def get_shop_goods(category):
    """
    Return the goods belonging to a shop category.

    This is GUI-safe and does not request terminal input.
    """

    categories = {
        "weapons": WEAPON_GOODS,
        "armor": ARMOR_GOODS,
        "supplies": SUPPLY_GOODS,
    }

    return categories.get(
        category,
        [],
    )


def get_sellable_items(inventory):
    """
    Return all currently owned items that may be sold.

    Each result contains:
        name
        quantity
        value_each
    """

    sellables = []

    for item, quantity in inventory.items.items():

        if (
            item in SELL_VALUES
            and quantity > 0
        ):

            sellables.append(
                {
                    "name": item,
                    "quantity": quantity,
                    "value_each": (
                        SELL_VALUES[item] // 2
                    ),
                }
            )

    return sellables


def get_purchase_status(player, effect):
    """
    Return equipment ownership information for a shop item.

    Possible results:
        "available"
        "owned"
    """

    equipment = (
        _equipment_tier_from_effect(
            effect
        )
    )

    if not equipment:
        return "available"

    stat, target_tier = equipment

    current_tier = getattr(
        player,
        stat,
    )

    if current_tier >= target_tier:
        return "owned"

    return "available"


def purchase_item(
    player,
    inventory,
    name,
    price,
    effect,
):
    """
    Purchase one shop item.

    Returns a result dictionary so both CLI and GUI code can use
    the same economic rules without requiring input() or print().
    """

    equipment = (
        _equipment_tier_from_effect(
            effect
        )
    )

    # ------------------------------------------------------------
    # EQUIPMENT OWNERSHIP CHECK
    # ------------------------------------------------------------

    if equipment:

        stat, target_tier = equipment

        current_tier = getattr(
            player,
            stat,
        )

        if current_tier >= target_tier:

            return {
                "success": False,
                "reason": "owned",
                "message": (
                    "You already own equipment "
                    "of this tier or better."
                ),
            }

    # ------------------------------------------------------------
    # GOLD CHECK
    # ------------------------------------------------------------

    if player.gold < price:

        return {
            "success": False,
            "reason": "gold",
            "message": "Not enough gold.",
        }

    # ------------------------------------------------------------
    # APPLY PURCHASE
    # ------------------------------------------------------------

    player.gold -= price

    if effect == "heal_full":

        inventory.add(
            name,
            1,
        )

    elif effect == "atk+1":

        player.attack += 1

    elif effect == "def+1":

        player.defense += 1

    elif equipment:

        stat, target_tier = equipment

        setattr(
            player,
            stat,
            target_tier,
        )

    return {
        "success": True,
        "reason": "purchased",
        "message": (
            f"Purchased {name} "
            f"for {price}g."
        ),
    }


def sell_item(
    player,
    inventory,
    item,
    quantity=1,
):
    """
    Sell an eligible inventory item.

    Returns a result dictionary suitable for either CLI or GUI use.
    """

    if item not in SELL_VALUES:

        return {
            "success": False,
            "reason": "not_sellable",
            "message": (
                f"{item} cannot be sold."
            ),
        }

    if quantity <= 0:

        return {
            "success": False,
            "reason": "quantity",
            "message": (
                "Sale quantity must be "
                "at least 1."
            ),
        }

    owned = inventory.count(
        item
    )

    if owned < quantity:

        return {
            "success": False,
            "reason": "quantity",
            "message": (
                "You do not have enough "
                f"{item}."
            ),
        }

    value_each = (
        SELL_VALUES[item] // 2
    )

    total_value = (
        value_each * quantity
    )

    if not inventory.remove(
        item,
        quantity,
    ):

        return {
            "success": False,
            "reason": "inventory",
            "message": (
                "Unable to remove item "
                "from inventory."
            ),
        }

    player.gold += total_value

    return {
        "success": True,
        "reason": "sold",
        "message": (
            f"Sold {quantity}x {item} "
            f"for {total_value}g."
        ),
        "gold": total_value,
    }


# ================================================================
# CLI SELLING
# ================================================================

def _sell_loop(
    inventory,
    player,
):
    """Allow the player to sell eligible inventory items."""

    print(
        "\nSell Items "
        "(50% value shown)"
    )

    print("-" * 32)

    while True:

        sellables = (
            get_sellable_items(
                inventory
            )
        )

        if not sellables:

            print(
                "You have no sellable "
                "items."
            )

            return

        for i, item in enumerate(
            sellables,
            start=1,
        ):

            print(
                f"{i}) "
                f"{item['name']} "
                f"x{item['quantity']} "
                f"— {item['value_each']}g "
                "each"
            )

        print("0) Done selling")

        choice = (
            input("> ")
            .strip()
        )

        if choice == "0":
            return

        try:

            idx = int(choice) - 1

            if not (
                0 <= idx < len(
                    sellables
                )
            ):
                raise ValueError

        except ValueError:

            print("Invalid.")
            continue

        selected = sellables[idx]

        item = selected["name"]
        quantity_owned = (
            selected["quantity"]
        )

        if quantity_owned == 1:

            amount = 1

        else:

            print(
                f"Sell how many "
                f"{item}? "
                f"(1-{quantity_owned})"
            )

            amount_input = (
                input("> ")
                .strip()
            )

            try:

                amount = int(
                    amount_input
                )

                if not (
                    1
                    <= amount
                    <= quantity_owned
                ):
                    raise ValueError

            except ValueError:

                print(
                    "Invalid amount."
                )

                continue

        result = sell_item(
            player,
            inventory,
            item,
            amount,
        )

        print(
            result["message"]
        )


# ================================================================
# CLI BUYING
# ================================================================

def _buy_loop(
    player,
    inventory,
    goods,
    on_purchase=None,
):
    """
    Display a terminal shop and process purchases.

    Purchase rules are delegated to purchase_item() so the CLI
    and GUI use the same economy.
    """

    while True:

        print(
            f"\nGold: {player.gold}"
        )

        for i, (
            name,
            price,
            effect,
        ) in enumerate(
            goods,
            start=1,
        ):

            status = ""

            if (
                get_purchase_status(
                    player,
                    effect,
                )
                == "owned"
            ):

                status = (
                    " [Owned/Surpassed]"
                )

            print(
                f"{i}) {name} "
                f"- {price}g"
                f"{status}"
            )

        print("S) Sell Items")
        print("0) Leave")

        choice = (
            input("> ")
            .strip()
            .lower()
        )

        if choice == "0":
            return

        if choice == "s":

            _sell_loop(
                inventory,
                player,
            )

            continue

        try:

            idx = int(choice) - 1

            if not (
                0 <= idx < len(
                    goods
                )
            ):
                raise ValueError

        except ValueError:

            print("Invalid.")
            continue

        name, price, effect = (
            goods[idx]
        )

        result = purchase_item(
            player,
            inventory,
            name,
            price,
            effect,
        )

        print(
            result["message"]
        )

        if (
            result["success"]
            and on_purchase
        ):

            on_purchase(
                name,
                effect,
            )


# ================================================================
# CLI TOWN SHOP WRAPPER
# ================================================================

class Town:

    def __init__(
        self,
        player,
        inventory,
    ):

        self.player = player
        self.inventory = inventory

    def weapon_smith(self):

        _buy_loop(
            self.player,
            self.inventory,
            WEAPON_GOODS,
        )

    def armor_smith(self):

        _buy_loop(
            self.player,
            self.inventory,
            ARMOR_GOODS,
        )

    def magic_shop(self):

        _buy_loop(
            self.player,
            self.inventory,
            SUPPLY_GOODS,
        )