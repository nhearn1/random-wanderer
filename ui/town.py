"""Graphical town hub for Random Wanderer."""

from pathlib import Path

import pygame

from ui.components import Button


# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = (
    Path(__file__)
    .resolve()
    .parent
    .parent
)

TOWN_BACKGROUND_PATH = (
    PROJECT_ROOT
    / "assets"
    / "backgrounds"
    / "town_background.png"
)


# ============================================================
# COLORS
# ============================================================

WHITE = (245, 245, 235)
GOLD = (218, 164, 70)
PANEL_BLUE = (20, 35, 55, 220)


# ============================================================
# BACKGROUND
# ============================================================

def load_town_background(size):
    """Load and scale the town background."""

    if not TOWN_BACKGROUND_PATH.exists():

        raise FileNotFoundError(
            "Town background not found:\n"
            f"{TOWN_BACKGROUND_PATH}"
        )

    background = pygame.image.load(
        str(
            TOWN_BACKGROUND_PATH
        )
    ).convert()

    return pygame.transform.smoothscale(
        background,
        size,
    )


# ============================================================
# PLAYER PANEL
# ============================================================

def draw_player_panel(
    screen,
    player,
    font,
    small_font,
):
    """Draw the player's current status."""

    panel = pygame.Surface(
        (350, 145),
        pygame.SRCALPHA,
    )

    panel.fill(
        PANEL_BLUE
    )

    pygame.draw.rect(
        panel,
        GOLD,
        panel.get_rect(),
        3,
    )

    name_text = font.render(
        player.name,
        True,
        GOLD,
    )

    role_text = small_font.render(
        (
            f"Level {player.level} "
            f"{player.role}"
        ),
        True,
        WHITE,
    )

    hp_text = small_font.render(
        (
            f"HP: "
            f"{player.hp}/"
            f"{player.max_hp}"
        ),
        True,
        WHITE,
    )

    gold_text = small_font.render(
        f"Gold: {player.gold}",
        True,
        WHITE,
    )

    panel.blit(
        name_text,
        (20, 15),
    )

    panel.blit(
        role_text,
        (20, 55),
    )

    panel.blit(
        hp_text,
        (20, 85),
    )

    panel.blit(
        gold_text,
        (20, 110),
    )

    screen.blit(
        panel,
        (25, 25),
    )


# ============================================================
# TOWN SCREEN
# ============================================================

def town_screen(
    screen,
    clock,
    player,
    font,
    small_font,
):
    """Display the graphical town hub."""

    background = (
        load_town_background(
            screen.get_size()
        )
    )

    screen_width, screen_height = (
        screen.get_size()
    )

    button_width = 220
    button_height = 55

    # ========================================================
    # LOCATION BUTTONS
    # ========================================================

    pub_button = Button(
        "PUB",
        60,
        int(
            screen_height * 0.34
        ),
        button_width,
        button_height,
        font,
    )

    general_shop_button = Button(
        "GENERAL SHOP",
        (
            screen_width
            - button_width
            - 60
        ),
        int(
            screen_height * 0.34
        ),
        button_width,
        button_height,
        font,
    )

    workshop_button = Button(
        "WORKSHOP",
        60,
        int(
            screen_height * 0.57
        ),
        button_width,
        button_height,
        font,
    )

    equipment_shop_button = Button(
        "EQUIPMENT",
        (
            screen_width
            - button_width
            - 60
        ),
        int(
            screen_height * 0.57
        ),
        button_width,
        button_height,
        font,
    )

    quest_button = Button(
        "QUEST BOARD",
        (
            screen_width
            - button_width
        ) // 2,
        110,
        button_width,
        button_height,
        font,
    )

    guild_unlocked = (
        player.level >= 5
        and player.main_story_unlocked
    )

    guild_label = (
        "GUILD HALL"
        if guild_unlocked
        else "GUILD HALL - LOCKED"
    )

    guild_button = Button(
        guild_label,
        (
            screen_width
            - 280
        ) // 2,
        285,
        280,
        button_height,
        small_font,
    )

    explore_button = Button(
        "EXPLORE",
        (
            screen_width
            - button_width
        ) // 2,
        screen_height - 105,
        button_width,
        button_height,
        font,
    )

    # ========================================================
    # PLAYER MENU BUTTONS
    # ========================================================

    inventory_button = Button(
        "INV",
        screen_width - 245,
        25,
        100,
        45,
        small_font,
    )

    stats_button = Button(
        "STATS",
        screen_width - 130,
        25,
        100,
        45,
        small_font,
    )

    buttons = [
        pub_button,
        general_shop_button,
        workshop_button,
        equipment_shop_button,
        quest_button,
        guild_button,
        explore_button,
        inventory_button,
        stats_button,
    ]

    # ========================================================
    # MAIN LOOP
    # ========================================================

    while True:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    return "title"

            if pub_button.clicked(
                event
            ):
                return "pub"

            if general_shop_button.clicked(
                event
            ):
                return "general_shop"

            if workshop_button.clicked(
                event
            ):
                return "workshop"

            if equipment_shop_button.clicked(
                event
            ):
                return "equipment_shop"

            if quest_button.clicked(
                event
            ):
                return "quests"

            if guild_button.clicked(
                event
            ):

                if guild_unlocked:
                    return "guild_hall"

            if explore_button.clicked(
                event
            ):
                return "explore"

            if inventory_button.clicked(
                event
            ):
                return "inventory"

            if stats_button.clicked(
                event
            ):
                return "stats"

        # ====================================================
        # DRAW BACKGROUND
        # ====================================================

        screen.blit(
            background,
            (0, 0),
        )

        overlay = pygame.Surface(
            screen.get_size(),
            pygame.SRCALPHA,
        )

        overlay.fill(
            (0, 0, 0, 35)
        )

        screen.blit(
            overlay,
            (0, 0),
        )

        # ====================================================
        # PLAYER PANEL
        # ====================================================

        draw_player_panel(
            screen,
            player,
            font,
            small_font,
        )

        # ====================================================
        # BUTTONS
        # ====================================================

        for button in buttons:

            button.draw(
                screen
            )

        pygame.display.flip()
        clock.tick(60)