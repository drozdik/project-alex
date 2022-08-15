import threading
import time
from queue import Queue
from random import randint
from typing import List
from monsters import Monster, Skeleton, SkeletonLich, SkeletonMage
from gameui import Screen

screen = None
screenHolder = {"screen":screen}


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
    "active_monster_pack": [Monster(screen),Monster(screen)],
    "game_log": [],
    "hero_dead": False,
    "monsters_dead": False
    }
    state["active_monster_pack"] = state["monster_packs"][state["active_monster_pack_index"]]
    return state

def new_skeleton():
    return Skeleton(screenHolder)

def create_monster_packs()-> List[Monster]:
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
    return SkeletonMage(screen)

def new_skeleton_lich():
    return SkeletonLich(screen)

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
    for monster in get_active_monster_pack():
        if monster.alive():
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

def use_heal_inside(screen: Screen):
    use_heal()
    screen.update_components()
    time.sleep(1)
    screen.clear_statuses()


def use_precision_strike_inside(screen: Screen):
    monster = get_first_alive_monster()
    damage = calc_damage(game_state["hero_min_damage"],game_state["hero_max_damage"]) + 5
    monster.hp = monster.hp - damage
    game_state["hero_hp"] = game_state["hero_hp"] - 1
    append_damage_log("Hero", damage, damage)
    after_hero_turn()
    screen.update_components()
    time.sleep(1)
    screen.clear_statuses()


def use_aoe_strike_inside(screen:Screen):
    damage = calc_damage(game_state["hero_min_damage"], game_state["hero_max_damage"]) - 1
    for monster in get_active_monster_pack():
        effective_damage = damage - monster.armor
        if effective_damage > 0:
            monster.hp = monster.hp - effective_damage
        append_damage_log("Hero", damage, effective_damage)
    after_hero_turn()
    screen.update_components()
    time.sleep(1)
    screen.clear_statuses()


def use_combo_strike_inside(screen:Screen):
    monster = get_first_alive_monster()
    hero_attacks_monster(monster)
    hero_attacks_monster(monster)
    game_state["hero_armor"] = game_state["hero_armor"] - 5
    after_hero_turn()
    screen.update_components()
    time.sleep(1)
    screen.clear_statuses()


def use_block_inside(screen:Screen):
    game_state["hero_in_block"] = True
    game_state["hero_armor"] = game_state["hero_armor"] + 15
    after_hero_turn()
    screen.update_components()
    time.sleep(1)
    screen.clear_statuses()


def attack_first_alive_monster():
    monster = get_first_alive_monster()
    hero_attacks_monster(monster)

def get_active_monster_pack()-> List[Monster]:
    return game_state["active_monster_pack"]

def get_first_alive_monster():
    for monster in get_active_monster_pack():
        if monster.alive():
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

def monster_attacks_hero(monster:Monster,screen:Screen = None):
    time.sleep(0.2)
    screen.show_monster_attacks(monster)
    print(f'outside screen is {screen}')
    monster.screen = screen
    damages = monster.deal_damage(calc_damage, game_state)
    append_damage_log("Monster", damages[0], damages[1])
    effective_damage = damages[1]
    screen.show_hero_hp_changed(min(0, 0 - effective_damage))

def hero_attacks_monster(monster:Monster):
    screen.show_hero_attacks() # view processing hero_attacked event
    damage = calc_damage(game_state["hero_min_damage"],game_state["hero_max_damage"])
    damages = monster.take_damage(damage)
    append_damage_log("Hero", damages[0], damages[1])
    effective_damage = damages[1]
    screen.show_monster_hp_changed(monster, 0-effective_damage) # view processing monster_hp_changed

def append_damage_log(attacker, damage, effective_damage):
    if(effective_damage <= 0):
        game_state.get("game_log").append(f"{attacker} hit {damage} damage, all absorbed")
    else:
        game_state.get("game_log").append(f"{attacker} hit {damage} damage, {effective_damage} passes armor")
    screen.show_updated_log()

def ask_for_hero_action():
    return input("Press any key or Q to end the programm. Press H to heal and hit")


def ask_for_monster_turn():
    return input("Press any key for monster turn ")


def hero_turn():
    return turn % 2 == 1

# let's make this method called from thread when it picks event from queue


def hero_attack_inside(screen: Screen):
    attack_first_alive_monster()
    # show that hero attacks
    after_hero_turn(screen)
    print("Updating hero statuses")
    # screen.update_components()
    print("Sleeping one sec")
    # time.sleep(1)
    print("Clearing statuses")
    # screen.clear_statuses()


def after_hero_turn(screen:Screen = None):
    if pack_is_dead():
        hero_rest()
        if last_pack_active():
            game_state["monsters_dead"] = True
            return
        switch_to_next_monster_pack()
    monster_pack_attack(screen)


def monster_pack_attack(screen:Screen = None):
    for monster in get_active_monster_pack():
        if monster.alive():
            monster_attacks_hero(monster, screen)
            if hero_is_dead():
                game_state["hero_dead"] = True
                return
    monsters_turn_end()

def game_restart():
    game_state.update(new_game_state())


queue = Queue()
screen = Screen(None, None, game_state, game_restart, None, None, None, None, queue)
screenHolder["screen"]=screen


def watch_queue(queue:Queue, hero_attack_inside, use_heal_inside, use_precision_strike_inside, use_aoe_strike_inside,
                use_combo_strike_inside,
                use_block_inside,
                screen:Screen):
    while True:
        if not queue.empty():
            event = queue.get()
            print(f"picked event {event}")
            if event == "hero_attack":
                hero_attack_inside(screen)
            elif event == "hero_heal":
                use_heal_inside(screen)
            elif event == "precision_strike":
                use_precision_strike_inside(screen)
            elif event == "aoe_strike":
                use_aoe_strike_inside(screen)
            elif event == "combo_strike":
                use_combo_strike_inside(screen)
            elif event == "block":
                use_block_inside(screen)



# start queue watcher thread here
queue_watcher = threading.Thread(target=watch_queue,
                                 args=[queue, hero_attack_inside, use_heal_inside, use_precision_strike_inside, use_aoe_strike_inside,
                                       use_combo_strike_inside,
                                       use_block_inside,
                                       screen])
queue_watcher.setDaemon(True)
queue_watcher.start()

screen.start()
