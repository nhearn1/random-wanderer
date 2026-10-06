"""Graphical Pub screen for Random Wanderer."""

import pygame

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


def draw_wrapped_text(
    screen,
    text,
    font,
    color,
    rect,
    line_spacing=6,
):
    """Draw wrapped text inside a rectangle."""

    words = text.split()

    lines = []
    current_line = ""

    for word in words:

        test_line = (
            word
            if not current_line
            else current_line
            + " "
            + word
        )

        width, _ = font.size(
            test_line
        )

        if width <= rect.width:

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

    y = rect.y

    line_height = (
        font.get_linesize()
        + line_spacing
    )

    for line in lines:

        if (
            y + line_height
            > rect.bottom
        ):
            break

        surface = font.render(
            line,
            True,
            color,
        )

        screen.blit(
            surface,
            (
                rect.x,
                y,
            ),
        )

        y += line_height


# ================================================================
# PUB SCREEN
# ================================================================

def pub_screen(
    screen,
    clock,
    player,
    quest_board,
    font,
    small_font,
):
    """Display the graphical Pub."""

    screen_width, screen_height = (
        screen.get_size()
    )

    panel_width = min(
        1000,
        screen_width - 80,
    )

    panel_height = min(
        640,
        screen_height - 40,
    )

    panel_x = (
        screen_width - panel_width
    ) // 2

    panel_y = (
        screen_height - panel_height
    ) // 2

    rest_button = Button(
        "REST - 10G",
        panel_x + 80,
        panel_y + 260,
        240,
        52,
        small_font,
    )

    rumors_button = Button(
        "ASK ABOUT RUMORS",
        panel_x + panel_width - 320,
        panel_y + 260,
        240,
        52,
        small_font,
    )

    back_button = Button(
        "BACK TO TOWN",
        panel_x + 30,
        panel_y + panel_height - 60,
        220,
        42,
        small_font,
    )

    message = (
        "The fire is warm and the room "
        "hums with quiet conversation."
    )

    message_good = True

    speaker = "Pub"

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

            # ----------------------------------------------------
            # REST
            # ----------------------------------------------------

            if rest_button.clicked(event):

                result = (
                    quest_board
                    .rest_at_pub()
                )

                speaker = "Innkeeper"

                message = (
                    result["message"]
                )

                message_good = (
                    result["success"]
                )

            # ----------------------------------------------------
            # RUMORS
            # ----------------------------------------------------

            if rumors_button.clicked(event):

                result = (
                    quest_board
                    .ask_about_rumors()
                )

                speaker = (
                    result["speaker"]
                )

                message = (
                    result["message"]
                )

                message_good = (
                    result["success"]
                )

        # ========================================================
        # BACKGROUND
        # ========================================================

        screen.fill(
            BACKGROUND
        )

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
            "THE WANDERER'S REST",
            font,
            GOLD,
            screen_width // 2,
            panel_y + 40,
        )

        draw_centered_text(
            screen,
            (
                "A warm bed, a strong drink, "
                "and whispers from the road."
            ),
            small_font,
            MUTED,
            screen_width // 2,
            panel_y + 78,
        )

        # ========================================================
        # PLAYER STATUS
        # ========================================================

        draw_text(
            screen,
            f"Gold: {player.gold}g",
            small_font,
            GOLD,
            panel_x + 60,
            panel_y + 125,
        )

        draw_text(
            screen,
            (
                f"HP: "
                f"{player.hp}/"
                f"{player.max_hp}"
            ),
            small_font,
            WHITE,
            panel_x + 230,
            panel_y + 125,
        )

        if player.resource_type:

            resource_text = (
                f"{player.resource_type}: "
                f"{player.resource}/"
                f"{player.max_resource}"
            )

        else:

            resource_text = (
                "Class Resource: "
                "Not unlocked"
            )

        draw_text(
            screen,
            resource_text,
            small_font,
            WHITE,
            panel_x + 430,
            panel_y + 125,
        )

        pygame.draw.line(
            screen,
            DIVIDER,
            (
                panel_x + 40,
                panel_y + 165,
            ),
            (
                panel_x
                + panel_width
                - 40,
                panel_y + 165,
            ),
            2,
        )

        # ========================================================
        # REST CARD
        # ========================================================

        rest_rect = pygame.Rect(
            panel_x + 50,
            panel_y + 195,
            360,
            145,
        )

        pygame.draw.rect(
            screen,
            CARD,
            rest_rect,
            border_radius=8,
        )

        draw_centered_text(
            screen,
            "RENT A ROOM",
            small_font,
            GOLD,
            rest_rect.centerx,
            rest_rect.y + 25,
        )

        draw_centered_text(
            screen,
            "Fully restores HP",
            small_font,
            WHITE,
            rest_rect.centerx,
            rest_rect.y + 55,
        )

        draw_centered_text(
            screen,
            (
                "and class resources."
            ),
            small_font,
            MUTED,
            rest_rect.centerx,
            rest_rect.y + 82,
        )

        rest_button.draw(
            screen
        )

        # ========================================================
        # RUMORS CARD
        # ========================================================

        rumors_rect = pygame.Rect(
            panel_x + panel_width - 410,
            panel_y + 195,
            360,
            145,
        )

        pygame.draw.rect(
            screen,
            CARD,
            rumors_rect,
            border_radius=8,
        )

        draw_centered_text(
            screen,
            "LOCAL RUMORS",
            small_font,
            GOLD,
            rumors_rect.centerx,
            rumors_rect.y + 25,
        )

        if player.main_story_unlocked:

            rumor_status = (
                "Guild Hall unlocked"
            )

            rumor_color = GOOD

        elif player.level >= 5:

            rumor_status = (
                "The owner may know something..."
            )

            rumor_color = WHITE

        else:

            rumor_status = (
                "Requires Level 5"
            )

            rumor_color = MUTED

        draw_centered_text(
            screen,
            rumor_status,
            small_font,
            rumor_color,
            rumors_rect.centerx,
            rumors_rect.y + 62,
        )

        rumors_button.draw(
            screen
        )

        # ========================================================
        # DIALOGUE
        # ========================================================

        dialogue_rect = pygame.Rect(
            panel_x + 50,
            panel_y + 375,
            panel_width - 100,
            150,
        )

        pygame.draw.rect(
            screen,
            CARD,
            dialogue_rect,
            border_radius=8,
        )

        pygame.draw.rect(
            screen,
            DIVIDER,
            dialogue_rect,
            2,
            border_radius=8,
        )

        message_color = (
            WHITE
            if message_good
            else BAD
        )

        draw_text(
            screen,
            speaker,
            small_font,
            GOLD,
            dialogue_rect.x + 20,
            dialogue_rect.y + 15,
        )

        text_rect = pygame.Rect(
            dialogue_rect.x + 20,
            dialogue_rect.y + 48,
            dialogue_rect.width - 40,
            dialogue_rect.height - 60,
        )

        draw_wrapped_text(
            screen,
            message,
            small_font,
            message_color,
            text_rect,
        )

        # ========================================================
        # STORY STATUS
        # ========================================================

        if player.main_story_unlocked:

            draw_centered_text(
                screen,
                (
                    "MAIN STORY UNLOCKED — "
                    "The Guild Hall is now "
                    "available."
                ),
                small_font,
                GOOD,
                screen_width // 2,
                panel_y + 550,
            )

        # ========================================================
        # FOOTER
        # ========================================================

        back_button.draw(
            screen
        )

        draw_text(
            screen,
            "ESC: Return to Town",
            small_font,
            MUTED,
            panel_x + 280,
            panel_y
            + panel_height
            - 49,
        )

        pygame.display.flip()
        clock.tick(60)