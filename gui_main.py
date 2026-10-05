import os
import sys

import pygame

from character import Character
from inventory import Inventory
from exploration import Explorer

from ui.components import Button
from ui.character_creation import character_creation_screen
from ui.town import town_screen
from ui.stats import stats_screen
from ui.inventory import inventory_screen
from ui.exploration import exploration_screen
from ui.combat import combat_screen


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

        # ========================================================
        # EVENTS
        # ========================================================

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

        # ========================================================
        # DRAW
        # ========================================================

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

    # Used by Inventory and Stats so those screens know whether
    # BACK should return to Town or Exploration.
    return_screen = "town"

    running = True

    player = None
    inventory = None
    explorer = None

    # Enemy objects generated by Explorer are stored here while
    # gui_main transitions from Exploration into Combat.
    active_enemies = None

    # ============================================================
    # MAIN APPLICATION LOOP
    # ============================================================

    while running:

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

                # ----------------------------------------------
                # PLAYER
                # ----------------------------------------------

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

                # ----------------------------------------------
                # SHARED GAME SYSTEMS
                # ----------------------------------------------

                inventory = Inventory()

                explorer = Explorer(
                    player,
                    inventory,
                )

                active_enemies = None

                # ----------------------------------------------
                # DEVELOPMENT DIAGNOSTICS
                # ----------------------------------------------

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

            else:

                print(
                    "Town destination selected: "
                    f"{result}"
                )

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

            # Exploration normally returns a simple string.
            # Monster encounters return:
            #
            #     ("combat", enemies)
            #
            # where enemies is the actual list of Enemy objects.

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

            # ----------------------------------------------------
            # VICTORY
            # ----------------------------------------------------

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

            # ----------------------------------------------------
            # DEFEAT
            # ----------------------------------------------------

            elif outcome == "lost":

                # Preserve the original CLI exploration behavior:
                # losing a wilderness fight returns the player to
                # Town with 1 HP.

                player.hp = 1

                explorer.reset_exploration_state()

                active_enemies = None

                print(
                    "\n"
                    "You wake up back in town "
                    "with 1 HP..."
                )

                current_screen = "town"

            # ----------------------------------------------------
            # FLED
            # ----------------------------------------------------

            elif outcome == "fled":

                active_enemies = None

                print(
                    "\n"
                    "You escaped the encounter."
                )

                current_screen = (
                    "exploration"
                )

            # ----------------------------------------------------
            # QUIT
            # ----------------------------------------------------

            elif outcome == "quit":

                running = False

            # ----------------------------------------------------
            # SAFETY FALLBACK
            # ----------------------------------------------------

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

    # ============================================================
    # SHUTDOWN
    # ============================================================

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()