from random import randint

from controller import Controller
from gameui import Screen
from model import Model

screen = None

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
    health_points = randint(20, 40)
    luck = roll_dice(10)
    if luck == 10:
        game_state.get("game_log").append("God loves you")
        health_points = health_points * 2
    return health_points       

def new_game_state():
    state = {
    # "min_damage": 1,
    # "max_damage": 15,
    # "turn": 1,
    "hero_max_hp": 100,
    "hero_hp": 100,
    "hero_min_damage": 2,
    "hero_max_damage": 20,
    "hero_base_max_damage": 20,
    "hero_armor": 1,
    "hero_base_armor": 1,
    "healing_potions": 5,
    "monster_packs": create_monster_packs(),
    "active_monster_pack_index": 0,
    "active_monster_pack": None,
    "game_log": [],
    "hero_dead": False,
    "monsters_dead": False
    }
    state["active_monster_pack"] = state["monster_packs"][state["active_monster_pack_index"]]
    return state

def new_skeleton():
    return {
    "max_hp" : 30,
    "armor" : 3,
    "hp" : 30,
    "name" : "Skeleton",
    "class" : "Skeleton",
    "min_damage" : 3,
    "max_damage" : 15
    }

def create_monster_packs():
    packs = []
    for i in range(10):
        pack = [new_skeleton(), new_skeleton()]
        mage_chance = randint(1,100)
        if(mage_chance < 20): # 20% of times it's True
            pack[1] = new_skeleton_mage()
            mage_chance = randint(1,100)
            if(mage_chance < 10):
                pack[0] = new_skeleton_mage()
        lich_chance = randint(1,100)
        if(lich_chance < (0 + i*10)): # each pack lich chance increased by 5%
            pack = [new_skeleton(), new_skeleton_lich()]
            packs.append(pack)
            break # lich is always end of dungeon, so no more packs needed
        packs.append(pack)
    return packs

def new_skeleton_mage():
    return {
    "max_hp" : 10,
    "hp" : 10,
    "armor" : 2,
    "name" : "Skeleton-mage",
    "class" : "Skeleton-mage",
    "min_damage" : 10,
    "max_damage" : 14
    }

def new_skeleton_lich():
    return{
    "max_hp" : 60,
    "hp" : 60,
    "armor" : 18,
    "name": "Skeleton-Lich",
    "class": "Skeleton-Lich",
    "min_damage" : 10,
    "max_damage" : 20
    }

turn = 1

game_state = new_game_state()

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
    prev_state = game_state.copy()
    if(game_state["healing_potions"] <= 0):
        raise Exception("No healing potions")
    game_state['healing_potions'] -= 1
    health_points = calc_heal()
    game_state.get("game_log").append(f"Healing {health_points}")
    game_state["hero_hp"] = game_state["hero_hp"] + health_points
    game_state["hero_max_damage"] = game_state["hero_max_damage"] + 4
    if game_state["hero_max_damage"] >= game_state["hero_base_max_damage"]:
        game_state["hero_max_damage"] = game_state["hero_base_max_damage"]
        game_state.get("game_log").append("Restored max damage")
    
    if game_state["hero_hp"] >= game_state["hero_max_hp"]:
        game_state["hero_hp"] = game_state["hero_max_hp"]
        game_state.get("game_log").append("Healed to max HP")
    screen.on_model_update(Model(prev_state, game_state))
    

def use_precision_strike():
    monster = get_first_alive_monster()
    damage = calc_damage(game_state["hero_min_damage"],game_state["hero_max_damage"]) + 5   
    monster["hp"] = monster["hp"] - damage
    game_state["hero_hp"] = game_state["hero_hp"] - 1
    append_damage_log("Hero", damage, damage)
    after_hero_turn()

def use_aoe_strike():
    damage = calc_damage(game_state["hero_min_damage"], game_state["hero_max_damage"]) - 1
    for monster in game_state["active_monster_pack"]:
        effective_damage = damage - monster["armor"]
        if effective_damage > 0:
            monster["hp"] = monster["hp"] - effective_damage
        append_damage_log("Hero", damage, effective_damage)
    after_hero_turn()

def use_combo_strike():
    monster = get_first_alive_monster()
    hero_attacks_monster(monster)
    hero_attacks_monster(monster)
    game_state["hero_armor"] = game_state["hero_armor"] - 5
    after_hero_turn()

def attack_first_alive_monster():
    monster = get_first_alive_monster()
    hero_attacks_monster(monster)

def get_first_alive_monster():
    for monster in game_state["active_monster_pack"]:
        if monster["hp"] > 0:
            return monster



def monster_attacks_hero(monster):
    prev_state = game_state.copy()
    damage = calc_damage(monster['min_damage'],monster ['max_damage'])
    effective_damage = damage - game_state["hero_armor"]
    if effective_damage > 0:
        game_state["hero_hp"] = game_state["hero_hp"] - effective_damage
    append_damage_log("Monster", damage, effective_damage)
    #hack1, restore armor after combo strike
    game_state["hero_armor"] = game_state["hero_base_armor"]
    if damage > game_state["hero_armor"] and monster["class"] == "Skeleton":
        game_state["hero_armor"]= game_state["hero_armor"] - 2
    if damage > game_state["hero_armor"] and monster["class"] == "Skeleton-mage":
        game_state["hero_max_damage"] = game_state["hero_max_damage"] - 5
        if game_state["hero_max_damage"] <= game_state["hero_min_damage"]:
            game_state["hero_max_damage"] = game_state["hero_min_damage"]
    screen.on_model_update(Model(prev_state, game_state.copy()))

def hero_attacks_monster(monster):
    damage = calc_damage(game_state["hero_min_damage"],game_state["hero_max_damage"])
    effective_damage = damage - monster["armor"]
    if effective_damage > 0:
        monster["hp"] = monster["hp"] - effective_damage
    append_damage_log("Hero", damage, effective_damage)

def append_damage_log(attacker, damage, effective_damage):
    if(effective_damage <= 0):
        game_state.get("game_log").append(f"{attacker} hit {damage} damage, all absorbed")
    else:
        game_state.get("game_log").append(f"{attacker} hit {damage} damage, {effective_damage} passes armor")


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
    game_state.update(new_game_state())



controller = Controller(use_heal)
screen = Screen(hero_attack, use_heal, game_state, game_restart, use_precision_strike, use_aoe_strike, use_combo_strike, controller)
screen.display()

# screen create with game as a controller
# game.subscribe(screen)
# screen.display()
