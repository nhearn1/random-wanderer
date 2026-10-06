"""Graphical advanced-class selection screen."""

import pygame

from ui.components import Button


# ================================================================
# COLORS
# ================================================================

BACKGROUND = (12, 20, 32)
PANEL = (20, 35, 55)

GOLD = (218, 164, 70)
WHITE = (245, 239, 218)
MUTED = (180, 180, 170)
DIVIDER = (110, 95, 70)


# ================================================================
# DRAWING HELPERS
# ================================================================

def draw_centered_text(
    screen,
    text,
    font,
    color,
    center_x,
    y,
):
    """Draw centered text."""

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


def draw_class_card(
    screen,
    rect,
    role,
    description,
    stat_text,
    resource_text,
    font,
    small_font,
):
    """Draw one class information card."""

    pygame.draw.rect(
        screen,
        PANEL,
        rect,
    )

    pygame.draw.rect(
        screen,
        DIVIDER,
        rect,
        2,
    )

    draw_centered_text(
        screen,
        role.upper(),
        font,
        GOLD,
        rect.centerx,
        rect.y + 35,
    )

    draw_centered_text(
        screen,
        description,
        small_font,
        WHITE,
        rect.centerx,
        rect.y + 78,
    )

    draw_centered_text(
        screen,
        stat_text,
        small_font,
        WHITE,
        rect.centerx,
        rect.y + 115,
    )

    draw_centered_text(
        screen,
        resource_text,
        small_font,
        MUTED,
        rect.centerx,
        rect.y + 145,
    )


# ================================================================
# CLASS SELECTION SCREEN
# ================================================================

def class_selection_screen(
    screen,
    clock,
    player,
    font,
    small_font,
):
    """
    Display the Level 5 advanced-class selection screen.

    Returns:
        "selected" after a successful class selection.
        "quit" if the game window is closed.
    """

    screen_width, screen_height = (
        screen.get_size()
    )

    # ------------------------------------------------------------
    # CLASS CARDS
    # ------------------------------------------------------------

    card_width = 340
    card_height = 230
    card_gap = 35

    total_width = (
        card_width * 3
        + card_gap * 2
    )

    start_x = (
        screen_width - total_width
    ) // 2

    card_y = 205

    warrior_rect = pygame.Rect(
        start_x,
        card_y,
        card_width,
        card_height,
    )

    mage_rect = pygame.Rect(
        start_x
        + card_width
        + card_gap,
        card_y,
        card_width,
        card_height,
    )

    rogue_rect = pygame.Rect(
        start_x
        + (
            card_width
            + card_gap
        ) * 2,
        card_y,
        card_width,
        card_height,
    )

    # ------------------------------------------------------------
    # BUTTONS
    # ------------------------------------------------------------

    button_width = 220
    button_height = 50

    warrior_button = Button(
        "CHOOSE WARRIOR",
        warrior_rect.centerx
        - button_width // 2,
        warrior_rect.bottom - 65,
        button_width,
        button_height,
        small_font,
    )

    mage_button = Button(
        "CHOOSE MAGE",
        mage_rect.centerx
        - button_width // 2,
        mage_rect.bottom - 65,
        button_width,
        button_height,
        small_font,
    )

    rogue_button = Button(
        "CHOOSE ROGUE",
        rogue_rect.centerx
        - button_width // 2,
        rogue_rect.bottom - 65,
        button_width,
        button_height,
        small_font,
    )

    # ------------------------------------------------------------
    # MAIN LOOP
    # ------------------------------------------------------------

    while True:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                return "quit"

            # This screen deliberately has no Back or ESC action.
            # Once Level 5 is reached, the player must choose a
            # class before continuing.

            if warrior_button.clicked(
                event
            ):

                if player.select_advanced_class(
                    "Warrior"
                ):

                    return "selected"

            if mage_button.clicked(
                event
            ):

                if player.select_advanced_class(
                    "Mage"
                ):

                    return "selected"

            if rogue_button.clicked(
                event
            ):

                if player.select_advanced_class(
                    "Rogue"
                ):

                    return "selected"

        # ========================================================
        # DRAW
        # ========================================================

        screen.fill(BACKGROUND)

        # --------------------------------------------------------
        # HEADER
        # --------------------------------------------------------

        draw_centered_text(
            screen,
            "CHOOSE YOUR CLASS",
            font,
            GOLD,
            screen_width // 2,
            55,
        )

        draw_centered_text(
            screen,
            (
                f"{player.name} has reached "
                "Level 5."
            ),
            small_font,
            WHITE,
            screen_width // 2,
            105,
        )

        draw_centered_text(
            screen,
            (
                "Your days as a Wanderer are over. "
                "Choose the path you will follow."
            ),
            small_font,
            MUTED,
            screen_width // 2,
            140,
        )

        # --------------------------------------------------------
        # WARRIOR
        # --------------------------------------------------------

        draw_class_card(
            screen,
            warrior_rect,
            "Warrior",
            "Durable melee fighter",
            "+10 Max HP   +1 DEF",
            "Resource: 100 Energy",
            font,
            small_font,
        )

        warrior_button.draw(
            screen
        )

        # --------------------------------------------------------
        # MAGE
        # --------------------------------------------------------

        draw_class_card(
            screen,
            mage_rect,
            "Mage",
            "Magic damage and healing",
            "-5 Max HP   +2 ATK",
            "Resource: 100 Mana",
            font,
            small_font,
        )

        mage_button.draw(
            screen
        )

        # --------------------------------------------------------
        # ROGUE
        # --------------------------------------------------------

        draw_class_card(
            screen,
            rogue_rect,
            "Rogue",
            "Agile burst-damage fighter",
            "+5 Max HP   +1 ATK",
            "Resource: 100 Energy",
            font,
            small_font,
        )

        rogue_button.draw(
            screen
        )

        # --------------------------------------------------------
        # FOOTER
        # --------------------------------------------------------

        draw_centered_text(
            screen,
            (
                "This choice is permanent."
            ),
            small_font,
            MUTED,
            screen_width // 2,
            490,
        )

        draw_centered_text(
            screen,
            (
                "New abilities unlock as "
                "your level increases."
            ),
            small_font,
            MUTED,
            screen_width // 2,
            520,
        )

        pygame.display.flip()
        clock.tick(60)