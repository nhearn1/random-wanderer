"""Graphical equipment screen for Random Wanderer."""

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

DIVIDER = (110, 95, 70)


# ================================================================
# EQUIPMENT NAMES
# ================================================================

WEAPON_NAMES = {
    0: "Basic Weapon",
    1: "Iron Sword",
    2: "Steel Sword",
    3: "Masterwork Sword",
}


ARMOR_NAMES = {
    0: "Basic Clothing",
    1: "Chainmail",
    2: "Plate Armor",
    3: "Bulwark Armor",
}


SHIELD_NAMES = {
    0: "No Shield",
    1: "Stout Shield",
    2: "Kite Shield",
    3: "Tower Shield",
}


# ================================================================
# HELPERS
# ================================================================

def get_equipment_name(
    equipment_type,
    tier,
):
    """Return the display name for an equipment tier."""

    equipment_tables = {
        "weapon": WEAPON_NAMES,
        "armor": ARMOR_NAMES,
        "shield": SHIELD_NAMES,
    }

    table = equipment_tables.get(
        equipment_type,
        {},
    )

    return table.get(
        tier,
        f"Unknown Tier {tier}",
    )


def get_effective_defense(player):
    """Calculate defense using the same rules as character stats."""

    effective_defense = (
        player.defense
        + player.armor_tier
        + player.shield_tier
    )

    # Warrior Level 7 passive:
    # Improved Fighting Stance
    if (
        player.role == "Warrior"
        and player.level >= 7
    ):
        effective_defense += 1

    return effective_defense


def get_weapon_bonus(player):
    """
    Return the weapon damage multiplier bonus.

    Combat currently grants +20% damage per weapon tier.
    """

    return (
        player.weapon_tier * 20
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


def draw_equipment_card(
    screen,
    x,
    y,
    width,
    height,
    title,
    item_name,
    tier,
    effect_text,
    font,
    small_font,
):
    """Draw one equipment slot card."""

    card_rect = pygame.Rect(
        x,
        y,
        width,
        height,
    )

    pygame.draw.rect(
        screen,
        CARD,
        card_rect,
        border_radius=10,
    )

    pygame.draw.rect(
        screen,
        GOLD,
        card_rect,
        2,
        border_radius=10,
    )

    title_surface = font.render(
        title,
        True,
        GOLD,
    )

    screen.blit(
        title_surface,
        (
            x + 20,
            y + 15,
        ),
    )

    item_surface = small_font.render(
        item_name,
        True,
        WHITE,
    )

    screen.blit(
        item_surface,
        (
            x + 20,
            y + 60,
        ),
    )

    tier_surface = small_font.render(
        f"Tier: {tier}",
        True,
        MUTED,
    )

    screen.blit(
        tier_surface,
        (
            x + 20,
            y + 90,
        ),
    )

    effect_surface = small_font.render(
        effect_text,
        True,
        GOOD,
    )

    screen.blit(
        effect_surface,
        (
            x + 20,
            y + 120,
        ),
    )


# ================================================================
# EQUIPMENT SCREEN
# ================================================================

def equipment_screen(
    screen,
    clock,
    player,
    font,
    small_font,
):
    """Display the player's currently equipped gear."""

    screen_width, screen_height = (
        screen.get_size()
    )

    # ============================================================
    # LAYOUT
    # ============================================================

    panel_width = min(
        1120,
        screen_width - 80,
    )

    panel_height = min(
        650,
        screen_height - 50,
    )

    panel_x = (
        screen_width - panel_width
    ) // 2

    panel_y = (
        screen_height - panel_height
    ) // 2

    card_gap = 20

    card_width = (
        panel_width
        - 80
        - (card_gap * 2)
    ) // 3

    card_height = 170

    card_y = (
        panel_y + 155
    )

    weapon_x = (
        panel_x + 40
    )

    armor_x = (
        weapon_x
        + card_width
        + card_gap
    )

    shield_x = (
        armor_x
        + card_width
        + card_gap
    )

    back_button = Button(
        "BACK TO TOWN",
        panel_x + 35,
        panel_y + panel_height - 70,
        220,
        45,
        small_font,
    )

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
            "EQUIPMENT",
            font,
            GOLD,
            screen_width // 2,
            panel_y + 40,
        )

        draw_centered_text(
            screen,
            (
                f"{player.name} — "
                f"Level {player.level} "
                f"{player.role}"
            ),
            small_font,
            WHITE,
            screen_width // 2,
            panel_y + 80,
        )

        pygame.draw.line(
            screen,
            DIVIDER,
            (
                panel_x + 35,
                panel_y + 115,
            ),
            (
                panel_x
                + panel_width
                - 35,
                panel_y + 115,
            ),
            2,
        )

        # ========================================================
        # EQUIPMENT DATA
        # ========================================================

        weapon_name = get_equipment_name(
            "weapon",
            player.weapon_tier,
        )

        armor_name = get_equipment_name(
            "armor",
            player.armor_tier,
        )

        shield_name = get_equipment_name(
            "shield",
            player.shield_tier,
        )

        weapon_bonus = get_weapon_bonus(
            player
        )

        # ========================================================
        # EQUIPMENT CARDS
        # ========================================================

        draw_equipment_card(
            screen,
            weapon_x,
            card_y,
            card_width,
            card_height,
            "WEAPON",
            weapon_name,
            player.weapon_tier,
            (
                f"+{weapon_bonus}% "
                "weapon damage"
            ),
            font,
            small_font,
        )

        draw_equipment_card(
            screen,
            armor_x,
            card_y,
            card_width,
            card_height,
            "ARMOR",
            armor_name,
            player.armor_tier,
            (
                f"+{player.armor_tier} "
                "effective DEF"
            ),
            font,
            small_font,
        )

        draw_equipment_card(
            screen,
            shield_x,
            card_y,
            card_width,
            card_height,
            "SHIELD",
            shield_name,
            player.shield_tier,
            (
                f"+{player.shield_tier} "
                "effective DEF"
            ),
            font,
            small_font,
        )

        # ========================================================
        # COMBAT SUMMARY
        # ========================================================

        summary_y = (
            card_y
            + card_height
            + 45
        )

        summary_title = font.render(
            "COMBAT SUMMARY",
            True,
            GOLD,
        )

        screen.blit(
            summary_title,
            (
                panel_x + 45,
                summary_y,
            ),
        )

        attack_text = small_font.render(
            (
                f"Base Attack: "
                f"{player.attack}"
            ),
            True,
            WHITE,
        )

        defense_text = small_font.render(
            (
                f"Base Defense: "
                f"{player.defense}"
            ),
            True,
            WHITE,
        )

        effective_text = small_font.render(
            (
                "Effective Defense: "
                f"{get_effective_defense(player)}"
            ),
            True,
            GOOD,
        )

        screen.blit(
            attack_text,
            (
                panel_x + 45,
                summary_y + 45,
            ),
        )

        screen.blit(
            defense_text,
            (
                panel_x + 330,
                summary_y + 45,
            ),
        )

        screen.blit(
            effective_text,
            (
                panel_x + 615,
                summary_y + 45,
            ),
        )

        # ========================================================
        # EQUIPMENT NOTE
        # ========================================================

        note = small_font.render(
            (
                "Equipment purchased in the General Shop "
                "is automatically equipped."
            ),
            True,
            MUTED,
        )

        screen.blit(
            note,
            (
                panel_x + 45,
                summary_y + 90,
            ),
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
                - 56,
            ),
        )

        pygame.display.flip()
        clock.tick(60)