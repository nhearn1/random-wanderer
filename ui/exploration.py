"""Graphical exploration screen for Random Wanderer."""

import pygame

from data import REGIONS
from ui.components import Button


# ================================================================
# COLORS
# ================================================================

BACKGROUND = (12, 20, 32)
PANEL = (20, 35, 55)

GOLD = (218, 164, 70)
WHITE = (245, 239, 218)
MUTED = (180, 180, 170)

GREEN = (120, 190, 120)
RED = (190, 100, 100)

DIVIDER = (110, 95, 70)


# ================================================================
# HELPERS
# ================================================================

def draw_centered_text(
    screen,
    text,
    font,
    color,
    center_x,
    y,
):
    """Draw text centered horizontally."""

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


def wrap_text(
    text,
    font,
    max_width,
):
    """Split text into lines that fit within max_width."""

    words = text.split()

    lines = []
    current_line = ""

    for word in words:

        test_line = (
            word
            if not current_line
            else f"{current_line} {word}"
        )

        width = font.size(
            test_line
        )[0]

        if width <= max_width:

            current_line = test_line

        else:

            if current_line:
                lines.append(
                    current_line
                )

            current_line = word

    if current_line:

        lines.append(
            current_line
        )

    return lines


def draw_wrapped_centered_text(
    screen,
    text,
    font,
    color,
    center_x,
    start_y,
    max_width,
    line_spacing=26,
):
    """Draw wrapped text centered around center_x."""

    lines = wrap_text(
        text,
        font,
        max_width,
    )

    for index, line in enumerate(
        lines
    ):

        draw_centered_text(
            screen,
            line,
            font,
            color,
            center_x,
            start_y
            + index * line_spacing,
        )


# ================================================================
# REGION SELECTION
# ================================================================

def region_selection_screen(
    screen,
    clock,
    player,
    explorer,
    menu_font,
    small_font,
):
    """Allow the player to select an unlocked region."""

    screen_width, screen_height = (
        screen.get_size()
    )

    panel_width = min(
        900,
        screen_width - 100,
    )

    panel_height = min(
        620,
        screen_height - 80,
    )

    panel_x = (
        screen_width - panel_width
    ) // 2

    panel_y = (
        screen_height - panel_height
    ) // 2

    button_width = 650
    button_height = 55

    button_x = (
        screen_width - button_width
    ) // 2

    region_buttons = []

    region_y = panel_y + 120

    # Use the shared Explorer logic to determine
    # which regions are currently unlocked.
    for region_data in (
        explorer.get_available_regions()
    ):

        region_key = region_data[
            "key"
        ]

        unlocked = region_data[
            "unlocked"
        ]

        if unlocked:

            label = (
                region_key.upper()
            )

        else:

            label = "????? — LOCKED"

        button = Button(
            label,
            button_x,
            region_y,
            button_width,
            button_height,
            small_font,
        )

        region_buttons.append(
            (
                region_key,
                unlocked,
                button,
            )
        )

        region_y += 70

    back_button = Button(
        "BACK",
        panel_x + 25,
        panel_y + panel_height - 65,
        180,
        45,
        small_font,
    )

    while True:

        # ========================================================
        # EVENTS
        # ========================================================

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    return "back"

            if back_button.clicked(event):
                return "back"

            for (
                region_key,
                unlocked,
                button,
            ) in region_buttons:

                if button.clicked(event):

                    if unlocked:

                        if explorer.set_region(
                            region_key
                        ):

                            return "selected"

        # ========================================================
        # DRAW
        # ========================================================

        screen.fill(BACKGROUND)

        panel_rect = pygame.Rect(
            panel_x,
            panel_y,
            panel_width,
            panel_height,
        )

        pygame.draw.rect(
            screen,
            PANEL,
            panel_rect,
        )

        pygame.draw.rect(
            screen,
            GOLD,
            panel_rect,
            4,
        )

        draw_centered_text(
            screen,
            "CHOOSE REGION",
            menu_font,
            GOLD,
            screen_width // 2,
            panel_y + 45,
        )

        draw_centered_text(
            screen,
            (
                "Unknown destinations will be "
                "revealed as the story progresses."
            ),
            small_font,
            MUTED,
            screen_width // 2,
            panel_y + 82,
        )

        for (
            region_key,
            unlocked,
            button,
        ) in region_buttons:

            button.draw(screen)

            if (
                unlocked
                and region_key
                == explorer.current_region
            ):

                marker = (
                    small_font.render(
                        "CURRENT",
                        True,
                        GREEN,
                    )
                )

                screen.blit(
                    marker,
                    (
                        button.rect.right + 15,
                        button.rect.centery
                        - marker.get_height()
                        // 2,
                    ),
                )

        back_button.draw(screen)

        pygame.display.flip()
        clock.tick(60)


# ================================================================
# EXPLORATION SCREEN
# ================================================================

def exploration_screen(
    screen,
    clock,
    player,
    inventory,
    explorer,
    menu_font,
    small_font,
):
    """
    Display and control the exploration interface.

    Returns either a screen destination string or a combat tuple:

        "town"
        "inventory"
        "stats"
        "quit"

    or:

        ("combat", enemies)
    """

    screen_width, screen_height = (
        screen.get_size()
    )

    panel_width = min(
        1100,
        screen_width - 100,
    )

    panel_height = min(
        650,
        screen_height - 60,
    )

    panel_x = (
        screen_width - panel_width
    ) // 2

    panel_y = (
        screen_height - panel_height
    ) // 2

    center_x = (
        screen_width // 2
    )

    # ------------------------------------------------------------
    # BUTTONS
    # ------------------------------------------------------------

    explore_button = Button(
        "EXPLORE",
        center_x - 180,
        panel_y + 240,
        360,
        60,
        menu_font,
    )

    region_button = Button(
        "CHANGE REGION",
        center_x - 390,
        panel_y + 325,
        300,
        50,
        small_font,
    )

    rest_button = Button(
        "REST",
        center_x + 90,
        panel_y + 325,
        300,
        50,
        small_font,
    )

    inventory_button = Button(
        "INVENTORY",
        center_x - 390,
        panel_y + 395,
        300,
        50,
        small_font,
    )

    stats_button = Button(
        "STATS",
        center_x + 90,
        panel_y + 395,
        300,
        50,
        small_font,
    )

    town_button = Button(
        "RETURN TO TOWN",
        center_x - 180,
        panel_y + 485,
        360,
        50,
        small_font,
    )

    # ------------------------------------------------------------
    # MESSAGE STATE
    # ------------------------------------------------------------

    message = (
        "The road ahead waits for you."
    )

    message_color = MUTED

    while True:

        region = (
            explorer.get_current_region()
        )

        # ========================================================
        # EVENTS
        # ========================================================

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                return "quit"

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:

                    explorer.reset_exploration_state()

                    return "town"

            # ----------------------------------------------------
            # EXPLORE
            # ----------------------------------------------------

            if explore_button.clicked(event):

                result = (
                    explorer.roll_encounter()
                )

                # ----------------------------------------------
                # MONSTER
                # ----------------------------------------------

                if result["type"] == "monster":

                    return (
                        "combat",
                        result["enemies"],
                    )

                # ----------------------------------------------
                # RESOURCE
                # ----------------------------------------------

                elif result["type"] == "resource":

                    resource = result[
                        "resource"
                    ]

                    quantity = result.get(
                        "quantity",
                        1,
                    )

                    message = (
                        f"You found "
                        f"{quantity} "
                        f"{resource}."
                    )

                    message_color = GREEN

                # ----------------------------------------------
                # NOTHING
                # ----------------------------------------------

                else:

                    message = (
                        "Nothing happens... "
                        "you catch your breath."
                    )

                    message_color = MUTED

            # ----------------------------------------------------
            # CHANGE REGION
            # ----------------------------------------------------

            if region_button.clicked(event):

                result = (
                    region_selection_screen(
                        screen,
                        clock,
                        player,
                        explorer,
                        menu_font,
                        small_font,
                    )
                )

                if result == "quit":

                    return "quit"

                if result == "selected":

                    region = (
                        explorer.get_current_region()
                    )

                    message = (
                        "You head to the "
                        f"{explorer.current_region.title()}."
                    )

                    message_color = GREEN

            # ----------------------------------------------------
            # REST
            # ----------------------------------------------------

            if rest_button.clicked(event):

                result = explorer.rest()

                healed = result[
                    "healed"
                ]

                # ----------------------------------------------
                # AMBUSH
                # ----------------------------------------------

                if result["ambushed"]:

                    enemies = (
                        explorer.generate_encounter()
                    )

                    return (
                        "combat",
                        enemies,
                    )

                # ----------------------------------------------
                # SAFE REST
                # ----------------------------------------------

                if healed > 0:

                    message = (
                        "You rest and recover "
                        f"{healed} HP. "
                        f"({player.hp}/"
                        f"{player.max_hp})"
                    )

                    message_color = GREEN

                else:

                    message = (
                        "You rest for a while. "
                        "Your HP is already full."
                    )

                    message_color = MUTED

            # ----------------------------------------------------
            # INVENTORY
            # ----------------------------------------------------

            if inventory_button.clicked(event):

                return "inventory"

            # ----------------------------------------------------
            # STATS
            # ----------------------------------------------------

            if stats_button.clicked(event):

                return "stats"

            # ----------------------------------------------------
            # TOWN
            # ----------------------------------------------------

            if town_button.clicked(event):

                explorer.reset_exploration_state()

                return "town"

        # ========================================================
        # DRAW BACKGROUND
        # ========================================================

        screen.fill(BACKGROUND)

        # ========================================================
        # MAIN PANEL
        # ========================================================

        panel_rect = pygame.Rect(
            panel_x,
            panel_y,
            panel_width,
            panel_height,
        )

        pygame.draw.rect(
            screen,
            PANEL,
            panel_rect,
        )

        pygame.draw.rect(
            screen,
            GOLD,
            panel_rect,
            4,
        )

        # ========================================================
        # HEADER
        # ========================================================

        draw_centered_text(
            screen,
            "EXPLORATION",
            menu_font,
            GOLD,
            center_x,
            panel_y + 40,
        )

        region_name = (
            explorer.current_region.upper()
        )

        draw_centered_text(
            screen,
            region_name,
            menu_font,
            WHITE,
            center_x,
            panel_y + 90,
        )

        # ========================================================
        # REGION DESCRIPTION
        # ========================================================

        draw_wrapped_centered_text(
            screen,
            region["desc"],
            small_font,
            MUTED,
            center_x,
            panel_y + 130,
            800,
        )

        # ========================================================
        # PLAYER STATUS
        # ========================================================

        status_text = (
            f"{player.name}    "
            f"Level {player.level} "
            f"{player.role}    "
            f"HP: {player.hp}/"
            f"{player.max_hp}    "
            f"Gold: {player.gold}"
        )

        draw_centered_text(
            screen,
            status_text,
            small_font,
            WHITE,
            center_x,
            panel_y + 190,
        )

        # ========================================================
        # BUTTONS
        # ========================================================

        explore_button.draw(screen)

        region_button.draw(screen)
        rest_button.draw(screen)

        inventory_button.draw(screen)
        stats_button.draw(screen)

        town_button.draw(screen)

        # ========================================================
        # MESSAGE
        # ========================================================

        pygame.draw.line(
            screen,
            DIVIDER,
            (
                panel_x + 60,
                panel_y + 555,
            ),
            (
                panel_x
                + panel_width
                - 60,
                panel_y + 555,
            ),
            2,
        )

        draw_wrapped_centered_text(
            screen,
            message,
            small_font,
            message_color,
            center_x,
            panel_y + 585,
            850,
        )

        draw_centered_text(
            screen,
            "ESC: Return to Town",
            small_font,
            MUTED,
            center_x,
            panel_y + 625,
        )

        # ========================================================
        # DISPLAY
        # ========================================================

        pygame.display.flip()
        clock.tick(60)