import os
import sys

import pygame

from character import Character
from inventory import Inventory
from exploration import Explorer

from ui.components import Button
from ui.character_creation import character_creation_screen
from ui.class_selection import class_selection_screen
from ui.town import town_screen
from ui.stats import stats_screen
from ui.inventory import inventory_screen
from ui.exploration import exploration_screen
from ui.combat import combat_screen
from ui.shop import shop_screen
from ui.equipment import equipment_screen
from ui.workshop import workshop_screen


# ================================================================
# GAME SETTINGS
# ================================================================

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

TITLE = "Random Wanderer"

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

TITLE_BACKGROUND_PATH = os.path.join(
    BASE_DIR,
    "assets",
    "backgrounds",
    "title_background.png",
)


# ================================================================
# COLORS
# ================================================================

TEXT = (245, 239, 218)


# ================================================================
# ASSET LOADING
# ================================================================

def load_title_background():
    """Load and scale the title artwork."""

    if not os.path.exists(
        TITLE_BACKGROUND_PATH
    ):
        raise FileNotFoundError(
            "Title background not found:\n"
            f"{TITLE_BACKGROUND_PATH}"
        )

    image = pygame.image.load(
        TITLE_BACKGROUND_PATH
    ).convert()

    return pygame.transform.scale(
        image,
        (
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
        ),
    )


# ================================================================
# TITLE SCREEN
# ================================================================

def title_screen(
    screen,
    clock,
    background,
    menu_font,
    small_font,
):
    """Display the Random Wanderer title screen."""

    button_width = 360
    button_height = 58

    button_x = (
        SCREEN_WIDTH - button_width
    ) // 2

    begin_button = Button(
        "BEGIN JOURNEY",
        button_x,
        470,
        button_width,
        button_height,
        menu_font,
    )

    quit_button = Button(
        "QUIT",
        button_x,
        545,
        button_width,
        button_height,
        menu_font,
    )

    while True:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    return "quit"

                if event.key == pygame.K_RETURN:
                    return "start"

            if begin_button.clicked(event):
                return "start"

            if quit_button.clicked(event):
                return "quit"

        screen.blit(
            background,
            (0, 0),
        )

        panel = pygame.Surface(
            (420, 175),
            pygame.SRCALPHA,
        )

        panel.fill(
            (0, 0, 0, 115)
        )

        screen.blit(
            panel,
            (
                (SCREEN_WIDTH - 420) // 2,
                445,
            ),
        )

        begin_button.draw(screen)
        quit_button.draw(screen)

        hint = small_font.render(
            "ENTER: Begin    ESC: Quit",
            True,
            TEXT,
        )

        hint_rect = hint.get_rect(
            center=(
                SCREEN_WIDTH // 2,
                640,
            )
        )

        screen.blit(
            hint,
            hint_rect,
        )

        pygame.display.flip()
        clock.tick(FPS)


# ================================================================
# MAIN
# ================================================================

def main():
    """Run the graphical version of Random Wanderer."""

    pygame.init()

    pygame.display.set_caption(
        TITLE
    )

    screen = pygame.display.set_mode(
        (
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
        )
    )

    clock = pygame.time.Clock()

    menu_font = pygame.font.Font(
        None,
        36,
    )

    small_font = pygame.font.Font(
        None,
        23,
    )

    title_background = (
        load_title_background()
    )

    # ============================================================
    # GAME STATE
    # ============================================================

    current_screen = "title"

    return_screen = "town"

    class_return_screen = "town"

    running = True

    player = None
    inventory = None
    explorer = None

    active_enemies = None

    # ============================================================
    # MAIN APPLICATION LOOP
    # ============================================================

    while running:

        # ========================================================
        # PENDING CLASS SELECTION
        # ========================================================

        if (
            player is not None
            and player.class_selection_pending
            and current_screen not in (
                "combat",
                "class_selection",
            )
        ):

            class_return_screen = (
                current_screen
            )

            current_screen = (
                "class_selection"
            )

        # ========================================================
        # TITLE
        # ========================================================

        if current_screen == "title":

            result = title_screen(
                screen,
                clock,
                title_background,
                menu_font,
                small_font,
            )

            if result == "start":

                current_screen = (
                    "character_creation"
                )

            elif result == "quit":

                running = False

        # ========================================================
        # CHARACTER CREATION
        # ========================================================

        elif current_screen == "character_creation":

            result, character_data = (
                character_creation_screen(
                    screen,
                    clock,
                    menu_font,
                    small_font,
                )
            )

            if result == "back":

                current_screen = "title"

            elif result == "start":

                player = Character(
                    name=character_data[
                        "name"
                    ],
                    gender=character_data[
                        "gender"
                    ],
                    appearance=character_data[
                        "appearance"
                    ],
                    gui_mode=True,
                )

                inventory = Inventory()

                explorer = Explorer(
                    player,
                    inventory,
                )

                active_enemies = None

                print(
                    "\n"
                    "=== GUI CHARACTER CREATED ==="
                )

                print(
                    f"Name: {player.name}"
                )

                print(
                    f"Gender: {player.gender}"
                )

                print(
                    "Appearance: "
                    f"{player.appearance}"
                )

                print(
                    f"Role: {player.role}"
                )

                print(
                    f"Level: {player.level}"
                )

                print(
                    "HP: "
                    f"{player.hp}/"
                    f"{player.max_hp}"
                )

                print(
                    f"Gold: {player.gold}"
                )

                print(
                    "GUI Mode: "
                    f"{player.gui_mode}"
                )

                print(
                    "Class Selection Pending: "
                    f"{player.class_selection_pending}"
                )

                print(
                    "Inventory Created: "
                    f"{inventory is not None}"
                )

                print(
                    "Explorer Created: "
                    f"{explorer is not None}"
                )

                current_screen = "town"

            elif result == "quit":

                running = False

        # ========================================================
        # CLASS SELECTION
        # ========================================================

        elif current_screen == "class_selection":

            if player is None:

                current_screen = "title"
                continue

            result = class_selection_screen(
                screen,
                clock,
                player,
                menu_font,
                small_font,
            )

            if result == "selected":

                print(
                    "\n"
                    "=== ADVANCED CLASS SELECTED ==="
                )

                print(
                    f"Role: {player.role}"
                )

                print(
                    "HP: "
                    f"{player.hp}/"
                    f"{player.max_hp}"
                )

                print(
                    f"ATK: {player.attack}"
                )

                print(
                    f"DEF: {player.defense}"
                )

                print(
                    "Resource: "
                    f"{player.resource_type} "
                    f"{player.resource}/"
                    f"{player.max_resource}"
                )

                print(
                    "Class Selection Pending: "
                    f"{player.class_selection_pending}"
                )

                current_screen = (
                    class_return_screen
                )

            elif result == "quit":

                running = False

        # ========================================================
        # TOWN
        # ========================================================

        elif current_screen == "town":

            if player is None:

                current_screen = "title"
                continue

            result = town_screen(
                screen,
                clock,
                player,
                menu_font,
                small_font,
            )

            if result == "title":

                current_screen = "title"

            elif result == "quit":

                running = False

            elif result == "stats":

                return_screen = "town"
                current_screen = "stats"

            elif result == "inventory":

                return_screen = "town"
                current_screen = "inventory"

            elif result == "explore":

                current_screen = "exploration"

            elif result == "general_shop":

                current_screen = "shop"

            elif result == "equipment_shop":

                current_screen = "equipment"

            elif result == "workshop":

                current_screen = "workshop"

            else:

                print(
                    "Town destination selected: "
                    f"{result}"
                )

        # ========================================================
        # GENERAL SHOP
        # ========================================================

        elif current_screen == "shop":

            if (
                player is None
                or inventory is None
            ):

                current_screen = "title"
                continue

            result = shop_screen(
                screen,
                clock,
                player,
                inventory,
                menu_font,
                small_font,
            )

            if result == "quit":

                running = False

            else:

                current_screen = "town"

        # ========================================================
        # EQUIPMENT
        # ========================================================

        elif current_screen == "equipment":

            if player is None:

                current_screen = "title"
                continue

            result = equipment_screen(
                screen,
                clock,
                player,
                menu_font,
                small_font,
            )

            if result == "quit":

                running = False

            else:

                current_screen = "town"

        # ========================================================
        # WORKSHOP
        # ========================================================

        elif current_screen == "workshop":

            if (
                player is None
                or inventory is None
            ):

                current_screen = "title"
                continue

            result = workshop_screen(
                screen,
                clock,
                player,
                inventory,
                menu_font,
                small_font,
            )

            if result == "quit":

                running = False

            else:

                current_screen = "town"

        # ========================================================
        # EXPLORATION
        # ========================================================

        elif current_screen == "exploration":

            if (
                player is None
                or inventory is None
                or explorer is None
            ):

                current_screen = "title"
                continue

            result = exploration_screen(
                screen,
                clock,
                player,
                inventory,
                explorer,
                menu_font,
                small_font,
            )

            if (
                isinstance(result, tuple)
                and len(result) == 2
                and result[0] == "combat"
            ):

                active_enemies = result[1]

                current_screen = "combat"

            elif result == "town":

                current_screen = "town"

            elif result == "inventory":

                return_screen = "exploration"
                current_screen = "inventory"

            elif result == "stats":

                return_screen = "exploration"
                current_screen = "stats"

            elif result == "quit":

                running = False

        # ========================================================
        # COMBAT
        # ========================================================

        elif current_screen == "combat":

            if (
                player is None
                or inventory is None
                or explorer is None
                or not active_enemies
            ):

                active_enemies = None
                current_screen = "exploration"
                continue

            combat_result = combat_screen(
                screen,
                clock,
                player,
                inventory,
                active_enemies,
                menu_font,
                small_font,
            )

            outcome = combat_result.get(
                "outcome"
            )

            combat_enemies = (
                combat_result.get(
                    "enemies",
                    active_enemies,
                )
            )

            if outcome == "won":

                rewards = (
                    explorer.award_victory_rewards(
                        combat_enemies
                    )
                )

                print(
                    "\n=== COMBAT VICTORY ==="
                )

                print(
                    "Gold earned: "
                    f"{rewards['gold']}"
                )

                if rewards["drops"]:

                    print(
                        "Drops: "
                        + ", ".join(
                            rewards["drops"]
                        )
                    )

                else:

                    print(
                        "Drops: None"
                    )

                print(
                    "Player gold: "
                    f"{player.gold}"
                )

                print(
                    "Player XP: "
                    f"{player.xp}"
                )

                active_enemies = None

                current_screen = (
                    "exploration"
                )

            elif outcome == "lost":

                player.hp = 1

                explorer.reset_exploration_state()

                active_enemies = None

                print(
                    "\n"
                    "You wake up back in town "
                    "with 1 HP..."
                )

                current_screen = "town"

            elif outcome == "fled":

                active_enemies = None

                print(
                    "\n"
                    "You escaped the encounter."
                )

                current_screen = (
                    "exploration"
                )

            elif outcome == "quit":

                running = False

            else:

                print(
                    "Unknown combat outcome: "
                    f"{outcome}"
                )

                active_enemies = None

                current_screen = (
                    "exploration"
                )

        # ========================================================
        # STATS
        # ========================================================

        elif current_screen == "stats":

            if player is None:

                current_screen = "title"
                continue

            result = stats_screen(
                screen,
                clock,
                player,
                menu_font,
                small_font,
                return_screen=return_screen,
            )

            if result == "quit":

                running = False

            elif result in (
                "town",
                "exploration",
            ):

                current_screen = result

            else:

                current_screen = (
                    return_screen
                )

        # ========================================================
        # INVENTORY
        # ========================================================

        elif current_screen == "inventory":

            if (
                player is None
                or inventory is None
            ):

                current_screen = "title"
                continue

            result = inventory_screen(
                screen,
                clock,
                player,
                inventory,
                menu_font,
                small_font,
                return_screen=return_screen,
            )

            if result == "quit":

                running = False

            elif result in (
                "town",
                "exploration",
            ):

                current_screen = result

            else:

                current_screen = (
                    return_screen
                )

        # ========================================================
        # UNKNOWN STATE SAFETY
        # ========================================================

        else:

            print(
                "Unknown screen state: "
                f"{current_screen}"
            )

            current_screen = "title"

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()