"""Graphical Guild Hall and main-story interface."""

import pygame

from ui.components import Button


# ================================================================
# COLORS
# ================================================================

BACKGROUND = (10, 16, 27)
PANEL = (20, 32, 49)
CARD = (28, 43, 62)

GOLD = (218, 164, 70)
WHITE = (245, 239, 218)
MUTED = (175, 178, 180)
GOOD = (120, 210, 130)
BAD = (220, 105, 95)

DIVIDER = (105, 91, 68)


# ================================================================
# TEXT HELPERS
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

            current_line = (
                test_line
            )

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
# GUILD HALL
# ================================================================

def guild_hall_screen(
    screen,
    clock,
    player,
    story,
    font,
    small_font,
):
    """Display the graphical main-story interface."""

    screen_width, screen_height = (
        screen.get_size()
    )

    panel_width = 1040
    panel_height = 650

    panel_x = (
        screen_width - panel_width
    ) // 2

    panel_y = (
        screen_height - panel_height
    ) // 2

    back_button = Button(
        "BACK TO TOWN",
        panel_x + 30,
        panel_y + panel_height - 58,
        210,
        40,
        small_font,
    )

    message = None
    message_good = True

    while True:

        stage = (
            player.story_stage
        )

        info = (
            story.get_stage_info()
        )

        level_progress = (
            story.get_level_progress()
        )

        required_level = (
            level_progress[
                "required_level"
            ]
        )

        level_unlocked = (
            level_progress[
                "unlocked"
            ]
        )

        last_message = (
            story.get_last_message()
        )

        # ========================================================
        # ACTION BUTTONS
        # ========================================================

        begin_button = None
        boss_button = None

        hero_button = None
        rebel_button = None
        wanderer_button = None
        duel_button = None

        # --------------------------------------------------------
        # PROLOGUE
        # --------------------------------------------------------

        if stage == 0:

            begin_button = Button(
                "BEGIN ACT I",
                panel_x + 365,
                panel_y + 450,
                310,
                52,
                small_font,
            )

        # --------------------------------------------------------
        # STORY BOSSES
        # --------------------------------------------------------

        elif stage in range(
            1,
            7,
        ):

            boss_name = (
                info["boss"]
                .replace(
                    "_",
                    " ",
                )
                .title()
            )

            if level_unlocked:

                boss_label = (
                    "FACE "
                    f"{boss_name.upper()}"
                )

            else:

                boss_label = (
                    "CONTRACT LOCKED - "
                    f"LEVEL {required_level}"
                )

            boss_button = Button(
                boss_label,
                panel_x + 320,
                panel_y + 450,
                400,
                52,
                small_font,
            )

        # --------------------------------------------------------
        # FINALE
        # --------------------------------------------------------

        elif stage == 7:

            if level_unlocked:

                hero_label = (
                    "KING'S HONOR"
                )

                rebel_label = (
                    "SIDE WITH KAELEN"
                )

                wanderer_label = (
                    "WALK AWAY"
                )

                duel_label = (
                    "CHALLENGE KAELEN"
                )

            else:

                hero_label = (
                    "FINALE LOCKED"
                )

                rebel_label = (
                    "FINALE LOCKED"
                )

                wanderer_label = (
                    "FINALE LOCKED"
                )

                duel_label = (
                    "REQUIRES LEVEL 20"
                )

            hero_button = Button(
                hero_label,
                panel_x + 90,
                panel_y + 425,
                250,
                48,
                small_font,
            )

            rebel_button = Button(
                rebel_label,
                panel_x + 395,
                panel_y + 425,
                250,
                48,
                small_font,
            )

            wanderer_button = Button(
                wanderer_label,
                panel_x + 700,
                panel_y + 425,
                250,
                48,
                small_font,
            )

            duel_button = Button(
                duel_label,
                panel_x + 365,
                panel_y + 485,
                310,
                48,
                small_font,
            )

        # ========================================================
        # EVENTS
        # ========================================================

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    return "town"

            if back_button.clicked(
                event
            ):
                return "town"

            # ----------------------------------------------------
            # BEGIN STORY
            # ----------------------------------------------------

            if (
                begin_button
                and begin_button.clicked(
                    event
                )
            ):

                result = (
                    story.begin_story()
                )

                message = (
                    result["message"]
                )

                message_good = (
                    result["success"]
                )

            # ----------------------------------------------------
            # STORY BOSS
            # ----------------------------------------------------

            if (
                boss_button
                and boss_button.clicked(
                    event
                )
            ):

                if not level_unlocked:

                    message = (
                        "The Guild will authorize "
                        "this contract at Level "
                        f"{required_level}. "
                        "Current Level: "
                        f"{player.level}."
                    )

                    message_good = False

                else:

                    enemy = (
                        story
                        .create_current_boss()
                    )

                    if enemy is not None:

                        return (
                            "story_combat",
                            [enemy],
                            "boss",
                        )

                    message = (
                        "The contract could not "
                        "be started."
                    )

                    message_good = False

            # ----------------------------------------------------
            # HERO ENDING
            # ----------------------------------------------------

            if (
                hero_button
                and hero_button.clicked(
                    event
                )
            ):

                if not level_unlocked:

                    message = (
                        "The finale requires "
                        f"Level {required_level}. "
                        "Current Level: "
                        f"{player.level}."
                    )

                    message_good = False

                else:

                    result = (
                        story.choose_ending(
                            "Hero"
                        )
                    )

                    message = (
                        result["message"]
                    )

                    message_good = (
                        result["success"]
                    )

            # ----------------------------------------------------
            # REBEL ENDING
            # ----------------------------------------------------

            if (
                rebel_button
                and rebel_button.clicked(
                    event
                )
            ):

                if not level_unlocked:

                    message = (
                        "The finale requires "
                        f"Level {required_level}. "
                        "Current Level: "
                        f"{player.level}."
                    )

                    message_good = False

                else:

                    result = (
                        story.choose_ending(
                            "Rebel"
                        )
                    )

                    message = (
                        result["message"]
                    )

                    message_good = (
                        result["success"]
                    )

            # ----------------------------------------------------
            # WANDERER ENDING
            # ----------------------------------------------------

            if (
                wanderer_button
                and wanderer_button.clicked(
                    event
                )
            ):

                if not level_unlocked:

                    message = (
                        "The finale requires "
                        f"Level {required_level}. "
                        "Current Level: "
                        f"{player.level}."
                    )

                    message_good = False

                else:

                    result = (
                        story.choose_ending(
                            "Wanderer"
                        )
                    )

                    message = (
                        result["message"]
                    )

                    message_good = (
                        result["success"]
                    )

            # ----------------------------------------------------
            # KAELEN DUEL
            # ----------------------------------------------------

            if (
                duel_button
                and duel_button.clicked(
                    event
                )
            ):

                if not level_unlocked:

                    message = (
                        "You must reach Level "
                        f"{required_level} before "
                        "challenging Kaelen. "
                        "Current Level: "
                        f"{player.level}."
                    )

                    message_good = False

                else:

                    enemy = (
                        story
                        .create_kaelen_boss()
                    )

                    if enemy is not None:

                        return (
                            "story_combat",
                            [enemy],
                            "kaelen",
                        )

                    message = (
                        "Kaelen cannot be "
                        "challenged right now."
                    )

                    message_good = False

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
            "GUILD HALL",
            font,
            GOLD,
            screen_width // 2,
            panel_y + 38,
        )

        draw_centered_text(
            screen,
            "MAIN STORY",
            small_font,
            MUTED,
            screen_width // 2,
            panel_y + 72,
        )

        draw_text(
            screen,
            (
                f"Level {player.level} "
                f"{player.role}"
            ),
            small_font,
            WHITE,
            panel_x + 45,
            panel_y + 105,
        )

        draw_text(
            screen,
            (
                "Story Stage: "
                f"{player.story_stage}"
            ),
            small_font,
            WHITE,
            panel_x + 780,
            panel_y + 105,
        )

        pygame.draw.line(
            screen,
            DIVIDER,
            (
                panel_x + 40,
                panel_y + 140,
            ),
            (
                panel_x
                + panel_width
                - 40,
                panel_y + 140,
            ),
            2,
        )

        # ========================================================
        # STORY CARD
        # ========================================================

        story_rect = pygame.Rect(
            panel_x + 60,
            panel_y + 170,
            panel_width - 120,
            220,
        )

        pygame.draw.rect(
            screen,
            CARD,
            story_rect,
            border_radius=10,
        )

        pygame.draw.rect(
            screen,
            DIVIDER,
            story_rect,
            2,
            border_radius=10,
        )

        draw_centered_text(
            screen,
            info["title"],
            font,
            GOLD,
            story_rect.centerx,
            story_rect.y + 32,
        )

        draw_text(
            screen,
            info["speaker"],
            small_font,
            GOLD,
            story_rect.x + 25,
            story_rect.y + 70,
        )

        dialogue_rect = pygame.Rect(
            story_rect.x + 25,
            story_rect.y + 98,
            story_rect.width - 50,
            50,
        )

        draw_wrapped_text(
            screen,
            info["text"],
            small_font,
            WHITE,
            dialogue_rect,
        )

        draw_text(
            screen,
            (
                "Objective: "
                f"{info['objective']}"
            ),
            small_font,
            MUTED,
            story_rect.x + 25,
            story_rect.y + 158,
        )

        # ========================================================
        # LEVEL REQUIREMENT
        # ========================================================

        if stage in range(
            1,
            8,
        ):

            if level_unlocked:

                requirement_text = (
                    "Guild Rank: "
                    f"Level {player.level} "
                    f"/ {required_level} "
                    "- AUTHORIZED"
                )

                requirement_color = (
                    GOOD
                )

            else:

                requirement_text = (
                    "Guild Rank: "
                    f"Level {player.level} "
                    f"/ {required_level} "
                    "- CONTRACT LOCKED"
                )

                requirement_color = (
                    GOLD
                )

            draw_text(
                screen,
                requirement_text,
                small_font,
                requirement_color,
                story_rect.x + 25,
                story_rect.y + 185,
            )

        # ========================================================
        # ACTION BUTTONS
        # ========================================================

        if begin_button:

            begin_button.draw(
                screen
            )

        if boss_button:

            boss_button.draw(
                screen
            )

        if hero_button:

            hero_button.draw(
                screen
            )

            rebel_button.draw(
                screen
            )

            wanderer_button.draw(
                screen
            )

            duel_button.draw(
                screen
            )

        # ========================================================
        # RESULT / STORY MESSAGE
        # ========================================================

        display_message = (
            message
        )

        if (
            display_message is None
            and last_message
        ):

            display_message = (
                f"{last_message['speaker']}: "
                f"{last_message['text']}"
            )

        if display_message:

            message_rect = pygame.Rect(
                panel_x + 100,
                panel_y + 545,
                panel_width - 200,
                45,
            )

            message_color = (
                GOOD
                if message_good
                else BAD
            )

            draw_wrapped_text(
                screen,
                display_message,
                small_font,
                message_color,
                message_rect,
            )

        # ========================================================
        # EPILOGUE
        # ========================================================

        if stage == 8:

            ending_name = (
                story.ending_name
                or "Completed"
            )

            draw_centered_text(
                screen,
                (
                    "ENDING UNLOCKED: "
                    f"{ending_name.upper()}"
                ),
                small_font,
                GOOD,
                screen_width // 2,
                panel_y + 455,
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
            panel_x + 270,
            panel_y
            + panel_height
            - 47,
        )

        pygame.display.flip()

        clock.tick(
            60
        )