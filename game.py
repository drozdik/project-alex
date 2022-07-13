from random import randint

from gameui import Screen


def calc_damage(min_damage, max_damage):
    damage = randint(min_damage, max_damage)
    luck = roll_dice(20)
    if luck == 10:
        damage = damage * 2
        print("critical damage")
    if luck == 1:
        damage = min_damage
        print("critical miss")
    return damage


def roll_dice(sides):
    result = randint(1, sides)
    return result


def calc_heal():
    health_points = roll_dice(8)
    luck = roll_dice(10)
    if luck == 10:
        print("God loves you")
        health_points = health_points * 2
    return health_points


min_damage = 1
max_damage = 15
turn = 1
# hero_max_hp = 20
# hero_hp = hero_max_hp
hero_armor = 10
# monster_packs = [[30, 20], [30, 30]]
# active_monster_pack_index = 0
# active_monster_pack = monster_packs[active_monster_pack_index]

game_state = {
    # "min_damage": 1,
    # "max_damage": 15,
    # "turn": 1,
    "hero_max_hp": 20,
    "hero_hp": 20,
    # "hero_armor": 10,
    "monster_packs": [[30, 20], [30, 30]],
    "active_monster_pack_index": 0,
    "active_monster_pack": None,
}

game_state["active_monster_pack"] = game_state["monster_packs"][game_state["active_monster_pack_index"]]


def switch_to_next_monster_pack():
    game_state["active_monster_pack_index"] += 1
    game_state["active_monster_pack"] = game_state["monster_packs"][game_state["active_monster_pack_index"]]


def pack_is_dead():
    for monster_hp in game_state["active_monster_pack"]:
        if monster_hp > 0:
            return False
    return True


def hero_is_dead():
    return game_state["hero_hp"] <= 0


def all_packs_are_dead():
    return game_state["active_monster_pack_index"] == len(game_state["monster_packs"])


def use_heal():
    health_points = calc_heal()
    print("Healing", health_points)
    game_state["hero_hp"] = game_state["hero_hp"] + health_points
    if game_state["hero_hp"] >= game_state["hero_max_hp"]:
        game_state["hero_hp"] = game_state["hero_max_hp"]
        print("You have max HP")


def attack_first_alive_monster():
    damage = calc_damage(min_damage, max_damage)
    print("You hit ", damage, "damage")
    print("Current monster pack hp is ", game_state["active_monster_pack"])
    for index, monster_hp in enumerate(game_state["active_monster_pack"]):
        if monster_hp > 0:
            game_state["active_monster_pack"][index] = monster_hp - damage
            print("After hit", game_state["active_monster_pack"])
            break


def attack_hero():
    damage = calc_damage(1, 15)
    # print(monster_hp, "Monster hit ", damage, "damage")
    if damage <= hero_armor:
        print("All damage absorbed")
    else:
        game_state["hero_hp"] = game_state["hero_hp"] - (damage - hero_armor)
    print("Current Hero hp is ", game_state["hero_hp"])


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
    if pack_is_dead() and not all_packs_are_dead():
        switch_to_next_monster_pack()


def monster_pack_attack():
    for monster_hp in game_state["active_monster_pack"]:
        if monster_hp > 0 and not hero_is_dead():
            attack_hero()


screen = Screen(hero_attack, monster_pack_attack, game_state)
