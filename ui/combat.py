"""Graphical combat screen for Random Wanderer."""

import random

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

GREEN = (120, 190, 120)
RED = (205, 100, 100)
YELLOW = (220, 190, 100)

DIVIDER = (110, 95, 70)


# ================================================================
# CORE COMBAT HELPERS
# ================================================================

def hit_success(
    base=0.80,
    modifier=0.0,
):
    """Return True when an attack roll succeeds."""

    chance = max(
        0.05,
        min(
            0.98,
            base + modifier,
        ),
    )

    return random.random() < chance


def calc_damage(
    attack,
    defense,
    multiplier=1.0,
):
    """Calculate damage using the CLI combat formula."""

    raw = max(
        1,
        attack
        - defense
        + random.randint(-1, 2),
    )

    return max(
        1,
        int(raw * multiplier),
    )


def add_log(
    combat_log,
    message,
):
    """Add a message to the combat log."""

    combat_log.append(message)

    # Keep the visible log manageable.
    if len(combat_log) > 8:
        del combat_log[0]


def reset_combat_state(
    player,
    enemies,
):
    """Reset temporary state at the start of combat."""

    if hasattr(
        player,
        "cooldowns",
    ):
        player.cooldowns.clear()

    if hasattr(
        player,
        "status_effects",
    ):
        player.status_effects.clear()

    if hasattr(
        player,
        "guard_active",
    ):
        player.guard_active = False

    if hasattr(
        player,
        "dodge_bonus",
    ):
        player.dodge_bonus = 0.0

    for enemy in enemies:

        enemy.status_effects = {}


# ================================================================
# DRAWING HELPERS
# ================================================================

def draw_centered_text(
    screen,
    text,
    font,
    color,
    center_x,
    y,
):
    """Draw centered text."""

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


def draw_bar(
    screen,
    x,
    y,
    width,
    height,
    current,
    maximum,
):
    """Draw a simple HP/resource bar."""

    maximum = max(
        1,
        maximum,
    )

    ratio = max(
        0.0,
        min(
            1.0,
            current / maximum,
        ),
    )

    background_rect = pygame.Rect(
        x,
        y,
        width,
        height,
    )

    fill_rect = pygame.Rect(
        x,
        y,
        int(width * ratio),
        height,
    )

    pygame.draw.rect(
        screen,
        (55, 55, 55),
        background_rect,
    )

    pygame.draw.rect(
        screen,
        GREEN,
        fill_rect,
    )

    pygame.draw.rect(
        screen,
        WHITE,
        background_rect,
        1,
    )


def draw_enemy_card(
    screen,
    enemy,
    rect,
    font,
    small_font,
    selected=False,
):
    """Draw one enemy card."""

    pygame.draw.rect(
        screen,
        PANEL,
        rect,
    )

    border_color = (
        GOLD
        if selected
        else DIVIDER
    )

    border_width = (
        4
        if selected
        else 2
    )

    pygame.draw.rect(
        screen,
        border_color,
        rect,
        border_width,
    )

    name_surface = font.render(
        enemy.name.title(),
        True,
        WHITE,
    )

    name_rect = name_surface.get_rect(
        center=(
            rect.centerx,
            rect.y + 28,
        )
    )

    screen.blit(
        name_surface,
        name_rect,
    )

    hp_text = small_font.render(
        f"HP: {max(0, enemy.hp)}",
        True,
        WHITE,
    )

    hp_rect = hp_text.get_rect(
        center=(
            rect.centerx,
            rect.y + 62,
        )
    )

    screen.blit(
        hp_text,
        hp_rect,
    )

    if enemy.hp <= 0:

        defeated = small_font.render(
            "DEFEATED",
            True,
            RED,
        )

        defeated_rect = (
            defeated.get_rect(
                center=(
                    rect.centerx,
                    rect.y + 95,
                )
            )
        )

        screen.blit(
            defeated,
            defeated_rect,
        )

    elif selected:

        selected_text = (
            small_font.render(
                "TARGET",
                True,
                GOLD,
            )
        )

        selected_rect = (
            selected_text.get_rect(
                center=(
                    rect.centerx,
                    rect.y + 95,
                )
            )
        )

        screen.blit(
            selected_text,
            selected_rect,
        )


# ================================================================
# TARGET HELPERS
# ================================================================

def living_enemies(
    enemies,
):
    """Return enemies that are still alive."""

    return [
        enemy
        for enemy in enemies
        if enemy.hp > 0
    ]


def first_living_index(
    enemies,
):
    """Return the first living enemy index."""

    for index, enemy in enumerate(
        enemies
    ):

        if enemy.hp > 0:
            return index

    return None


def next_living_index(
    enemies,
    current_index,
):
    """Cycle to the next living enemy."""

    if not enemies:
        return None

    for offset in range(
        1,
        len(enemies) + 1,
    ):

        index = (
            current_index + offset
        ) % len(enemies)

        if enemies[index].hp > 0:
            return index

    return None


# ================================================================
# PLAYER ACTIONS
# ================================================================

def normal_attack(
    player,
    target,
    combat_log,
):
    """Perform the existing normal attack rules."""

    if target is None:
        return False

    if target.hp <= 0:
        return False

    if hit_success():

        multiplier = (
            1.0
            + (
                0.20
                * player.weapon_tier
            )
        )

        # Existing Warrior level 7 passive.
        if (
            player.role == "Warrior"
            and player.level >= 7
        ):
            multiplier += 0.10

        damage = calc_damage(
            player.attack,
            target.defense,
            multiplier,
        )

        target.hp -= damage

        add_log(
            combat_log,
            (
                f"You hit the "
                f"{target.name} "
                f"for {damage}."
            ),
        )

        if target.hp <= 0:

            target.hp = 0

            add_log(
                combat_log,
                (
                    f"The {target.name} "
                    "is defeated!"
                ),
            )

            player.gain_xp(
                getattr(
                    target,
                    "xp",
                    0,
                )
            )

        return True

    add_log(
        combat_log,
        "Your attack missed!",
    )

    return True


def use_healing_tonic(
    player,
    inventory,
    combat_log,
):
    """Use one Healing Tonic."""

    if (
        inventory is None
        or inventory.count(
            "Healing Tonic"
        ) <= 0
    ):

        add_log(
            combat_log,
            "You have no Healing Tonics.",
        )

        return False

    if player.hp >= player.max_hp:

        add_log(
            combat_log,
            "Your HP is already full.",
        )

        return False

    inventory.remove(
        "Healing Tonic",
        1,
    )

    player.hp = player.max_hp

    add_log(
        combat_log,
        (
            "You use a Healing Tonic. "
            "HP fully restored!"
        ),
    )

    return True


# ================================================================
# ENEMY PHASE
# ================================================================

def enemy_phase(
    player,
    enemies,
    combat_log,
):
    """Run attacks for all surviving enemies."""

    for enemy in enemies:

        if enemy.hp <= 0:
            continue

        if player.hp <= 0:
            break

        dodge_bonus = getattr(
            player,
            "dodge_bonus",
            0.0,
        )

        if hit_success(
            modifier=-dodge_bonus
        ):

            total_defense = (
                player.defense
                + player.armor_tier
                + player.shield_tier
            )

            # Existing Warrior level 7 passive.
            if (
                player.role == "Warrior"
                and player.level >= 7
            ):
                total_defense += 1

            damage = calc_damage(
                enemy.atk,
                total_defense,
            )

            guard_active = getattr(
                player,
                "guard_active",
                False,
            )

            if guard_active:

                reduction = min(
                    0.75,
                    (
                        0.40
                        + (
                            0.05
                            * player.shield_tier
                        )
                    ),
                )

                damage = max(
                    1,
                    int(
                        damage
                        * (
                            1.0
                            - reduction
                        )
                    ),
                )

                player.guard_active = False

                add_log(
                    combat_log,
                    (
                        "Your guard absorbs "
                        "part of the blow!"
                    ),
                )

            player.hp = max(
                0,
                player.hp - damage,
            )

            add_log(
                combat_log,
                (
                    f"The {enemy.name} "
                    f"hits you for "
                    f"{damage}."
                ),
            )

        else:

            add_log(
                combat_log,
                (
                    f"The {enemy.name} "
                    "misses."
                ),
            )

    if hasattr(
        player,
        "dodge_bonus",
    ):
        player.dodge_bonus = 0.0


# ================================================================
# RESOURCE REGENERATION
# ================================================================

def regenerate_resource(
    player,
    combat_log,
):
    """Apply existing per-turn class resource regeneration."""

    resource_type = getattr(
        player,
        "resource_type",
        None,
    )

    if not resource_type:
        return

    maximum = getattr(
        player,
        "max_resource",
        0,
    )

    current = getattr(
        player,
        "resource",
        0,
    )

    old_resource = current

    player.resource = min(
        maximum,
        current + 10,
    )

    gained = (
        player.resource
        - old_resource
    )

    if gained:

        add_log(
            combat_log,
            (
                f"You recover {gained} "
                f"{resource_type}."
            ),
        )


# ================================================================
# COMBAT SCREEN
# ================================================================

def combat_screen(
    screen,
    clock,
    player,
    inventory,
    enemies,
    font,
    small_font,
):
    """Run a graphical combat encounter."""

    screen_width, screen_height = (
        screen.get_size()
    )

    reset_combat_state(
        player,
        enemies,
    )

    combat_log = [
        "Enemies approach!",
    ]

    selected_index = (
        first_living_index(
            enemies
        )
    )

    turn = 1

    # ------------------------------------------------------------
    # BUTTONS
    # ------------------------------------------------------------

    attack_button = Button(
        "ATTACK",
        70,
        575,
        220,
        55,
        small_font,
    )

    ability_button = Button(
        "ABILITIES",
        310,
        575,
        220,
        55,
        small_font,
    )

    item_button = Button(
        "HEALING TONIC",
        550,
        575,
        220,
        55,
        small_font,
    )

    run_button = Button(
        "RUN",
        790,
        575,
        180,
        55,
        small_font,
    )

    target_button = Button(
        "NEXT TARGET",
        990,
        575,
        220,
        55,
        small_font,
    )

    # ------------------------------------------------------------
    # MAIN LOOP
    # ------------------------------------------------------------

    while True:

        # ========================================================
        # CHECK RESULTS
        # ========================================================

        if player.hp <= 0:

            return {
                "outcome": "lost",
                "enemies": enemies,
            }

        if not living_enemies(
            enemies
        ):

            return {
                "outcome": "won",
                "enemies": enemies,
            }

        if (
            selected_index is None
            or enemies[
                selected_index
            ].hp <= 0
        ):

            selected_index = (
                first_living_index(
                    enemies
                )
            )

        # ========================================================
        # EVENTS
        # ========================================================

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                return {
                    "outcome": "quit",
                    "enemies": enemies,
                }

            # ----------------------------------------------------
            # TARGET CARDS
            # ----------------------------------------------------

            if event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 1:

                    living_count = len(
                        enemies
                    )

                    if living_count:

                        card_width = 250
                        card_gap = 25

                        total_width = (
                            len(enemies)
                            * card_width
                            + (
                                len(enemies) - 1
                            )
                            * card_gap
                        )

                        start_x = (
                            screen_width
                            - total_width
                        ) // 2

                        for index, enemy in enumerate(
                            enemies
                        ):

                            card_rect = pygame.Rect(
                                start_x
                                + index
                                * (
                                    card_width
                                    + card_gap
                                ),
                                155,
                                card_width,
                                125,
                            )

                            if (
                                enemy.hp > 0
                                and card_rect.collidepoint(
                                    event.pos
                                )
                            ):

                                selected_index = index

            # ----------------------------------------------------
            # ATTACK
            # ----------------------------------------------------

            if attack_button.clicked(event):

                if selected_index is not None:

                    acted = normal_attack(
                        player,
                        enemies[
                            selected_index
                        ],
                        combat_log,
                    )

                    if acted:

                        if living_enemies(
                            enemies
                        ):

                            enemy_phase(
                                player,
                                enemies,
                                combat_log,
                            )

                            if player.hp > 0:

                                regenerate_resource(
                                    player,
                                    combat_log,
                                )

                        turn += 1

            # ----------------------------------------------------
            # ABILITIES PLACEHOLDER
            # ----------------------------------------------------

            if ability_button.clicked(event):

                add_log(
                    combat_log,
                    (
                        "Class abilities will "
                        "be added in the next "
                        "combat pass."
                    ),
                )

            # ----------------------------------------------------
            # HEALING TONIC
            # ----------------------------------------------------

            if item_button.clicked(event):

                acted = use_healing_tonic(
                    player,
                    inventory,
                    combat_log,
                )

                if acted:

                    enemy_phase(
                        player,
                        enemies,
                        combat_log,
                    )

                    if player.hp > 0:

                        regenerate_resource(
                            player,
                            combat_log,
                        )

                    turn += 1

            # ----------------------------------------------------
            # RUN
            # ----------------------------------------------------

            if run_button.clicked(event):

                if random.random() < 0.5:

                    add_log(
                        combat_log,
                        "You fled successfully.",
                    )

                    return {
                        "outcome": "fled",
                        "enemies": enemies,
                    }

                add_log(
                    combat_log,
                    "You failed to run!",
                )

                enemy_phase(
                    player,
                    enemies,
                    combat_log,
                )

                if player.hp > 0:

                    regenerate_resource(
                        player,
                        combat_log,
                    )

                turn += 1

            # ----------------------------------------------------
            # NEXT TARGET
            # ----------------------------------------------------

            if target_button.clicked(event):

                if selected_index is not None:

                    selected_index = (
                        next_living_index(
                            enemies,
                            selected_index,
                        )
                    )

        # ========================================================
        # DRAW BACKGROUND
        # ========================================================

        screen.fill(BACKGROUND)

        # ========================================================
        # HEADER
        # ========================================================

        draw_centered_text(
            screen,
            f"COMBAT — TURN {turn}",
            font,
            GOLD,
            screen_width // 2,
            35,
        )

        # ========================================================
        # PLAYER PANEL
        # ========================================================

        player_panel = pygame.Rect(
            45,
            65,
            screen_width - 90,
            70,
        )

        pygame.draw.rect(
            screen,
            PANEL,
            player_panel,
        )

        pygame.draw.rect(
            screen,
            DIVIDER,
            player_panel,
            2,
        )

        player_text = small_font.render(
            (
                f"{player.name}    "
                f"Level {player.level} "
                f"{player.role}"
            ),
            True,
            WHITE,
        )

        screen.blit(
            player_text,
            (
                player_panel.x + 20,
                player_panel.y + 12,
            ),
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

        screen.blit(
            hp_text,
            (
                player_panel.x + 20,
                player_panel.y + 39,
            ),
        )

        draw_bar(
            screen,
            player_panel.x + 135,
            player_panel.y + 42,
            250,
            15,
            player.hp,
            player.max_hp,
        )

        resource_type = getattr(
            player,
            "resource_type",
            None,
        )

        if resource_type:

            resource_text = (
                small_font.render(
                    (
                        f"{resource_type}: "
                        f"{player.resource}/"
                        f"{player.max_resource}"
                    ),
                    True,
                    WHITE,
                )
            )

            screen.blit(
                resource_text,
                (
                    player_panel.right - 280,
                    player_panel.y + 25,
                ),
            )

        # ========================================================
        # ENEMIES
        # ========================================================

        card_width = 250
        card_gap = 25

        total_width = (
            len(enemies)
            * card_width
            + (
                len(enemies) - 1
            )
            * card_gap
        )

        start_x = (
            screen_width - total_width
        ) // 2

        for index, enemy in enumerate(
            enemies
        ):

            card_rect = pygame.Rect(
                start_x
                + index
                * (
                    card_width
                    + card_gap
                ),
                155,
                card_width,
                125,
            )

            draw_enemy_card(
                screen,
                enemy,
                card_rect,
                small_font,
                small_font,
                selected=(
                    index
                    == selected_index
                    and enemy.hp > 0
                ),
            )

        # ========================================================
        # COMBAT LOG
        # ========================================================

        log_panel = pygame.Rect(
            110,
            310,
            screen_width - 220,
            225,
        )

        pygame.draw.rect(
            screen,
            PANEL,
            log_panel,
        )

        pygame.draw.rect(
            screen,
            DIVIDER,
            log_panel,
            2,
        )

        log_title = small_font.render(
            "COMBAT LOG",
            True,
            GOLD,
        )

        screen.blit(
            log_title,
            (
                log_panel.x + 20,
                log_panel.y + 15,
            ),
        )

        log_y = (
            log_panel.y + 48
        )

        for message in combat_log:

            message_surface = (
                small_font.render(
                    message,
                    True,
                    WHITE,
                )
            )

            screen.blit(
                message_surface,
                (
                    log_panel.x + 20,
                    log_y,
                ),
            )

            log_y += 21

        # ========================================================
        # BUTTONS
        # ========================================================

        attack_button.draw(screen)
        ability_button.draw(screen)
        item_button.draw(screen)
        run_button.draw(screen)
        target_button.draw(screen)

        # ========================================================
        # FOOTER
        # ========================================================

        selected_enemy = None

        if selected_index is not None:

            selected_enemy = enemies[
                selected_index
            ]

        if selected_enemy:

            target_text = (
                f"Target: "
                f"{selected_enemy.name.title()}"
            )

        else:

            target_text = (
                "Target: None"
            )

        draw_centered_text(
            screen,
            target_text,
            small_font,
            MUTED,
            screen_width // 2,
            665,
        )

        pygame.display.flip()
        clock.tick(60)