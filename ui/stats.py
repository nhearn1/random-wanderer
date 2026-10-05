"""Graphical character stats screen for Random Wanderer."""

import pygame

from ui.components import Button


# ============================================================
# COLORS
# ============================================================

BACKGROUND = (12, 20, 32)
PANEL = (20, 35, 55)
GOLD = (218, 164, 70)
WHITE = (245, 239, 218)
MUTED = (180, 180, 170)


# ============================================================
# HELPERS
# ============================================================

def draw_stat_line(
    screen,
    label,
    value,
    x,
    y,
    font,
):
    """Draw one label/value stat line."""

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
        (x + 190, y),
    )


def get_effective_defense(player):
    """Calculate defense exactly as the character stats display does."""

    effective_defense = (
        player.defense
        + player.armor_tier
        + player.shield_tier
    )

    # Warrior Lv7 passive:
    # Improved Fighting Stance
    if (
        player.role == "Warrior"
        and player.level >= 7
    ):
        effective_defense += 1

    return effective_defense


# ============================================================
# STATS SCREEN
# ============================================================

def stats_screen(
    screen,
    clock,
    player,
    font,
    small_font,
):
    """Display the player's character statistics."""

    screen_width, screen_height = screen.get_size()

    back_button = Button(
        "BACK",
        40,
        screen_height - 85,
        180,
        50,
        small_font,
    )

    while True:

        # ====================================================
        # EVENTS
        # ====================================================

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    return "town"

            if back_button.clicked(event):
                return "town"

        # ====================================================
        # BACKGROUND
        # ====================================================

        screen.fill(BACKGROUND)

        # ====================================================
        # MAIN PANEL
        # ====================================================

        panel_width = min(
            900,
            screen_width - 100,
        )

        panel_height = min(
            650,
            screen_height - 120,
        )

        panel_x = (
            screen_width - panel_width
        ) // 2

        panel_y = 45

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

        # ====================================================
        # HEADER
        # ====================================================

        title = font.render(
            player.name.upper(),
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

        role_text = small_font.render(
            f"Level {player.level} {player.role}",
            True,
            WHITE,
        )

        role_rect = role_text.get_rect(
            center=(
                screen_width // 2,
                panel_y + 85,
            )
        )

        screen.blit(
            role_text,
            role_rect,
        )

        # ====================================================
        # COLUMN POSITIONS
        # ====================================================

        left_x = panel_x + 65
        right_x = panel_x + panel_width // 2 + 35

        start_y = panel_y + 145
        spacing = 48

        # ====================================================
        # LEFT COLUMN
        # ====================================================

        draw_stat_line(
            screen,
            "LEVEL",
            player.level,
            left_x,
            start_y,
            small_font,
        )

        draw_stat_line(
            screen,
            "XP",
            f"{player.xp}/{player.xp_to_next()}",
            left_x,
            start_y + spacing,
            small_font,
        )

        draw_stat_line(
            screen,
            "HP",
            f"{player.hp}/{player.max_hp}",
            left_x,
            start_y + spacing * 2,
            small_font,
        )

        if player.resource_type:

            draw_stat_line(
                screen,
                player.resource_type.upper(),
                (
                    f"{player.resource}/"
                    f"{player.max_resource}"
                ),
                left_x,
                start_y + spacing * 3,
                small_font,
            )

        draw_stat_line(
            screen,
            "GOLD",
            player.gold,
            left_x,
            start_y + spacing * 4,
            small_font,
        )

        # ====================================================
        # RIGHT COLUMN
        # ====================================================

        effective_defense = get_effective_defense(
            player
        )

        draw_stat_line(
            screen,
            "ATTACK",
            player.attack,
            right_x,
            start_y,
            small_font,
        )

        draw_stat_line(
            screen,
            "DEFENSE",
            player.defense,
            right_x,
            start_y + spacing,
            small_font,
        )

        draw_stat_line(
            screen,
            "EFFECTIVE DEF",
            effective_defense,
            right_x,
            start_y + spacing * 2,
            small_font,
        )

        draw_stat_line(
            screen,
            "WEAPON TIER",
            player.weapon_tier,
            right_x,
            start_y + spacing * 3,
            small_font,
        )

        draw_stat_line(
            screen,
            "ARMOR TIER",
            player.armor_tier,
            right_x,
            start_y + spacing * 4,
            small_font,
        )

        draw_stat_line(
            screen,
            "SHIELD TIER",
            player.shield_tier,
            right_x,
            start_y + spacing * 5,
            small_font,
        )

        # ====================================================
        # STORY / CLASS INFORMATION
        # ====================================================

        bottom_y = panel_y + panel_height - 85

        subclass = (
            player.subclass
            if player.subclass
            else "None"
        )

        story_text = small_font.render(
            (
                f"Subclass: {subclass}   |   "
                f"Story Stage: {player.story_stage}"
            ),
            True,
            MUTED,
        )

        story_rect = story_text.get_rect(
            center=(
                screen_width // 2,
                bottom_y,
            )
        )

        screen.blit(
            story_text,
            story_rect,
        )

        # ====================================================
        # BACK BUTTON
        # ====================================================

        back_button.draw(screen)

        hint = small_font.render(
            "ESC: Return to Town",
            True,
            MUTED,
        )

        screen.blit(
            hint,
            (
                240,
                screen_height - 70,
            ),
        )

        pygame.display.flip()
        clock.tick(60)