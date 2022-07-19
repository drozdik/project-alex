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
    "hp" : 30,
    "name" : "Skeleton",
    }

def new_skeleton_mage():
    return {
    "max_hp" : 35,
    "hp" : 35,
    "name" : "Skeleton-mage",
    }

min_damage = 1
max_damage = 15
turn = 1
# hero_max_hp = 20
# hero_hp = hero_max_hp
hero_armor = 10
# monster_packs = [[30, 20], [30, 30]]
# active_monster_pack_index = 0
# active_monster_pack = monster_packs[active_monster_pack_index]
skeleton1 = {
    "max_hp" : 30,
    "hp" : 30,
    "name" : "Skeleton",
    "min_damage" : 3,
    "max_damage" : 15
}
skeleton2 = {
    "max_hp" : 30,
    "hp" : 30,
    "name" : "Skeleton",
    "min_damage" : 3,
    "max_damage" : 15
}
skeleton3 = {
    "max_hp" : 30,
    "hp" : 30,
    "name" : "Skeleton",
    "min_damage" : 3,
    "max_damage" : 15
}
skeleton_mage = {
    "max_hp" : 20,
    "hp" : 20,
    "name" : "Skeleton-mage",
    "min_damage" : 5,
    "max_damage" : 14

}
skeleton_lich ={
    "max_hp" : 60,
    "hp" : 60,
    "name": "Skeleton-Lich",
    "min_damage" : 10,
    "max_damage" : 20
}


game_state = {
    # "min_damage": 1,
    # "max_damage": 15,
    # "turn": 1,
    "hero_max_hp": 20,
    "hero_hp": 20,
    # "hero_armor": 10,
    "monster_packs": [[skeleton_lich, skeleton_mage], [skeleton2, skeleton3],[skeleton_lich]],
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


def attack_first_alive_monster():
    damage = calc_damage(min_damage, max_damage)
    hero_damage_log = f"You hit {damage} damage"
    game_state.get("game_log").append(hero_damage_log)
    for monster in game_state["active_monster_pack"]:
        if monster["hp"] > 0:
            monster["hp"] = monster["hp"] - damage
            break


def attack_hero(monster):

    damage = calc_damage(monster['min_damage'],monster ['max_damage'])
    if damage <= hero_armor:
        game_state.get("game_log").append(f"Monster hit {damage} damage, all absorbed")
    else:
        effective_damage = (damage - hero_armor)
        game_state["hero_hp"] = game_state["hero_hp"] - effective_damage
        game_state.get("game_log").append(f"Monster hit {damage} damage, {effective_damage} passes armor")


def ask_for_hero_action():
    return input("Press any key or Q to end the programm. Press H to heal and hit")


def ask_for_monster_turn():
    return input("Press any key for monster turn ")


def hero_turn():
    return turn % 2 == 1


# start game
# hero attack # hero heal
# monster attack
# quit game

# while True:
#     if hero_turn():
#         user_input = ask_for_hero_action()
#         if user_input == "Q":
#             break
#         if user_input == "H":
#             use_heal()
#         attack_first_alive_monster()
#
#     else:  # monster turn
#         user_input = ask_for_monster_turn()
#         for monster_hp in active_monster_pack:
#             if monster_hp > 0 and not hero_is_dead():
#                 attack_hero()
#
#     if pack_is_dead():
#         switch_to_next_monster_pack()
#
#     if all_packs_are_dead():
#         print("All packs is dead")
#         break
#     if hero_is_dead():
#         print("Hero is dead")
#         break
#     turn = turn + 1
#
# print("Game over")

def hero_attack():
    attack_first_alive_monster()
    if pack_is_dead():
        if last_pack_active():
            game_state["monsters_dead"] = True
            return
        switch_to_next_monster_pack()
    monster_pack_attack()


def monster_pack_attack():
    for monster in game_state["active_monster_pack"]:
        if monster["hp"] > 0:
            attack_hero(monster)
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
        "monster_packs": [[skeleton1, skeleton_mage], [skeleton2, skeleton3],[skeleton_lich]],
        "active_monster_pack_index": 0,
        "active_monster_pack": None,
        "game_log": [],
        "hero_dead": False,
        "monsters_dead": False
    })
    game_state["active_monster_pack"] = game_state["monster_packs"][game_state["active_monster_pack_index"]]


screen = Screen(hero_attack, use_heal, game_state, game_restart)
