"""Graphical Quest Board for Random Wanderer."""

import pygame

from ui.components import Button


# ================================================================
# COLORS
# ================================================================

BACKGROUND = (12, 20, 32)
PANEL = (20, 35, 55)
CARD = (28, 46, 68)
ACTIVE_CARD = (35, 52, 70)

GOLD = (218, 164, 70)
WHITE = (245, 239, 218)
MUTED = (180, 180, 170)

GOOD = (120, 210, 130)
BAD = (220, 105, 95)

DIVIDER = (110, 95, 70)


# ================================================================
# HELPERS
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


def requirement_text(
    quest_board,
    quest,
):
    """Build a compact quest requirement string."""

    parts = []

    for progress in (
        quest_board.get_quest_progress(
            quest
        )
    ):

        item_name = (
            progress["item"]
            .replace("_", " ")
            .title()
        )

        parts.append(
            f"{item_name}: "
            f"{progress['have']}/"
            f"{progress['required']}"
        )

    return "   ".join(parts)


# ================================================================
# ABANDON CONFIRMATION
# ================================================================

def confirm_abandon(
    screen,
    clock,
    quest_name,
    font,
    small_font,
):
    """Ask the player to confirm abandoning a quest."""

    screen_width, screen_height = (
        screen.get_size()
    )

    yes_button = Button(
        "YES",
        screen_width // 2 - 170,
        screen_height // 2 + 55,
        140,
        45,
        small_font,
    )

    no_button = Button(
        "NO",
        screen_width // 2 + 30,
        screen_height // 2 + 55,
        140,
        45,
        small_font,
    )

    background = screen.copy()

    while True:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    return False

            if yes_button.clicked(event):
                return True

            if no_button.clicked(event):
                return False

        screen.blit(
            background,
            (0, 0),
        )

        overlay = pygame.Surface(
            screen.get_size(),
            pygame.SRCALPHA,
        )

        overlay.fill(
            (0, 0, 0, 150)
        )

        screen.blit(
            overlay,
            (0, 0),
        )

        box_width = 600
        box_height = 230

        box_x = (
            screen_width - box_width
        ) // 2

        box_y = (
            screen_height - box_height
        ) // 2

        box_rect = pygame.Rect(
            box_x,
            box_y,
            box_width,
            box_height,
        )

        pygame.draw.rect(
            screen,
            PANEL,
            box_rect,
            border_radius=10,
        )

        pygame.draw.rect(
            screen,
            GOLD,
            box_rect,
            3,
            border_radius=10,
        )

        draw_centered_text(
            screen,
            "ABANDON QUEST?",
            font,
            GOLD,
            screen_width // 2,
            box_y + 40,
        )

        draw_centered_text(
            screen,
            quest_name,
            small_font,
            WHITE,
            screen_width // 2,
            box_y + 85,
        )

        draw_centered_text(
            screen,
            (
                "Collected items will "
                "remain in your inventory."
            ),
            small_font,
            MUTED,
            screen_width // 2,
            box_y + 120,
        )

        yes_button.draw(screen)
        no_button.draw(screen)

        pygame.display.flip()
        clock.tick(60)


# ================================================================
# QUEST BOARD SCREEN
# ================================================================

def quest_board_screen(
    screen,
    clock,
    player,
    quest_board,
    font,
    small_font,
):
    """Display the graphical Quest Board."""

    screen_width, screen_height = (
        screen.get_size()
    )

    panel_width = min(
        1160,
        screen_width - 60,
    )

    panel_height = min(
        670,
        screen_height - 30,
    )

    panel_x = (
        screen_width - panel_width
    ) // 2

    panel_y = (
        screen_height - panel_height
    ) // 2

    back_button = Button(
        "BACK TO TOWN",
        panel_x + 30,
        panel_y + panel_height - 60,
        220,
        42,
        small_font,
    )

    turn_in_button = Button(
        "TURN IN",
        panel_x + panel_width - 350,
        panel_y + 170,
        140,
        45,
        small_font,
    )

    abandon_button = Button(
        "ABANDON",
        panel_x + panel_width - 190,
        panel_y + 170,
        140,
        45,
        small_font,
    )

    message = ""
    message_good = True

    while True:

        active_quest = (
            quest_board.get_active_quest()
        )

        available_quests = (
            quest_board.get_available_quests()
        )

        # ========================================================
        # AVAILABLE QUEST BUTTONS
        # ========================================================

        accept_buttons = []

        available_start_y = (
            panel_y + 350
        )

        for index, quest in enumerate(
            available_quests
        ):

            button = Button(
                "ACCEPT",
                panel_x + panel_width - 190,
                available_start_y
                + index * 62,
                140,
                42,
                small_font,
            )

            accept_buttons.append(
                button
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

            if back_button.clicked(event):
                return "town"

            # ----------------------------------------------------
            # ACTIVE QUEST ACTIONS
            # ----------------------------------------------------

            if active_quest:

                if turn_in_button.clicked(
                    event
                ):

                    result = (
                        quest_board
                        .turn_in_active()
                    )

                    message = (
                        result["message"]
                    )

                    message_good = (
                        result["success"]
                    )

                if abandon_button.clicked(
                    event
                ):

                    confirmation = (
                        confirm_abandon(
                            screen,
                            clock,
                            active_quest[
                                "name"
                            ],
                            font,
                            small_font,
                        )
                    )

                    if confirmation == "quit":
                        return "quit"

                    if confirmation:

                        result = (
                            quest_board
                            .abandon_active()
                        )

                        message = (
                            result["message"]
                        )

                        message_good = (
                            result["success"]
                        )

            # ----------------------------------------------------
            # ACCEPT QUEST
            # ----------------------------------------------------

            if active_quest is None:

                for index, button in enumerate(
                    accept_buttons
                ):

                    if button.clicked(event):

                        result = (
                            quest_board
                            .accept_quest(
                                available_quests[
                                    index
                                ]
                            )
                        )

                        message = (
                            result["message"]
                        )

                        message_good = (
                            result["success"]
                        )

                        break

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
            "QUEST BOARD",
            font,
            GOLD,
            screen_width // 2,
            panel_y + 35,
        )

        draw_centered_text(
            screen,
            (
                "Take contracts, gather "
                "the required materials, "
                "and return for your reward."
            ),
            small_font,
            MUTED,
            screen_width // 2,
            panel_y + 70,
        )

        draw_text(
            screen,
            (
                f"Level {player.level} "
                f"{player.role}"
            ),
            small_font,
            WHITE,
            panel_x + 40,
            panel_y + 105,
        )

        draw_text(
            screen,
            f"Gold: {player.gold}g",
            small_font,
            GOLD,
            panel_x + 250,
            panel_y + 105,
        )

        draw_text(
            screen,
            (
                "Story Stage: "
                f"{player.story_stage}"
            ),
            small_font,
            MUTED,
            panel_x + 400,
            panel_y + 105,
        )

        pygame.draw.line(
            screen,
            DIVIDER,
            (
                panel_x + 35,
                panel_y + 135,
            ),
            (
                panel_x
                + panel_width
                - 35,
                panel_y + 135,
            ),
            2,
        )

        # ========================================================
        # ACTIVE QUEST
        # ========================================================

        draw_text(
            screen,
            "ACTIVE QUEST",
            small_font,
            GOLD,
            panel_x + 40,
            panel_y + 150,
        )

        active_rect = pygame.Rect(
            panel_x + 35,
            panel_y + 180,
            panel_width - 70,
            125,
        )

        pygame.draw.rect(
            screen,
            ACTIVE_CARD,
            active_rect,
            border_radius=8,
        )

        if active_quest:

            draw_text(
                screen,
                active_quest["name"],
                font,
                WHITE,
                panel_x + 55,
                panel_y + 195,
            )

            progress_string = (
                requirement_text(
                    quest_board,
                    active_quest,
                )
            )

            progress_color = (
                GOOD
                if quest_board.can_turn_in(
                    active_quest
                )
                else MUTED
            )

            draw_text(
                screen,
                progress_string,
                small_font,
                progress_color,
                panel_x + 55,
                panel_y + 235,
            )

            draw_text(
                screen,
                (
                    "Reward: "
                    f"{active_quest['xp']} XP"
                    "  |  "
                    f"{active_quest['gold']} gold"
                ),
                small_font,
                GOLD,
                panel_x + 55,
                panel_y + 265,
            )

            turn_in_button.draw(
                screen
            )

            abandon_button.draw(
                screen
            )

        else:

            draw_text(
                screen,
                "No active quest.",
                font,
                MUTED,
                panel_x + 55,
                panel_y + 215,
            )

            draw_text(
                screen,
                (
                    "Choose one of the "
                    "available contracts below."
                ),
                small_font,
                MUTED,
                panel_x + 55,
                panel_y + 255,
            )

        # ========================================================
        # AVAILABLE QUESTS
        # ========================================================

        draw_text(
            screen,
            "AVAILABLE CONTRACTS",
            small_font,
            GOLD,
            panel_x + 40,
            panel_y + 320,
        )

        if active_quest:

            draw_text(
                screen,
                (
                    "Complete or abandon your "
                    "current quest before "
                    "accepting another."
                ),
                small_font,
                MUTED,
                panel_x + 55,
                panel_y + 365,
            )

        elif not available_quests:

            draw_text(
                screen,
                (
                    "No quests are currently "
                    "available. Progress the "
                    "story or explore."
                ),
                small_font,
                MUTED,
                panel_x + 55,
                panel_y + 365,
            )

        else:

            for index, quest in enumerate(
                available_quests
            ):

                y = (
                    available_start_y
                    + index * 62
                )

                card_rect = pygame.Rect(
                    panel_x + 35,
                    y - 5,
                    panel_width - 70,
                    52,
                )

                pygame.draw.rect(
                    screen,
                    CARD,
                    card_rect,
                    border_radius=6,
                )

                draw_text(
                    screen,
                    quest["name"],
                    small_font,
                    WHITE,
                    panel_x + 55,
                    y + 4,
                )

                requirements = (
                    requirement_text(
                        quest_board,
                        quest,
                    )
                )

                draw_text(
                    screen,
                    requirements,
                    small_font,
                    MUTED,
                    panel_x + 310,
                    y + 4,
                )

                draw_text(
                    screen,
                    (
                        f"{quest['xp']} XP / "
                        f"{quest['gold']}g"
                    ),
                    small_font,
                    GOLD,
                    panel_x + 650,
                    y + 4,
                )

                accept_buttons[
                    index
                ].draw(screen)

        # ========================================================
        # MESSAGE
        # ========================================================

        if message:

            message_color = (
                GOOD
                if message_good
                else BAD
            )

            draw_centered_text(
                screen,
                message,
                small_font,
                message_color,
                screen_width // 2,
                panel_y + panel_height - 85,
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
            panel_x + 280,
            panel_y
            + panel_height
            - 49,
        )

        pygame.display.flip()
        clock.tick(60)