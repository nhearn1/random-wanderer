"""Graphical inventory screen for Random Wanderer."""

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

def draw_section_title(
    screen,
    text,
    x,
    y,
    font,
):
    """Draw a gold section heading."""

    surface = font.render(
        text,
        True,
        GOLD,
    )

    screen.blit(
        surface,
        (x, y),
    )


def draw_item_row(
    screen,
    item_name,
    quantity,
    x,
    y,
    font,
):
    """Draw one inventory item and quantity."""

    item_surface = font.render(
        item_name,
        True,
        WHITE,
    )

    quantity_surface = font.render(
        f"x{quantity}",
        True,
        MUTED,
    )

    screen.blit(
        item_surface,
        (x, y),
    )

    screen.blit(
        quantity_surface,
        (x + 300, y),
    )


def draw_equipment_row(
    screen,
    label,
    tier,
    x,
    y,
    font,
):
    """Draw one equipment tier."""

    label_surface = font.render(
        label,
        True,
        MUTED,
    )

    tier_surface = font.render(
        f"Tier {tier}",
        True,
        WHITE,
    )

    screen.blit(
        label_surface,
        (x, y),
    )

    screen.blit(
        tier_surface,
        (x + 180, y),
    )


# ================================================================
# INVENTORY SCREEN
# ================================================================

def inventory_screen(
    screen,
    clock,
    player,
    inventory,
    font,
    small_font,
    return_screen="town",
):
    """Display inventory and equipment."""

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
            "INVENTORY",
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

        gold_text = small_font.render(
            f"Gold: {player.gold}",
            True,
            WHITE,
        )

        gold_rect = gold_text.get_rect(
            center=(
                screen_width // 2,
                panel_y + 82,
            )
        )

        screen.blit(
            gold_text,
            gold_rect,
        )

        # ========================================================
        # DIVIDER
        # ========================================================

        divider_x = (
            panel_x + panel_width // 2
        )

        pygame.draw.line(
            screen,
            DIVIDER,
            (
                divider_x,
                panel_y + 120,
            ),
            (
                divider_x,
                panel_y + panel_height - 90,
            ),
            2,
        )

        # ========================================================
        # ITEMS
        # ========================================================

        left_x = panel_x + 50
        content_y = panel_y + 140

        draw_section_title(
            screen,
            "ITEMS",
            left_x,
            content_y,
            small_font,
        )

        item_y = content_y + 55

        if inventory.items:

            for item_name, quantity in sorted(
                inventory.items.items()
            ):

                draw_item_row(
                    screen,
                    item_name,
                    quantity,
                    left_x,
                    item_y,
                    small_font,
                )

                item_y += 40

        else:

            empty_text = small_font.render(
                "Your inventory is empty.",
                True,
                MUTED,
            )

            screen.blit(
                empty_text,
                (
                    left_x,
                    item_y,
                ),
            )

        # ========================================================
        # EQUIPMENT
        # ========================================================

        right_x = divider_x + 50

        draw_section_title(
            screen,
            "EQUIPMENT",
            right_x,
            content_y,
            small_font,
        )

        equipment_y = content_y + 55

        draw_equipment_row(
            screen,
            "Weapon",
            player.weapon_tier,
            right_x,
            equipment_y,
            small_font,
        )

        draw_equipment_row(
            screen,
            "Armor",
            player.armor_tier,
            right_x,
            equipment_y + 50,
            small_font,
        )

        draw_equipment_row(
            screen,
            "Shield",
            player.shield_tier,
            right_x,
            equipment_y + 100,
            small_font,
        )

        # ========================================================
        # CHARACTER
        # ========================================================

        character_y = (
            equipment_y + 185
        )

        draw_section_title(
            screen,
            "CHARACTER",
            right_x,
            character_y,
            small_font,
        )

        name_text = small_font.render(
            player.name,
            True,
            WHITE,
        )

        role_text = small_font.render(
            f"Level {player.level} "
            f"{player.role}",
            True,
            MUTED,
        )

        screen.blit(
            name_text,
            (
                right_x,
                character_y + 50,
            ),
        )

        screen.blit(
            role_text,
            (
                right_x,
                character_y + 85,
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