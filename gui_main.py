import os
import sys

import pygame
from ui.components import Button
from ui.character_creation import character_creation_screen


# ================================================================
# GAME SETTINGS
# ================================================================

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

TITLE = "Random Wanderer"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

TITLE_BACKGROUND_PATH = os.path.join(
    BASE_DIR,
    "assets",
    "backgrounds",
    "title_background.png",
)


# ================================================================
# COLORS
# ================================================================

BUTTON_NORMAL = (25, 37, 56)
BUTTON_HOVER = (25, 76, 125)

BUTTON_BORDER = (218, 164, 73)
BUTTON_BORDER_INNER = (113, 72, 31)

TEXT = (245, 239, 218)
TEXT_DISABLED = (125, 125, 125)

OVERLAY = (0, 0, 0, 80)


# ================================================================
# ASSET LOADING
# ================================================================

def load_title_background():
    """Load and scale the title artwork."""

    if not os.path.exists(TITLE_BACKGROUND_PATH):
        raise FileNotFoundError(
            f"Title background not found:\n"
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

    # Positioned lower so we don't cover the logo.
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

        # --------------------------------------------------------
        # EVENTS
        # --------------------------------------------------------

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

        # --------------------------------------------------------
        # DRAW
        # --------------------------------------------------------

        screen.blit(
            background,
            (0, 0),
        )

        # Slight dark panel behind menu buttons.
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
    pygame.init()

    pygame.display.set_caption(TITLE)

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

    # Load assets once at startup.
    title_background = load_title_background()

    current_screen = "title"
    running = True

    while running:

        if current_screen == "title":

            result = title_screen(
                screen,
                clock,
                title_background,
                menu_font,
                small_font,
            )

            if result == "start":
                current_screen = "character_creation"

            elif result == "quit":
                running = False

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

                print(
                    "Character created:",
                    character_data,
                )

                # Temporary:
                # Until the GUI game screen is built,
                # return to the title screen.
                current_screen = "title"    

            elif result == "quit":
                running = False

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()