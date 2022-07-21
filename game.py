from random import randint

from gameui import Screen


def calc_damage(min_damage, max_damage):
    damage = randint(min_damage, max_damage)
    luck = roll_dice(20)
    if luck == 10:
        damage = damage * 2
        game_state.get("game_log").append("Critical damage")
    if luck == 1:
        damage = min_damage
        game_state.get("game_log").append("Critical miss")
    return damage


def roll_dice(sides):
    result = randint(1, sides)
    return result


def calc_heal():
    health_points = roll_dice(8)
    luck = roll_dice(10)
    if luck == 10:
        game_state.get("game_log").append("God loves you")
        health_points = health_points * 2
    return health_points

def new_skeleton():
    return {
    "max_hp" : 30,
    "armor" : 2,
    "hp" : 30,
    "name" : "Skeleton",
    "class" : "Skeleton",
    "min_damage" : 3,
    "max_damage" : 15
    }

def create_monster_packs():
    return[
        [new_skeleton(),new_skeleton()],
        [new_skeleton(),new_skeleton_mage()],
        [new_skeleton(),new_skeleton_lich()]
    ]

def new_skeleton_mage():
    return {
    "max_hp" : 20,
    "hp" : 20,
    "armor" : 2,
    "name" : "Skeleton-mage",
    "class" : "Skeleton-mage",
    "min_damage" : 5,
    "max_damage" : 14
    }

def new_skeleton_lich():
    return{
    "max_hp" : 60,
    "hp" : 60,
    "armor" : 3,
    "name": "Skeleton-Lich",
    "class": "Skeleton-Lich",
    "min_damage" : 10,
    "max_damage" : 20
    }

turn = 1

game_state = {
    # "min_damage": 1,
    # "max_damage": 15,
    # "turn": 1,
    "hero_max_hp": 20,
    "hero_hp": 20,
    "hero_min_damage": 1,
    "hero_max_damage": 15,
    "hero_armor": 10,
    # "hero_armor": 10,
    "monster_packs": create_monster_packs(),
    "active_monster_pack_index": 0,
    "active_monster_pack": None,
    "game_log": [],
    "hero_dead": False,
    "monsters_dead": False
}

game_state["active_monster_pack"] = game_state["monster_packs"][game_state["active_monster_pack_index"]]


def switch_to_next_monster_pack():
    game_state["active_monster_pack_index"] += 1
    game_state["active_monster_pack"] = game_state["monster_packs"][game_state["active_monster_pack_index"]]
    game_state.get("game_log").append("\nNew monsters arrived\n")


def pack_is_dead():
    for monster in game_state["active_monster_pack"]:
        if monster["hp"] > 0:
            return False
    return True


def hero_is_dead():
    return game_state["hero_hp"] <= 0


def all_packs_are_dead():
    return game_state["active_monster_pack_index"] == len(game_state["monster_packs"])


def last_pack_active():
    return game_state["active_monster_pack_index"] == len(game_state["monster_packs"]) - 1


def use_heal():
    health_points = calc_heal()
    game_state.get("game_log").append(f"Healing {health_points}")
    game_state["hero_hp"] = game_state["hero_hp"] + health_points
    if game_state["hero_hp"] >= game_state["hero_max_hp"]:
        game_state["hero_hp"] = game_state["hero_max_hp"]
        game_state.get("game_log").append("Healed to max HP")

def use_precision_strike():
    print('Implement me, pleas! Doing regular strike for now')
    attack_first_alive_monster() # hint: create new!
    after_hero_turn()

def use_aoe_strike():
    print('Implement me, pleas! Doing regular strike for now')
    attack_first_alive_monster()
    after_hero_turn()



def attack_first_alive_monster():
    for monster in game_state["active_monster_pack"]:
        if monster["hp"] > 0:
            hero_attacks_monster(monster)
            break


def monster_attacks_hero(monster):

    damage = calc_damage(monster['min_damage'],monster ['max_damage'])
    if damage <= game_state["hero_armor"]:
        game_state.get("game_log").append(f"Monster hit {damage} damage, all absorbed")
    else:
        effective_damage = (damage - game_state["hero_armor"])
        game_state["hero_hp"] = game_state["hero_hp"] - effective_damage
        game_state.get("game_log").append(f"Monster hit {damage} damage, {effective_damage} passes armor")

def hero_attacks_monster(monster):
    damage = calc_damage(game_state["hero_min_damage"],game_state["hero_max_damage"])
    if damage <= monster["armor"]:
        game_state.get("game_log").append(f"Hero hit {damage} damage, all absorbed")
    else:
        effective_damage = (damage - monster["armor"])
        monster["hp"] = monster["hp"] - effective_damage
        game_state.get("game_log").append(f"Hero hit {damage} damage, {effective_damage} passes armor")

def ask_for_hero_action():
    return input("Press any key or Q to end the programm. Press H to heal and hit")


def ask_for_monster_turn():
    return input("Press any key for monster turn ")


def hero_turn():
    return turn % 2 == 1


def hero_attack(): # regular attack
    attack_first_alive_monster()
    after_hero_turn()

def after_hero_turn():
    if pack_is_dead():
        if last_pack_active():
            game_state["monsters_dead"] = True
            return
        switch_to_next_monster_pack()
    monster_pack_attack()


def monster_pack_attack():
    for monster in game_state["active_monster_pack"]:
        if monster["hp"] > 0:
            monster_attacks_hero(monster)
            if hero_is_dead():
                game_state["hero_dead"] = True
                return


def game_restart():
    game_state.update({
        # "min_damage": 1,
        # "max_damage": 15,
        # "turn": 1,
        "hero_max_hp": 20,
        "hero_hp": 20,
        # "hero_armor": 10,
        "monster_packs": game_state(),
        "active_monster_pack_index": 0,
        "active_monster_pack": None,
        "game_log": [],
        "hero_dead": False,
        "monsters_dead": False
    })
    game_state["active_monster_pack"] = game_state["monster_packs"][game_state["active_monster_pack_index"]]


screen = Screen(hero_attack, use_heal, game_state, game_restart, use_precision_strike, use_aoe_strike)
