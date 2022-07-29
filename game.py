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
    health_points = randint(20, 40)
    luck = roll_dice(10)
    if luck == 10:
        game_state.get("game_log").append("God loves you")
        health_points = health_points * 2
    return health_points       

def new_game_state():
    state = {
    "hero_stuned_rounds" : 0,
    "hero_max_hp": 100,
    "hero_hp": 100,
    "hero_min_damage": 3,
    "hero_max_damage": 20,
    "hero_base_max_damage": 20,
    "hero_armor": 10,
    "hero_base_armor": 10,
    "hero_in_block" : False,
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
        if(mage_chance < 20): 
            pack[1] = new_skeleton_mage()
            mage_chance = randint(1,100)
            if(mage_chance < 10):
                pack[0] = new_skeleton_mage()
        lich_chance = randint(1,100)
        if(lich_chance < (0 + i*10)):
            pack = [new_skeleton(), new_skeleton_lich()]
            packs.append(pack)
            break 
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

def add_healing_potions(count):
     game_state["healing_potions"] = game_state["healing_potions"] + count

def fortune_rest():
    rest = randint(1 ,100)
    if rest <= 60:
        add_healing_potions(1)
        use_heal()
        game_state.get("game_log").append("Fortune:60% luck")
    if rest >= 80:
        add_healing_potions(2)
        use_heal()
        use_heal()
        game_state.get("game_log").append("Fortune:20% luck")
    if rest >= 70 and rest <= 75:
        game_state["hero_hp"] = game_state["hero_max_hp"]
        game_state["hero_max_damage"] = game_state["hero_base_max_damage"]
        game_state.get("game_log").append("Fortune:5% luck")

def power_increase():
    hero_power_icrease = randint(1, 100)
    if hero_power_icrease <= 50:
        game_state["hero_base_max_damage"] = game_state["hero_base_max_damage"] + 1
        game_state["hero_min_damage"] = game_state["hero_min_damage"] + 1
    if hero_power_icrease >= 95:
        game_state["hero_base_max_damage"] = game_state["hero_base_max_damage"] + 2
        game_state["hero_min_damage"] = game_state["hero_min_damage"] + 2

def hero_rest():
    game_state["hero_armor"] = game_state["hero_base_armor"]
    power_increase()
    fortune_rest()

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

def damage_restore():
    if game_state["hero_max_damage"] >= game_state["hero_base_max_damage"]:
        game_state["hero_max_damage"] = game_state["hero_base_max_damage"]
        game_state.get("game_log").append("Restored max damage")
def armor_restore():
    if game_state["hero_armor"] >= game_state["hero_base_armor"]:
        game_state["hero_armor"] = game_state["hero_base_armor"]
        game_state.get("game_log").append("Restored armor")

def max_hp_heal():
    if game_state["hero_hp"] >= game_state["hero_max_hp"]:
        game_state["hero_hp"] = game_state["hero_max_hp"]
        game_state.get("game_log").append("Healed to max HP")
def hero_restore():
    health_points = calc_heal()
    game_state.get("game_log").append(f"Healing {health_points}")
    game_state["hero_hp"] = game_state["hero_hp"] + health_points
    game_state["hero_max_damage"] = game_state["hero_max_damage"] + 4
    game_state["hero_armor"] = game_state["hero_armor"] * 2


def use_heal():
    if(game_state["healing_potions"] <= 0):
        raise Exception("No healing potions")
    game_state['healing_potions'] -= 1
    if hero_is_stunned():
        game_state["hero_stuned_rounds"] = 0
        game_state["hero_armor"] = game_state["hero_armor"] * 2
        game_state["hero_max_damage"] = game_state["hero_max_damage"] * 2
    hero_restore()
    damage_restore()
    max_hp_heal()
    armor_restore()

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

def use_block():
    game_state["hero_in_block"] = True
    game_state["hero_armor"] = game_state["hero_armor"] + 15   
    after_hero_turn()

def attack_first_alive_monster():
    monster = get_first_alive_monster()
    hero_attacks_monster(monster)

def get_first_alive_monster():
    for monster in game_state["active_monster_pack"]:
        if monster["hp"] > 0:
            return monster

def lich_stun():
    if not hero_is_stunned():
        game_state["hero_armor"] = game_state["hero_armor"] / 2
        game_state["hero_max_damage"] = int(game_state["hero_max_damage"] / 2)
    game_state["hero_stuned_rounds"] = game_state["hero_stuned_rounds"] + 3


def hero_is_stunned():
    return game_state["hero_stuned_rounds"] > 0

def monsters_turn_end():
    if hero_is_stunned():
        game_state["hero_stuned_rounds"] = game_state["hero_stuned_rounds"] - 1
        if not hero_is_stunned():
            print("restore damage and armor")
            game_state["hero_armor"] = game_state["hero_armor"] * 2
            game_state["hero_max_damage"] = game_state["hero_max_damage"] * 2
    if game_state["hero_in_block"]:
        game_state["hero_in_block"] = False
        game_state["hero_armor"] = game_state["hero_base_armor"]

def monster_attacks_hero(monster):
    damage = calc_damage(monster['min_damage'],monster ['max_damage'])
    effective_damage = damage - game_state["hero_armor"]
    if effective_damage > 0:
        game_state["hero_hp"] = game_state["hero_hp"] - effective_damage
    append_damage_log("Monster", damage, effective_damage)
    lich_will_stun = randint(1,10) <= 2   
    if lich_will_stun and monster["class"] == "Skeleton-Lich":    
        lich_stun()
    if damage > game_state["hero_armor"] and monster["class"] == "Skeleton":
        game_state["hero_armor"]= game_state["hero_armor"] - 2
    if damage > game_state["hero_armor"] and monster["class"] == "Skeleton-mage":
        game_state["hero_max_damage"] = game_state["hero_max_damage"] - 5
        if game_state["hero_max_damage"] <= game_state["hero_min_damage"]:
            game_state["hero_max_damage"] = game_state["hero_min_damage"]  

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


def hero_attack(): 
    attack_first_alive_monster()
    after_hero_turn()

def after_hero_turn():
    if pack_is_dead():
        hero_rest()
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
    monsters_turn_end()            

def game_restart():
    game_state.update(new_game_state())

screen = Screen(hero_attack, use_heal, game_state, game_restart, use_precision_strike, use_aoe_strike, use_combo_strike, use_block)
