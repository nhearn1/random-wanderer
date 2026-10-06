import pygame

from shops import (
    get_shop_goods,
    get_sellable_items,
    get_purchase_status,
    purchase_item,
    sell_item,
)

from ui.components import Button


# ================================================================
# COLORS
# ================================================================

BACKGROUND = (24, 20, 18)
PANEL = (42, 35, 29)
PANEL_ALT = (53, 44, 35)

TEXT = (245, 239, 218)
MUTED_TEXT = (190, 180, 160)

GOLD = (232, 196, 92)
GOOD = (120, 210, 130)
BAD = (220, 105, 95)


# ================================================================
# HELPERS
# ================================================================

def draw_text(
    screen,
    text,
    font,
    color,
    x,
    y,
):
    """Draw simple text at the supplied position."""

    surface = font.render(
        str(text),
        True,
        color,
    )

    screen.blit(
        surface,
        (x, y),
    )


def draw_centered_text(
    screen,
    text,
    font,
    color,
    center_x,
    y,
):
    """Draw horizontally centered text."""

    surface = font.render(
        str(text),
        True,
        color,
    )

    rect = surface.get_rect(
        center=(
            center_x,
            y,
        )
    )

    screen.blit(
        surface,
        rect,
    )


def category_title(category):

    titles = {
        "weapons": "WEAPONS",
        "armor": "ARMOR",
        "supplies": (
            "SUPPLIES & SHIELDS"
        ),
    }

    return titles.get(
        category,
        "SHOP",
    )


# ================================================================
# CATEGORY SHOP
# ================================================================

def category_shop_screen(
    screen,
    clock,
    player,
    inventory,
    menu_font,
    small_font,
    category,
):
    """Display one purchasing category."""

    goods = get_shop_goods(
        category
    )

    back_button = Button(
        "BACK",
        50,
        630,
        180,
        52,
        menu_font,
    )

    item_buttons = []

    for index, (
        name,
        price,
        effect,
    ) in enumerate(goods):

        button = Button(
            "BUY",
            950,
            180 + index * 92,
            180,
            48,
            small_font,
        )

        item_buttons.append(
            button
        )

    message = ""
    message_good = True

    while True:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    return "back"

            if back_button.clicked(event):
                return "back"

            for index, button in enumerate(
                item_buttons
            ):

                if button.clicked(event):

                    name, price, effect = (
                        goods[index]
                    )

                    result = purchase_item(
                        player,
                        inventory,
                        name,
                        price,
                        effect,
                    )

                    message = (
                        result["message"]
                    )

                    message_good = (
                        result["success"]
                    )

        screen.fill(
            BACKGROUND
        )

        draw_centered_text(
            screen,
            category_title(
                category
            ),
            menu_font,
            TEXT,
            640,
            55,
        )

        draw_text(
            screen,
            f"Gold: {player.gold}g",
            menu_font,
            GOLD,
            70,
            95,
        )

        for index, (
            name,
            price,
            effect,
        ) in enumerate(goods):

            y = 155 + index * 92

            pygame.draw.rect(
                screen,
                PANEL,
                (
                    65,
                    y,
                    1080,
                    72,
                ),
                border_radius=8,
            )

            draw_text(
                screen,
                name,
                small_font,
                TEXT,
                90,
                y + 14,
            )

            draw_text(
                screen,
                f"{price}g",
                small_font,
                GOLD,
                90,
                y + 40,
            )

            status = (
                get_purchase_status(
                    player,
                    effect,
                )
            )

            if status == "owned":

                draw_text(
                    screen,
                    "OWNED / SURPASSED",
                    small_font,
                    MUTED_TEXT,
                    610,
                    y + 25,
                )

            item_buttons[
                index
            ].draw(screen)

        if message:

            color = (
                GOOD
                if message_good
                else BAD
            )

            draw_centered_text(
                screen,
                message,
                small_font,
                color,
                640,
                590,
            )

        back_button.draw(
            screen
        )

        pygame.display.flip()
        clock.tick(60)


# ================================================================
# SELL SCREEN
# ================================================================

def sell_screen(
    screen,
    clock,
    player,
    inventory,
    menu_font,
    small_font,
):
    """
    Sell one item per click.

    Repeated clicks allow multiple copies to be sold without
    introducing a keyboard quantity-entry dialog.
    """

    back_button = Button(
        "BACK",
        50,
        630,
        180,
        52,
        menu_font,
    )

    message = ""
    message_good = True

    while True:

        sellables = (
            get_sellable_items(
                inventory
            )
        )

        sell_buttons = []

        for index, item in enumerate(
            sellables
        ):

            button = Button(
                "SELL 1",
                950,
                160 + index * 58,
                180,
                42,
                small_font,
            )

            sell_buttons.append(
                button
            )

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    return "back"

            if back_button.clicked(event):
                return "back"

            for index, button in enumerate(
                sell_buttons
            ):

                if button.clicked(event):

                    item = sellables[
                        index
                    ]

                    result = sell_item(
                        player,
                        inventory,
                        item["name"],
                        1,
                    )

                    message = (
                        result["message"]
                    )

                    message_good = (
                        result["success"]
                    )

                    break

        screen.fill(
            BACKGROUND
        )

        draw_centered_text(
            screen,
            "SELL ITEMS",
            menu_font,
            TEXT,
            640,
            55,
        )

        draw_text(
            screen,
            f"Gold: {player.gold}g",
            menu_font,
            GOLD,
            70,
            95,
        )

        draw_text(
            screen,
            "The shop pays 50% of base value.",
            small_font,
            MUTED_TEXT,
            70,
            130,
        )

        if not sellables:

            draw_centered_text(
                screen,
                "You have no sellable items.",
                small_font,
                MUTED_TEXT,
                640,
                300,
            )

        else:

            for index, item in enumerate(
                sellables
            ):

                y = 155 + index * 58

                pygame.draw.rect(
                    screen,
                    PANEL,
                    (
                        65,
                        y,
                        1080,
                        48,
                    ),
                    border_radius=7,
                )

                draw_text(
                    screen,
                    (
                        f"{item['name']} "
                        f"x{item['quantity']}"
                    ),
                    small_font,
                    TEXT,
                    90,
                    y + 14,
                )

                draw_text(
                    screen,
                    (
                        f"{item['value_each']}g "
                        "each"
                    ),
                    small_font,
                    GOLD,
                    610,
                    y + 14,
                )

                sell_buttons[
                    index
                ].draw(screen)

        if message:

            color = (
                GOOD
                if message_good
                else BAD
            )

            draw_centered_text(
                screen,
                message,
                small_font,
                color,
                640,
                595,
            )

        back_button.draw(
            screen
        )

        pygame.display.flip()
        clock.tick(60)


# ================================================================
# GENERAL SHOP HUB
# ================================================================

def shop_screen(
    screen,
    clock,
    player,
    inventory,
    menu_font,
    small_font,
):
    """Display the graphical General Shop hub."""

    weapons_button = Button(
        "WEAPONS",
        420,
        180,
        440,
        60,
        menu_font,
    )

    armor_button = Button(
        "ARMOR",
        420,
        260,
        440,
        60,
        menu_font,
    )

    supplies_button = Button(
        "SUPPLIES & SHIELDS",
        420,
        340,
        440,
        60,
        menu_font,
    )

    sell_button = Button(
        "SELL ITEMS",
        420,
        420,
        440,
        60,
        menu_font,
    )

    back_button = Button(
        "BACK TO TOWN",
        420,
        520,
        440,
        60,
        menu_font,
    )

    while True:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    return "town"

            if weapons_button.clicked(event):

                result = category_shop_screen(
                    screen,
                    clock,
                    player,
                    inventory,
                    menu_font,
                    small_font,
                    "weapons",
                )

                if result == "quit":
                    return "quit"

            if armor_button.clicked(event):

                result = category_shop_screen(
                    screen,
                    clock,
                    player,
                    inventory,
                    menu_font,
                    small_font,
                    "armor",
                )

                if result == "quit":
                    return "quit"

            if supplies_button.clicked(
                event
            ):

                result = category_shop_screen(
                    screen,
                    clock,
                    player,
                    inventory,
                    menu_font,
                    small_font,
                    "supplies",
                )

                if result == "quit":
                    return "quit"

            if sell_button.clicked(event):

                result = sell_screen(
                    screen,
                    clock,
                    player,
                    inventory,
                    menu_font,
                    small_font,
                )

                if result == "quit":
                    return "quit"

            if back_button.clicked(event):
                return "town"

        screen.fill(
            BACKGROUND
        )

        draw_centered_text(
            screen,
            "GENERAL SHOP",
            menu_font,
            TEXT,
            640,
            70,
        )

        draw_centered_text(
            screen,
            (
                "Weapons, armor, supplies, "
                "and trade goods"
            ),
            small_font,
            MUTED_TEXT,
            640,
            110,
        )

        draw_centered_text(
            screen,
            f"Gold: {player.gold}g",
            menu_font,
            GOLD,
            640,
            145,
        )

        weapons_button.draw(
            screen
        )

        armor_button.draw(
            screen
        )

        supplies_button.draw(
            screen
        )

        sell_button.draw(
            screen
        )

        back_button.draw(
            screen
        )

        pygame.display.flip()
        clock.tick(60)