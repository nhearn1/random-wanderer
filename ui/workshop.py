"""Graphical Workshop screen for Random Wanderer."""

import pygame

from crafting import Workshop
from ui.components import Button


# ================================================================
# COLORS
# ================================================================

BACKGROUND = (12, 20, 32)
PANEL = (20, 35, 55)
CARD = (28, 46, 68)

GOLD = (218, 164, 70)
WHITE = (245, 239, 218)
MUTED = (180, 180, 170)

GOOD = (120, 210, 130)
BAD = (220, 105, 95)

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


def draw_text(
    screen,
    text,
    font,
    color,
    x,
    y,
):
    """Draw text at a specific position."""

    surface = font.render(
        str(text),
        True,
        color,
    )

    screen.blit(
        surface,
        (
            x,
            y,
        ),
    )


# ================================================================
# WORKSHOP SCREEN
# ================================================================

def workshop_screen(
    screen,
    clock,
    player,
    inventory,
    font,
    small_font,
):
    """Display the graphical crafting Workshop."""

    workshop = Workshop(
        player,
        inventory,
    )

    recipes = workshop.get_recipes()

    screen_width, screen_height = (
        screen.get_size()
    )

    # ============================================================
    # PANEL
    # ============================================================

    panel_width = min(
        1160,
        screen_width - 60,
    )

    panel_height = min(
        670,
        screen_height - 30,
    )

    panel_x = (
        screen_width - panel_width
    ) // 2

    panel_y = (
        screen_height - panel_height
    ) // 2

    # ============================================================
    # RECIPE BUTTONS
    # ============================================================

    recipe_buttons = []

    recipe_start_y = (
        panel_y + 190
    )

    recipe_height = 82

    recipe_gap = 10

    for index, recipe in enumerate(
        recipes
    ):

        button = Button(
            recipe["action"].upper(),
            panel_x + panel_width - 190,
            (
                recipe_start_y
                + index
                * (
                    recipe_height
                    + recipe_gap
                )
                + 18
            ),
            140,
            45,
            small_font,
        )

        recipe_buttons.append(
            button
        )

    back_button = Button(
        "BACK TO TOWN",
        panel_x + 30,
        panel_y + panel_height - 65,
        220,
        42,
        small_font,
    )

    message = ""
    message_good = True

    # ============================================================
    # MAIN LOOP
    # ============================================================

    while True:

        # ========================================================
        # EVENTS
        # ========================================================

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    return "town"

            if back_button.clicked(event):
                return "town"

            for index, button in enumerate(
                recipe_buttons
            ):

                if button.clicked(event):

                    recipe = recipes[
                        index
                    ]

                    result = workshop.craft(
                        recipe["key"]
                    )

                    message = (
                        result["message"]
                    )

                    message_good = (
                        result["success"]
                    )

                    break

        # ========================================================
        # BACKGROUND
        # ========================================================

        screen.fill(
            BACKGROUND
        )

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
            border_radius=12,
        )

        pygame.draw.rect(
            screen,
            GOLD,
            panel_rect,
            4,
            border_radius=12,
        )

        # ========================================================
        # HEADER
        # ========================================================

        draw_centered_text(
            screen,
            "WORKSHOP",
            font,
            GOLD,
            screen_width // 2,
            panel_y + 35,
        )

        draw_centered_text(
            screen,
            (
                "Craft supplies and improve "
                "your equipment"
            ),
            small_font,
            MUTED,
            screen_width // 2,
            panel_y + 70,
        )

        # ========================================================
        # PLAYER RESOURCES
        # ========================================================

        materials = (
            workshop.get_material_counts()
        )

        draw_text(
            screen,
            f"Gold: {player.gold}g",
            small_font,
            GOLD,
            panel_x + 40,
            panel_y + 105,
        )

        draw_text(
            screen,
            (
                f"Herbs: "
                f"{materials['herbs']}"
            ),
            small_font,
            WHITE,
            panel_x + 200,
            panel_y + 105,
        )

        draw_text(
            screen,
            (
                f"Mushrooms: "
                f"{materials['mushrooms']}"
            ),
            small_font,
            WHITE,
            panel_x + 350,
            panel_y + 105,
        )

        draw_text(
            screen,
            (
                f"Ore: "
                f"{materials['ore']}"
            ),
            small_font,
            WHITE,
            panel_x + 555,
            panel_y + 105,
        )

        draw_text(
            screen,
            (
                f"Driftwood: "
                f"{materials['driftwood']}"
            ),
            small_font,
            WHITE,
            panel_x + 675,
            panel_y + 105,
        )

        pygame.draw.line(
            screen,
            DIVIDER,
            (
                panel_x + 35,
                panel_y + 145,
            ),
            (
                panel_x
                + panel_width
                - 35,
                panel_y + 145,
            ),
            2,
        )

        # ========================================================
        # CURRENT EQUIPMENT
        # ========================================================

        equipment_text = (
            "Current Equipment — "
            f"Weapon T{player.weapon_tier}   "
            f"Armor T{player.armor_tier}   "
            f"Shield T{player.shield_tier}"
        )

        draw_text(
            screen,
            equipment_text,
            small_font,
            MUTED,
            panel_x + 40,
            panel_y + 158,
        )

        # ========================================================
        # RECIPES
        # ========================================================

        for index, recipe in enumerate(
            recipes
        ):

            y = (
                recipe_start_y
                + index
                * (
                    recipe_height
                    + recipe_gap
                )
            )

            card_rect = pygame.Rect(
                panel_x + 35,
                y,
                panel_width - 70,
                recipe_height,
            )

            pygame.draw.rect(
                screen,
                CARD,
                card_rect,
                border_radius=8,
            )

            status = (
                workshop.get_recipe_status(
                    recipe["key"]
                )
            )

            # ----------------------------------------------------
            # RECIPE NAME
            # ----------------------------------------------------

            draw_text(
                screen,
                recipe["name"],
                small_font,
                GOLD,
                panel_x + 55,
                y + 12,
            )

            # ----------------------------------------------------
            # DESCRIPTION
            # ----------------------------------------------------

            draw_text(
                screen,
                recipe["description"],
                small_font,
                WHITE,
                panel_x + 55,
                y + 36,
            )

            # ----------------------------------------------------
            # REQUIREMENTS
            # ----------------------------------------------------

            requirement_color = (
                GOOD
                if status["available"]
                else MUTED
            )

            draw_text(
                screen,
                recipe["requirements"],
                small_font,
                requirement_color,
                panel_x + 475,
                y + 30,
            )

            # ----------------------------------------------------
            # STATUS
            # ----------------------------------------------------

            if status["maxed"]:

                draw_text(
                    screen,
                    "MAX TIER",
                    small_font,
                    GOOD,
                    panel_x
                    + panel_width
                    - 310,
                    y + 30,
                )

            recipe_buttons[
                index
            ].draw(screen)

        # ========================================================
        # RESULT MESSAGE
        # ========================================================

        if message:

            message_color = (
                GOOD
                if message_good
                else BAD
            )

            draw_centered_text(
                screen,
                message,
                small_font,
                message_color,
                screen_width // 2,
                panel_y + panel_height - 90,
            )

        # ========================================================
        # FOOTER
        # ========================================================

        back_button.draw(
            screen
        )

        hint = small_font.render(
            "ESC: Return to Town",
            True,
            MUTED,
        )

        screen.blit(
            hint,
            (
                panel_x + 280,
                panel_y
                + panel_height
                - 53,
            ),
        )

        pygame.display.flip()
        clock.tick(60)