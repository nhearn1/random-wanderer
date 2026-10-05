"""Graphical character statistics screen for Random Wanderer."""

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
# HELPERS
# ================================================================

def draw_stat_row(
    screen,
    label,
    value,
    x,
    y,
    font,
):
    """Draw a label and value pair."""

    label_surface = font.render(
        label,
        True,
        MUTED,
    )

    value_surface = font.render(
        str(value),
        True,
        WHITE,
    )

    screen.blit(
        label_surface,
        (x, y),
    )

    screen.blit(
        value_surface,
        (x + 220, y),
    )


# ================================================================
# STATS SCREEN
# ================================================================

def stats_screen(
    screen,
    clock,
    player,
    font,
    small_font,
    return_screen="town",
):
    """Display the player's character statistics."""

    screen_width, screen_height = (
        screen.get_size()
    )

    panel_width = min(
        1000,
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
                    return return_screen

            if back_button.clicked(event):
                return return_screen

        # ========================================================
        # BACKGROUND
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

        title = font.render(
            "CHARACTER STATS",
            True,
            GOLD,
        )

        title_rect = title.get_rect(
            center=(
                screen_width // 2,
                panel_y + 45,
            )
        )

        screen.blit(
            title,
            title_rect,
        )

        name_text = font.render(
            player.name,
            True,
            WHITE,
        )

        name_rect = name_text.get_rect(
            center=(
                screen_width // 2,
                panel_y + 90,
            )
        )

        screen.blit(
            name_text,
            name_rect,
        )

        role_text = small_font.render(
            f"Level {player.level} "
            f"{player.role}",
            True,
            MUTED,
        )

        role_rect = role_text.get_rect(
            center=(
                screen_width // 2,
                panel_y + 125,
            )
        )

        screen.blit(
            role_text,
            role_rect,
        )

        pygame.draw.line(
            screen,
            DIVIDER,
            (
                panel_x + 50,
                panel_y + 155,
            ),
            (
                panel_x
                + panel_width
                - 50,
                panel_y + 155,
            ),
            2,
        )

        # ========================================================
        # LEFT COLUMN
        # ========================================================

        left_x = panel_x + 90
        left_y = panel_y + 190

        xp_needed = getattr(
            player,
            "xp_to_next",
            None,
        )

        if callable(xp_needed):
            xp_needed = xp_needed()

        if xp_needed is None:
            xp_needed = getattr(
                player,
                "xp_needed",
                "?",
            )

        draw_stat_row(
            screen,
            "LEVEL",
            player.level,
            left_x,
            left_y,
            small_font,
        )

        draw_stat_row(
            screen,
            "XP",
            f"{player.xp}/{xp_needed}",
            left_x,
            left_y + 45,
            small_font,
        )

        draw_stat_row(
            screen,
            "HP",
            f"{player.hp}/{player.max_hp}",
            left_x,
            left_y + 90,
            small_font,
        )

        draw_stat_row(
            screen,
            "GOLD",
            player.gold,
            left_x,
            left_y + 135,
            small_font,
        )

        draw_stat_row(
            screen,
            "ATTACK",
            player.attack,
            left_x,
            left_y + 180,
            small_font,
        )

        draw_stat_row(
            screen,
            "DEFENSE",
            player.defense,
            left_x,
            left_y + 225,
            small_font,
        )

        effective_defense = (
            player.defense
            + player.armor_tier
            + player.shield_tier
        )

        draw_stat_row(
            screen,
            "EFFECTIVE DEF",
            effective_defense,
            left_x,
            left_y + 270,
            small_font,
        )

        # ========================================================
        # RIGHT COLUMN
        # ========================================================

        divider_x = (
            panel_x + panel_width // 2
        )

        pygame.draw.line(
            screen,
            DIVIDER,
            (
                divider_x,
                panel_y + 180,
            ),
            (
                divider_x,
                panel_y + 500,
            ),
            2,
        )

        right_x = divider_x + 70
        right_y = panel_y + 190

        draw_stat_row(
            screen,
            "WEAPON TIER",
            player.weapon_tier,
            right_x,
            right_y,
            small_font,
        )

        draw_stat_row(
            screen,
            "ARMOR TIER",
            player.armor_tier,
            right_x,
            right_y + 45,
            small_font,
        )

        draw_stat_row(
            screen,
            "SHIELD TIER",
            player.shield_tier,
            right_x,
            right_y + 90,
            small_font,
        )

        subclass = getattr(
            player,
            "subclass",
            None,
        )

        story_stage = getattr(
            player,
            "story_stage",
            0,
        )

        extra_text = small_font.render(
            f"Subclass: {subclass}  |  "
            f"Story Stage: {story_stage}",
            True,
            MUTED,
        )

        screen.blit(
            extra_text,
            (
                right_x,
                right_y + 160,
            ),
        )

        # ========================================================
        # FOOTER
        # ========================================================

        back_button.draw(screen)

        hint = small_font.render(
            "ESC: Return",
            True,
            MUTED,
        )

        screen.blit(
            hint,
            (
                panel_x + 230,
                panel_y + panel_height - 52,
            ),
        )

        pygame.display.flip()
        clock.tick(60)