"""Graphical combat screen for Random Wanderer."""



import random



import pygame



from abilities import ABILITIES

from ui.components import Button





# ================================================================

# COLORS

# ================================================================



BACKGROUND = (12, 20, 32)

PANEL = (20, 35, 55)

OVERLAY = (8, 14, 22)



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



    if len(combat_log) > 8:

        del combat_log[0]





def reset_combat_state(

    player,

    enemies,

):

    """Reset temporary encounter state."""



    player.cooldowns.clear()

    player.status_effects.clear()



    player.guard_active = False

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

    fill_color=GREEN,

):

    """Draw a simple status bar."""



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

        fill_color,

        fill_rect,

    )



    pygame.draw.rect(

        screen,

        WHITE,

        background_rect,

        1,

    )





def wrap_text(

    text,

    font,

    max_width,

):

    """Wrap text to a maximum pixel width."""



    words = text.split()



    lines = []

    current = ""



    for word in words:



        test = (

            word

            if not current

            else f"{current} {word}"

        )



        if font.size(test)[0] <= max_width:



            current = test



        else:



            if current:

                lines.append(current)



            current = word



    if current:

        lines.append(current)



    return lines





def draw_enemy_card(

    screen,

    enemy,

    rect,

    font,

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



    pygame.draw.rect(

        screen,

        border_color,

        rect,

        4 if selected else 2,

    )



    draw_centered_text(

        screen,

        enemy.name.title(),

        font,

        WHITE,

        rect.centerx,

        rect.y + 25,

    )



    draw_centered_text(

        screen,

        f"HP: {max(0, enemy.hp)}",

        font,

        WHITE,

        rect.centerx,

        rect.y + 54,

    )



    poison = (

        enemy.status_effects.get(

            "poison"

        )

    )



    if enemy.hp <= 0:



        draw_centered_text(

            screen,

            "DEFEATED",

            font,

            RED,

            rect.centerx,

            rect.y + 88,

        )



    elif poison:



        draw_centered_text(

            screen,

            (

                "POISONED "

                f"({poison['turns']})"

            ),

            font,

            GREEN,

            rect.centerx,

            rect.y + 88,

        )



    elif selected:



        draw_centered_text(

            screen,

            "TARGET",

            font,

            GOLD,

            rect.centerx,

            rect.y + 88,

        )





# ================================================================

# TARGET HELPERS

# ================================================================



def living_enemies(enemies):

    """Return all living enemies."""



    return [

        enemy

        for enemy in enemies

        if enemy.hp > 0

    ]





def first_living_index(enemies):

    """Return index of first living enemy."""



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

# KILL / XP HELPER

# ================================================================



def check_enemy_defeat(

    player,

    enemy,

    combat_log,

):

    """

    Award XP if an enemy has just been defeated.



    Returns True when the enemy is dead.

    """



    if enemy.hp > 0:

        return False



    enemy.hp = 0



    add_log(

        combat_log,

        f"The {enemy.name} is defeated!",

    )



    player.gain_xp(

        getattr(

            enemy,

            "xp",

            0,

        )

    )



    return True





# ================================================================

# NORMAL ATTACK

# ================================================================



def normal_attack(

    player,

    target,

    combat_log,

):

    """Perform a normal player attack."""



    if (

        target is None

        or target.hp <= 0

    ):

        return False



    if hit_success():



        multiplier = (

            1.0

            + (

                0.20

                * player.weapon_tier

            )

        )



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



            check_enemy_defeat(

                player,

                target,

                combat_log,

            )



    else:



        add_log(

            combat_log,

            "Your attack missed!",

        )



    return True





# ================================================================

# ITEM

# ================================================================



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



    # The CLI allows the tonic even at full HP,

    # but avoiding accidental waste is useful in

    # the graphical interface.

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

# COOLDOWNS

# ================================================================



def set_cooldown(

    player,

    ability_key,

):

    """Apply an ability cooldown."""



    ability = ABILITIES[

        player.role

    ][ability_key]



    cooldown = ability.get(

        "cooldown",

        0,

    )



    # Matches the CLI implementation.

    # Cooldowns tick at the end of the

    # current acted round.

    if cooldown > 0:



        player.cooldowns[

            ability_key

        ] = cooldown + 1





def tick_cooldowns(player):

    """Reduce active cooldowns by one."""



    for ability_key in list(

        player.cooldowns

    ):



        player.cooldowns[

            ability_key

        ] -= 1



        if (

            player.cooldowns[

                ability_key

            ] <= 0

        ):



            del player.cooldowns[

                ability_key

            ]





# ================================================================

# POISON

# ================================================================



def apply_poison(

    player,

    target,

    combat_log,

):

    """Apply or refresh Poison."""



    poison_damage = max(

        1,

        int(

            player.attack * 0.25

        ),

    )



    target.status_effects[

        "poison"

    ] = {

        "damage": poison_damage,

        "turns": 3,

    }



    add_log(

        combat_log,

        (

            f"The {target.name} "

            "has been poisoned!"

        ),

    )





def process_enemy_statuses(

    player,

    enemies,

    combat_log,

):

    """Process poison after the enemy phase."""



    for enemy in enemies:



        if enemy.hp <= 0:

            continue



        poison = (

            enemy.status_effects.get(

                "poison"

            )

        )



        if not poison:

            continue



        damage = poison["damage"]



        enemy.hp = max(

            0,

            enemy.hp - damage,

        )



        add_log(

            combat_log,

            (

                f"Poison deals {damage} "

                f"damage to the "

                f"{enemy.name}!"

            ),

        )



        poison["turns"] -= 1



        if enemy.hp <= 0:



            add_log(

                combat_log,

                (

                    f"The {enemy.name} "

                    "succumbs to the poison!"

                ),

            )



            player.gain_xp(

                getattr(

                    enemy,

                    "xp",

                    0,

                )

            )



            continue



        if poison["turns"] <= 0:



            del enemy.status_effects[

                "poison"

            ]



            add_log(

                combat_log,

                (

                    "The poison on the "

                    f"{enemy.name} "

                    "wears off."

                ),

            )





# ================================================================

# RESOURCE REGENERATION

# ================================================================



def regenerate_resource(

    player,

    combat_log,

):

    """Regenerate 10 class resource after an acted round."""



    if not player.resource_type:

        return



    old_resource = player.resource



    player.resource = min(

        player.max_resource,

        player.resource + 10,

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

                f"{player.resource_type}."

            ),

        )





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



        # --------------------------------------------------------

        # VANISH

        # --------------------------------------------------------



        vanish = (

            player.status_effects.get(

                "vanish"

            )

        )



        if (

            vanish

            and vanish.get(

                "evade_next"

            )

        ):



            add_log(

                combat_log,

                (

                    f"The {enemy.name} attacks, "

                    "but you vanish from sight!"

                ),

            )



            vanish[

                "evade_next"

            ] = False



            continue



        # --------------------------------------------------------

        # NORMAL ENEMY ATTACK

        # --------------------------------------------------------



        if hit_success(

            modifier=(

                -player.dodge_bonus

            )

        ):



            total_defense = (

                player.defense

                + player.armor_tier

                + player.shield_tier

            )



            if (

                player.role == "Warrior"

                and player.level >= 7

            ):

                total_defense += 1



            damage = calc_damage(

                enemy.atk,

                total_defense,

            )



            # ----------------------------------------------------

            # WARRIOR GUARD

            # ----------------------------------------------------



            if player.guard_active:



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



    # Nimble Feet only lasts through

    # the current enemy phase.

    if player.dodge_bonus > 0:



        player.dodge_bonus = 0.0





# ================================================================

# COMPLETE ACTED ROUND

# ================================================================



def finish_round(

    player,

    enemies,

    combat_log,

):

    """Process everything following a player action."""



    enemy_phase(

        player,

        enemies,

        combat_log,

    )



    # Matches CLI order:

    # enemy attacks -> statuses -> resource -> cooldowns



    process_enemy_statuses(

        player,

        enemies,

        combat_log,

    )



    regenerate_resource(

        player,

        combat_log,

    )



    tick_cooldowns(

        player

    )





# ================================================================

# ABILITY HELPERS

# ================================================================



def available_abilities(player):

    """Return active abilities unlocked by the player."""



    class_abilities = ABILITIES.get(

        player.role,

        {},

    )



    return [

        (key, ability)

        for key, ability

        in class_abilities.items()

        if (

            player.level

            >= ability["level"]

            and ability.get(

                "type",

                "active",

            ) == "active"

        )

    ]





def ability_ready(

    player,

    ability_key,

    combat_log,

):

    """Validate cooldown and resource cost."""



    ability = ABILITIES[

        player.role

    ][ability_key]



    cooldown_remaining = (

        player.cooldowns.get(

            ability_key,

            0,

        )

    )



    if cooldown_remaining > 0:



        add_log(

            combat_log,

            (

                f"{ability['name']} is on "

                "cooldown for "

                f"{cooldown_remaining} "

                "more turn(s)."

            ),

        )



        return False



    cost = ability["cost"]



    if player.resource < cost:



        add_log(

            combat_log,

            (

                f"Not enough "

                f"{player.resource_type}. "

                f"Need {cost}, "

                f"have {player.resource}."

            ),

        )



        return False



    return True





# ================================================================

# ABILITY EXECUTION

# ================================================================



def use_ability(

    player,

    ability_key,

    target,

    turn,

    combat_log,

):

    """

    Execute one graphical class ability.



    Returns True when the player's turn was used.

    """



    if not ability_ready(

        player,

        ability_key,

        combat_log,

    ):



        return False



    ability = ABILITIES[

        player.role

    ][ability_key]



    cost = ability["cost"]



    # ============================================================

    # WARRIOR

    # ============================================================



    if ability_key == "guard":



        player.resource -= cost

        player.guard_active = True



        add_log(

            combat_log,

            (

                "You raise your guard and "

                "brace for the next attack."

            ),

        )



        return True



    if ability_key == "mighty_strike":



        if (

            target is None

            or target.hp <= 0

        ):

            return False



        player.resource -= cost



        if hit_success():



            multiplier = (

                1.5

                + (

                    0.20

                    * player.weapon_tier

                )

            )



            if player.level >= 7:

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

                    "Mighty Strike hits the "

                    f"{target.name} for "

                    f"{damage} damage!"

                ),

            )



            if target.hp <= 0:



                check_enemy_defeat(

                    player,

                    target,

                    combat_log,

                )



        else:



            add_log(

                combat_log,

                "Mighty Strike misses!",

            )



        return True



    if ability_key == "critical_strike":



        if (

            target is None

            or target.hp <= 0

        ):

            return False



        player.resource -= cost



        if hit_success(

            base=0.65

        ):



            multiplier = (

                2.0

                + (

                    0.20

                    * player.weapon_tier

                )

            )



            if player.level >= 7:

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

                    "Critical Strike devastates "

                    f"the {target.name} for "

                    f"{damage} damage!"

                ),

            )



            if target.hp <= 0:



                check_enemy_defeat(

                    player,

                    target,

                    combat_log,

                )



        else:



            add_log(

                combat_log,

                "Critical Strike misses!",

            )



        set_cooldown(

            player,

            ability_key,

        )



        return True



    # ============================================================

    # MAGE

    # ============================================================



    if ability_key == "small_heal":



        if player.hp >= player.max_hp:



            add_log(

                combat_log,

                "Your HP is already full.",

            )



            return False



        player.resource -= cost



        heal = max(

            1,

            int(

                player.max_hp * 0.25

            ),

        )



        old_hp = player.hp



        player.hp = min(

            player.max_hp,

            player.hp + heal,

        )



        healed = (

            player.hp - old_hp

        )



        add_log(

            combat_log,

            (

                f"You restore "

                f"{healed} HP."

            ),

        )



        return True



    if ability_key == "fire_bolt":



        if (

            target is None

            or target.hp <= 0

        ):

            return False



        player.resource -= cost



        if hit_success(

            base=0.90

        ):



            damage = calc_damage(

                player.attack,

                target.defense,

                1.35,

            )



            target.hp -= damage



            add_log(

                combat_log,

                (

                    "Fire Bolt scorches the "

                    f"{target.name} for "

                    f"{damage} damage!"

                ),

            )



            if target.hp <= 0:



                check_enemy_defeat(

                    player,

                    target,

                    combat_log,

                )



        else:



            add_log(

                combat_log,

                "Fire Bolt misses!",

            )



        return True



    if ability_key == "lightning_bolt":



        if (

            target is None

            or target.hp <= 0

        ):

            return False



        player.resource -= cost



        if hit_success(

            base=0.95

        ):



            damage = calc_damage(

                player.attack,

                target.defense,

                1.75,

            )



            target.hp -= damage



            add_log(

                combat_log,

                (

                    "Lightning Bolt strikes "

                    f"the {target.name} for "

                    f"{damage} damage!"

                ),

            )



            if target.hp <= 0:



                check_enemy_defeat(

                    player,

                    target,

                    combat_log,

                )



        else:



            add_log(

                combat_log,

                "Lightning Bolt misses!",

            )



        set_cooldown(

            player,

            ability_key,

        )



        return True



    if ability_key == "greater_heal":



        if player.hp >= player.max_hp:



            add_log(

                combat_log,

                "Your HP is already full.",

            )



            return False



        player.resource -= cost



        heal = max(

            1,

            int(

                player.max_hp * 0.50

            ),

        )



        old_hp = player.hp



        player.hp = min(

            player.max_hp,

            player.hp + heal,

        )



        healed = (

            player.hp - old_hp

        )



        add_log(

            combat_log,

            (

                "Greater Heal restores "

                f"{healed} HP!"

            ),

        )



        set_cooldown(

            player,

            ability_key,

        )



        return True



    # ============================================================

    # ROGUE

    # ============================================================



    if ability_key == "sneak_attack":



        if (

            target is None

            or target.hp <= 0

        ):

            return False



        player.resource -= cost



        vanish = (

            "vanish"

            in player.status_effects

        )



        if turn == 1 or vanish:

            multiplier = 3.0

        else:

            multiplier = 1.5



        multiplier += (

            0.20

            * player.weapon_tier

        )



        if hit_success():



            damage = calc_damage(

                player.attack,

                target.defense,

                multiplier,

            )



            target.hp -= damage



            if vanish:



                add_log(

                    combat_log,

                    (

                        "You strike from "

                        "the shadows!"

                    ),

                )



            add_log(

                combat_log,

                (

                    "Sneak Attack hits the "

                    f"{target.name} for "

                    f"{damage} damage!"

                ),

            )



            if target.hp <= 0:



                check_enemy_defeat(

                    player,

                    target,

                    combat_log,

                )



        else:



            add_log(

                combat_log,

                "Sneak Attack misses!",

            )



        # CLI behavior: Vanish is consumed

        # by the next Sneak Attack attempt,

        # whether the attack hits or misses.

        if vanish:



            del player.status_effects[

                "vanish"

            ]



        return True



    if ability_key == "nimble_feet":



        player.resource -= cost

        player.dodge_bonus = 0.20



        add_log(

            combat_log,

            (

                "You become light on your "

                "feet. Dodge chance increased!"

            ),

        )



        return True



    if ability_key == "double_strike":



        if (

            target is None

            or target.hp <= 0

        ):

            return False



        player.resource -= cost



        total_damage = 0

        hits = 0



        for _ in range(2):



            if target.hp <= 0:

                break



            if hit_success():



                multiplier = (

                    1.0

                    + (

                        0.20

                        * player.weapon_tier

                    )

                )



                damage = calc_damage(

                    player.attack,

                    target.defense,

                    multiplier,

                )



                target.hp -= damage



                total_damage += damage

                hits += 1



                add_log(

                    combat_log,

                    (

                        "Double Strike hits "

                        f"the {target.name} "

                        f"for {damage} damage!"

                    ),

                )



            else:



                add_log(

                    combat_log,

                    (

                        "One of your "

                        "strikes misses!"

                    ),

                )



        if target.hp <= 0:



            check_enemy_defeat(

                player,

                target,

                combat_log,

            )



        if hits:



            add_log(

                combat_log,

                (

                    "Double Strike dealt "

                    f"{total_damage} "

                    "total damage."

                ),

            )



        set_cooldown(

            player,

            ability_key,

        )



        return True



    if ability_key == "vanish":



        player.resource -= cost



        player.status_effects[

            "vanish"

        ] = {

            "evade_next": True,

            "sneak_empowered": True,

        }



        add_log(

            combat_log,

            (

                "You vanish into "

                "the shadows!"

            ),

        )



        add_log(

            combat_log,

            (

                "The next enemy attack "

                "will miss."

            ),

        )



        set_cooldown(

            player,

            ability_key,

        )



        return True



    if ability_key == "poison_blade":



        if (

            target is None

            or target.hp <= 0

        ):

            return False



        player.resource -= cost



        if hit_success():



            multiplier = (

                1.0

                + (

                    0.20

                    * player.weapon_tier

                )

            )



            damage = calc_damage(

                player.attack,

                target.defense,

                multiplier,

            )



            target.hp -= damage



            add_log(

                combat_log,

                (

                    "Poison Blade hits the "

                    f"{target.name} for "

                    f"{damage} damage!"

                ),

            )



            if target.hp <= 0:



                check_enemy_defeat(

                    player,

                    target,

                    combat_log,

                )



            else:



                apply_poison(

                    player,

                    target,

                    combat_log,

                )



        else:



            add_log(

                combat_log,

                "Poison Blade misses!",

            )



        set_cooldown(

            player,

            ability_key,

        )



        return True



    add_log(

        combat_log,

        (

            "That ability has not "

            "been implemented."

        ),

    )



    return False





# ================================================================

# ABILITY OVERLAY

# ================================================================



def ability_overlay(

    screen,

    clock,

    player,

    font,

    small_font,

):

    """

    Display available active abilities.



    Returns an ability key, "back", or "quit".

    """



    abilities = (

        available_abilities(

            player

        )

    )



    if not abilities:

        return "none"



    screen_width, screen_height = (

        screen.get_size()

    )



    panel_width = 760

    panel_height = min(

        580,

        screen_height - 60,

    )



    panel_x = (

        screen_width - panel_width

    ) // 2



    panel_y = (

        screen_height - panel_height

    ) // 2



    buttons = []



    start_y = panel_y + 125



    for index, (

        ability_key,

        ability,

    ) in enumerate(abilities):



        y = (

            start_y

            + index * 90

        )



        button = Button(

            ability["name"].upper(),

            panel_x + 40,

            y,

            300,

            48,

            small_font,

        )



        buttons.append(

            (

                ability_key,

                ability,

                button,

            )

        )



    back_button = Button(

        "BACK",

        panel_x + 40,

        panel_y + panel_height - 60,

        180,

        42,

        small_font,

    )



    # Preserve the combat frame so the translucent overlay does not
    # accumulate and progressively darken the screen each frame.
    background = screen.copy()

    while True:

        screen.blit(
            background,
            (0, 0),
        )

        for event in pygame.event.get():



            if event.type == pygame.QUIT:

                return "quit"



            if event.type == pygame.KEYDOWN:



                if event.key == pygame.K_ESCAPE:

                    return "back"



            if back_button.clicked(event):

                return "back"



            for (

                ability_key,

                _,

                button,

            ) in buttons:



                if button.clicked(event):

                    return ability_key



        # --------------------------------------------------------

        # DARKEN EXISTING SCREEN

        # --------------------------------------------------------



        shade = pygame.Surface(

            (

                screen_width,

                screen_height,

            ),

            pygame.SRCALPHA,

        )



        shade.fill(

            (0, 0, 0, 180)

        )



        screen.blit(

            shade,

            (0, 0),

        )



        # --------------------------------------------------------

        # PANEL

        # --------------------------------------------------------



        panel_rect = pygame.Rect(

            panel_x,

            panel_y,

            panel_width,

            panel_height,

        )



        pygame.draw.rect(

            screen,

            OVERLAY,

            panel_rect,

        )



        pygame.draw.rect(

            screen,

            GOLD,

            panel_rect,

            4,

        )



        draw_centered_text(

            screen,

            (

                f"{player.role.upper()} "

                "ABILITIES"

            ),

            font,

            GOLD,

            screen_width // 2,

            panel_y + 35,

        )



        draw_centered_text(

            screen,

            (

                f"{player.resource_type}: "

                f"{player.resource}/"

                f"{player.max_resource}"

            ),

            small_font,

            WHITE,

            screen_width // 2,

            panel_y + 72,

        )



        # --------------------------------------------------------

        # ABILITY ROWS

        # --------------------------------------------------------



        for (

            ability_key,

            ability,

            button,

        ) in buttons:



            button.draw(screen)



            cooldown = (

                player.cooldowns.get(

                    ability_key,

                    0,

                )

            )



            status_x = (

                button.rect.right + 20

            )



            status_y = (

                button.rect.y + 3

            )



            cost_text = (

                f"Cost: {ability['cost']} "

                f"{player.resource_type}"

            )



            cost_surface = (

                small_font.render(

                    cost_text,

                    True,

                    WHITE,

                )

            )



            screen.blit(

                cost_surface,

                (

                    status_x,

                    status_y,

                ),

            )



            if cooldown > 0:



                cooldown_surface = (

                    small_font.render(

                        (

                            "Cooldown: "

                            f"{cooldown}"

                        ),

                        True,

                        RED,

                    )

                )



                screen.blit(

                    cooldown_surface,

                    (

                        status_x,

                        status_y + 22,

                    ),

                )



            description_lines = wrap_text(

                ability["description"],

                small_font,

                660,

            )



            description_y = (

                button.rect.bottom + 5

            )



            for line in description_lines[:2]:



                description_surface = (

                    small_font.render(

                        line,

                        True,

                        MUTED,

                    )

                )



                screen.blit(

                    description_surface,

                    (

                        panel_x + 45,

                        description_y,

                    ),

                )



                description_y += 18



        back_button.draw(screen)



        pygame.display.flip()

        clock.tick(60)





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



    while True:



        # ========================================================

        # RESULT CHECKS

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

            # CLICK ENEMY TO TARGET

            # ----------------------------------------------------



            if (

                event.type

                == pygame.MOUSEBUTTONDOWN

                and event.button == 1

            ):



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



                        finish_round(

                            player,

                            enemies,

                            combat_log,

                        )



                        turn += 1



            # ----------------------------------------------------

            # ABILITIES

            # ----------------------------------------------------



            if ability_button.clicked(event):



                ability_key = (

                    ability_overlay(

                        screen,

                        clock,

                        player,

                        font,

                        small_font,

                    )

                )



                if ability_key == "quit":



                    return {

                        "outcome": "quit",

                        "enemies": enemies,

                    }



                if ability_key == "none":



                    add_log(

                        combat_log,

                        (

                            "You have no "

                            "abilities available."

                        ),

                    )



                elif ability_key != "back":



                    target = None



                    if selected_index is not None:



                        target = enemies[

                            selected_index

                        ]



                    acted = use_ability(

                        player,

                        ability_key,

                        target,

                        turn,

                        combat_log,

                    )



                    if acted:



                        finish_round(

                            player,

                            enemies,

                            combat_log,

                        )



                        turn += 1



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



                    finish_round(

                        player,

                        enemies,

                        combat_log,

                    )



                    turn += 1



            # ----------------------------------------------------

            # RUN

            # ----------------------------------------------------



            if run_button.clicked(event):



                if random.random() < 0.5:



                    return {

                        "outcome": "fled",

                        "enemies": enemies,

                    }



                add_log(

                    combat_log,

                    "You failed to run!",

                )



                finish_round(

                    player,

                    enemies,

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

        # DRAW

        # ========================================================



        screen.fill(BACKGROUND)



        # --------------------------------------------------------

        # HEADER

        # --------------------------------------------------------



        draw_centered_text(

            screen,

            f"COMBAT — TURN {turn}",

            font,

            GOLD,

            screen_width // 2,

            35,

        )



        # --------------------------------------------------------

        # PLAYER PANEL

        # --------------------------------------------------------



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

                player_panel.y + 10,

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



        if player.resource_type:



            resource_text = (

                small_font.render(

                    (

                        f"{player.resource_type}: "

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

                    player_panel.right - 300,

                    player_panel.y + 12,

                ),

            )



            draw_bar(

                screen,

                player_panel.right - 300,

                player_panel.y + 42,

                250,

                15,

                player.resource,

                player.max_resource,

                YELLOW,

            )



        if (

            "vanish"

            in player.status_effects

        ):



            vanished_text = (

                small_font.render(

                    "VANISHED",

                    True,

                    GOLD,

                )

            )



            screen.blit(

                vanished_text,

                (

                    player_panel.centerx - 40,

                    player_panel.y + 25,

                ),

            )



        # --------------------------------------------------------

        # ENEMIES

        # --------------------------------------------------------



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



            draw_enemy_card(

                screen,

                enemy,

                card_rect,

                small_font,

                selected=(

                    index

                    == selected_index

                    and enemy.hp > 0

                ),

            )



        # --------------------------------------------------------

        # COMBAT LOG

        # --------------------------------------------------------



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



        # --------------------------------------------------------

        # ACTION BUTTONS

        # --------------------------------------------------------



        attack_button.draw(screen)

        ability_button.draw(screen)

        item_button.draw(screen)

        run_button.draw(screen)

        target_button.draw(screen)



        # --------------------------------------------------------

        # TARGET FOOTER

        # --------------------------------------------------------



        selected_enemy = None



        if selected_index is not None:



            selected_enemy = enemies[

                selected_index

            ]



        if selected_enemy:



            target_text = (

                "Target: "

                f"{selected_enemy.name.title()}"

            )



        else:



            target_text = "Target: None"



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