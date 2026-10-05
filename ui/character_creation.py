import os

import pygame

from ui.components import Button


# ================================================================
# COLORS
# ================================================================

TEXT = (245, 239, 218)
TEXT_MUTED = (185, 185, 175)

GOLD = (218, 164, 73)
DARK_GOLD = (113, 72, 31)

PANEL = (10, 16, 25, 210)

INPUT_NORMAL = (25, 37, 56)
INPUT_ACTIVE = (34, 64, 95)

SELECTED = (25, 76, 125)


# ================================================================
# PATHS
# ================================================================

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

BACKGROUND_PATH = os.path.join(
    PROJECT_ROOT,
    "assets",
    "backgrounds",
    "character_creation_background.png",
)


def character_sprite_path(gender, appearance):
    """Return the path for the selected Wanderer sprite."""

    return os.path.join(
        PROJECT_ROOT,
        "assets",
        "characters",
        gender,
        "wanderer",
        f"appearance_{appearance}.png",
    )


# ================================================================
# TEXT INPUT
# ================================================================

class TextInput:
    """Simple character-name input box."""

    def __init__(
        self,
        x,
        y,
        width,
        height,
        font,
        max_length=20,
    ):
        self.rect = pygame.Rect(
            x,
            y,
            width,
            height,
        )

        self.font = font
        self.text = ""
        self.active = False
        self.max_length = max_length

    def handle_event(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(
                event.pos
            )

        if (
            event.type == pygame.KEYDOWN
            and self.active
        ):

            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]

            elif event.key in (
                pygame.K_RETURN,
                pygame.K_ESCAPE,
            ):
                pass

            elif (
                event.unicode.isprintable()
                and len(self.text) < self.max_length
            ):
                self.text += event.unicode

    def draw(self, screen):

        if self.active:
            background = INPUT_ACTIVE
        else:
            background = INPUT_NORMAL

        pygame.draw.rect(
            screen,
            background,
            self.rect,
        )

        pygame.draw.rect(
            screen,
            GOLD,
            self.rect,
            3,
        )

        inner = self.rect.inflate(-10, -10)

        pygame.draw.rect(
            screen,
            DARK_GOLD,
            inner,
            2,
        )

        if self.text:
            display_text = self.text
            color = TEXT
        else:
            display_text = "Enter your name..."
            color = TEXT_MUTED

        rendered = self.font.render(
            display_text,
            True,
            color,
        )

        screen.blit(
            rendered,
            (
                self.rect.x + 15,
                self.rect.centery
                - rendered.get_height() // 2,
            ),
        )


# ================================================================
# ASSET LOADING
# ================================================================

def load_background(screen_size):

    if not os.path.exists(BACKGROUND_PATH):
        raise FileNotFoundError(
            f"Character creation background "
            f"not found:\n{BACKGROUND_PATH}"
        )

    image = pygame.image.load(
        BACKGROUND_PATH
    ).convert()

    return pygame.transform.scale(
        image,
        screen_size,
    )


def load_character_sprite(
    gender,
    appearance,
    target_height=500,
):
    """Load selected character and scale while preserving ratio."""

    path = character_sprite_path(
        gender,
        appearance,
    )

    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Character sprite not found:\n{path}"
        )

    image = pygame.image.load(
        path
    ).convert_alpha()

    width = image.get_width()
    height = image.get_height()

    scale = target_height / height

    new_width = int(width * scale)

    return pygame.transform.smoothscale(
        image,
        (
            new_width,
            target_height,
        ),
    )


# ================================================================
# HELPER DRAWING
# ================================================================

def draw_selected_button(
    screen,
    rect,
    text,
    font,
    selected,
):
    """Draw a Male/Female selection button."""

    if selected:
        color = SELECTED
    else:
        color = INPUT_NORMAL

    pygame.draw.rect(
        screen,
        color,
        rect,
    )

    pygame.draw.rect(
        screen,
        GOLD,
        rect,
        3,
    )

    label = font.render(
        text,
        True,
        TEXT,
    )

    label_rect = label.get_rect(
        center=rect.center
    )

    screen.blit(
        label,
        label_rect,
    )


# ================================================================
# CHARACTER CREATION SCREEN
# ================================================================

def character_creation_screen(
    screen,
    clock,
    menu_font,
    small_font,
):
    """
    Character creation screen.

    Returns:
        ("back", None)

    or:

        (
            "start",
            {
                "name": str,
                "gender": str,
                "appearance": int,
            },
        )

    or:

        ("quit", None)
    """

    screen_width, screen_height = (
        screen.get_size()
    )

    background = load_background(
        (
            screen_width,
            screen_height,
        )
    )

    # ------------------------------------------------------------
    # CURRENT CHARACTER SETTINGS
    # ------------------------------------------------------------

    gender = "male"
    appearance = 1

    # ------------------------------------------------------------
    # UI LAYOUT
    # ------------------------------------------------------------

    panel_rect = pygame.Rect(
        70,
        70,
        520,
        580,
    )

    name_input = TextInput(
        125,
        205,
        410,
        55,
        small_font,
    )

    male_rect = pygame.Rect(
        125,
        320,
        190,
        50,
    )

    female_rect = pygame.Rect(
        345,
        320,
        190,
        50,
    )

    previous_button = Button(
        "<",
        125,
        440,
        70,
        55,
        menu_font,
    )

    next_button = Button(
        ">",
        465,
        440,
        70,
        55,
        menu_font,
    )

    begin_button = Button(
        "BEGIN ADVENTURE",
        125,
        535,
        410,
        55,
        small_font,
    )

    back_button = Button(
        "BACK",
        125,
        600,
        410,
        40,
        small_font,
    )

    # Cache loaded sprites.
    sprite_cache = {}

    def get_sprite():

        key = (
            gender,
            appearance,
        )

        if key not in sprite_cache:
            sprite_cache[key] = (
                load_character_sprite(
                    gender,
                    appearance,
                )
            )

        return sprite_cache[key]

    # ------------------------------------------------------------
    # MAIN SCREEN LOOP
    # ------------------------------------------------------------

    while True:

        # Begin is only available with a valid name.
        valid_name = bool(
            name_input.text.strip()
        )

        begin_button.enabled = valid_name

        # --------------------------------------------------------
        # EVENTS
        # --------------------------------------------------------

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return "quit", None

            name_input.handle_event(event)

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    return "back", None

            if (
                event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
            ):

                if male_rect.collidepoint(
                    event.pos
                ):
                    gender = "male"

                elif female_rect.collidepoint(
                    event.pos
                ):
                    gender = "female"

            if previous_button.clicked(event):

                appearance -= 1

                if appearance < 1:
                    appearance = 3

            if next_button.clicked(event):

                appearance += 1

                if appearance > 3:
                    appearance = 1

            if back_button.clicked(event):
                return "back", None

            if begin_button.clicked(event):

                character_data = {
                    "name": (
                        name_input.text.strip()
                    ),
                    "gender": gender,
                    "appearance": appearance,
                }

                return (
                    "start",
                    character_data,
                )

        # --------------------------------------------------------
        # DRAW BACKGROUND
        # --------------------------------------------------------

        screen.blit(
            background,
            (0, 0),
        )

        # --------------------------------------------------------
        # LEFT UI PANEL
        # --------------------------------------------------------

        panel = pygame.Surface(
            (
                panel_rect.width,
                panel_rect.height,
            ),
            pygame.SRCALPHA,
        )

        panel.fill(PANEL)

        screen.blit(
            panel,
            panel_rect.topleft,
        )

        pygame.draw.rect(
            screen,
            GOLD,
            panel_rect,
            4,
        )

        # --------------------------------------------------------
        # TITLE
        # --------------------------------------------------------

        title = menu_font.render(
            "CREATE YOUR WANDERER",
            True,
            GOLD,
        )

        title_rect = title.get_rect(
            center=(
                panel_rect.centerx,
                115,
            )
        )

        screen.blit(
            title,
            title_rect,
        )

        # --------------------------------------------------------
        # NAME
        # --------------------------------------------------------

        name_label = small_font.render(
            "NAME",
            True,
            TEXT,
        )

        screen.blit(
            name_label,
            (
                125,
                175,
            ),
        )

        name_input.draw(screen)

        # --------------------------------------------------------
        # GENDER
        # --------------------------------------------------------

        gender_label = small_font.render(
            "GENDER",
            True,
            TEXT,
        )

        screen.blit(
            gender_label,
            (
                125,
                285,
            ),
        )

        draw_selected_button(
            screen,
            male_rect,
            "MALE",
            small_font,
            gender == "male",
        )

        draw_selected_button(
            screen,
            female_rect,
            "FEMALE",
            small_font,
            gender == "female",
        )

        # --------------------------------------------------------
        # APPEARANCE
        # --------------------------------------------------------

        appearance_label = small_font.render(
            f"APPEARANCE {appearance} OF 3",
            True,
            TEXT,
        )

        appearance_label_rect = (
            appearance_label.get_rect(
                center=(
                    panel_rect.centerx,
                    415,
                )
            )
        )

        screen.blit(
            appearance_label,
            appearance_label_rect,
        )

        previous_button.draw(screen)
        next_button.draw(screen)

        # Small color/theme indicator.
        themes = {
            1: "RED",
            2: "BLUE",
            3: "GREEN",
        }

        theme_label = small_font.render(
            themes[appearance],
            True,
            TEXT,
        )

        theme_rect = theme_label.get_rect(
            center=(
                panel_rect.centerx,
                468,
            )
        )

        screen.blit(
            theme_label,
            theme_rect,
        )

        # --------------------------------------------------------
        # ACTION BUTTONS
        # --------------------------------------------------------

        begin_button.draw(screen)
        back_button.draw(screen)

        # --------------------------------------------------------
        # CHARACTER PREVIEW
        # --------------------------------------------------------

        sprite = get_sprite()

        sprite_rect = sprite.get_rect()

        sprite_rect.midbottom = (
            920,
            690,
        )

        # Shadow underneath character.
        shadow_rect = pygame.Rect(
            760,
            655,
            320,
            35,
        )

        shadow_surface = pygame.Surface(
            shadow_rect.size,
            pygame.SRCALPHA,
        )

        pygame.draw.ellipse(
            shadow_surface,
            (0, 0, 0, 100),
            shadow_surface.get_rect(),
        )

        screen.blit(
            shadow_surface,
            shadow_rect.topleft,
        )

        screen.blit(
            sprite,
            sprite_rect,
        )

        # --------------------------------------------------------
        # CHARACTER DESCRIPTION
        # --------------------------------------------------------

        description = small_font.render(
            "Your path has yet to be written.",
            True,
            TEXT,
        )

        description_rect = (
            description.get_rect(
                center=(
                    930,
                    80,
                )
            )
        )

        # Small backing panel for readability.
        description_panel = pygame.Surface(
            (
                description.get_width() + 40,
                45,
            ),
            pygame.SRCALPHA,
        )

        description_panel.fill(
            (0, 0, 0, 145)
        )

        description_panel_rect = (
            description_panel.get_rect(
                center=(
                    930,
                    80,
                )
            )
        )

        screen.blit(
            description_panel,
            description_panel_rect,
        )

        screen.blit(
            description,
            description_rect,
        )

        pygame.display.flip()
        clock.tick(60)