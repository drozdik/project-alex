import threading
import time
from queue import Queue
from random import randint
from typing import List

from game_events_listener import GameEventsListener
from monsters import Monster, Skeleton, SkeletonLich, SkeletonMage
from gameui import Screen

screen = None
screenHolder = {"screen": screen}
event_listener = GameEventsListener(screenHolder)

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
        "hero_stuned_rounds": 0,
        "hero_max_hp": 100,
        "hero_hp": 100,
        "hero_min_damage": 3,
        "hero_max_damage": 20,
        "hero_base_max_damage": 20,
        "hero_armor": 0,
        "hero_base_armor": 10,
        "hero_in_block": False,
        "healing_potions": 5,
        "monster_packs": create_monster_packs(),
        "active_monster_pack_index": 0,
        "active_monster_pack": [Monster(screenHolder, event_listener), Monster(screenHolder, event_listener)],
        "game_log": [],
        "hero_dead": False,
        "monsters_dead": False
    }
    state["active_monster_pack"] = state["monster_packs"][state["active_monster_pack_index"]]
    return state


def new_skeleton():
    return Skeleton(screenHolder, event_listener)


def create_monster_packs() -> List[Monster]:
    packs = []
    for i in range(3):
        pack = [new_skeleton(), new_skeleton()]
        mage_chance = randint(1, 100)
        if (mage_chance < 20):
            pack[1] = new_skeleton_mage()
            mage_chance = randint(1, 100)
            if (mage_chance < 10):
                pack[0] = new_skeleton_mage()
        lich_chance = randint(1, 100)
        if (lich_chance < (0 + i * 10)):
            pack = [new_skeleton(), new_skeleton_lich()]
            packs.append(pack)
            break
        packs.append(pack)
    return packs


def new_skeleton_mage():
    return SkeletonMage(screenHolder, event_listener)


def new_skeleton_lich():
    return SkeletonLich(screenHolder, event_listener)


turn = 1

game_state = new_game_state()

game_state["active_monster_pack"] = game_state["monster_packs"][game_state["active_monster_pack_index"]]


def switch_to_next_monster_pack():
    print('switching to next monster pack')
    game_state["active_monster_pack_index"] += 1
    game_state["active_monster_pack"] = game_state["monster_packs"][game_state["active_monster_pack_index"]]
    get_screen().show_new_monsters_pack()
    game_state.get("game_log").append("\nNew monsters arrived\n")


def add_healing_potions(count):
    game_state["healing_potions"] = game_state["healing_potions"] + count


def fortune_rest():
    rest = randint(1, 100)
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
        change_hero_armor(game_state["hero_base_armor"])
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


def change_hero_hp(hp_diff):
    if game_state["hero_hp"] + hp_diff > game_state["hero_max_hp"]:
        hp_diff = game_state["hero_max_hp"] - game_state["hero_hp"]
    game_state["hero_hp"] += hp_diff
    screenHolder["screen"].show_hero_hp_changed(hp_diff)


def use_heal():
    if (game_state["healing_potions"] <= 0):
        raise Exception("No healing potions")
    game_state['healing_potions'] -= 1
    get_screen().show_number_of_health_potions_changed(-1)
    change_hero_hp(calc_heal())
    # if hero_is_stunned():
    #     game_state["hero_stuned_rounds"] = 0
    #     double_hero_armor()
    #     game_state["hero_max_damage"] = game_state["hero_max_damage"] * 2
    # hero_restore()
    # damage_restore()
    # max_hp_heal()
    # armor_restore()


def change_hero_armor(armor):
    prev_armor = game_state["hero_armor"]
    game_state["hero_armor"] = armor
    get_screen().show_hero_armor_changed(armor - prev_armor)


def double_hero_armor():
    change_hero_armor(game_state["hero_armor"] * 2)


def get_screen() -> Screen:
    return screenHolder["screen"]


def use_heal_inside():
    use_heal()


def use_precision_strike_inside():
    monster = get_first_alive_monster()
    get_screen().show_hero_attacks()
    damage = calc_damage(game_state["hero_min_damage"], game_state["hero_max_damage"]) + 5
    monster.hp = monster.hp - damage  # ignores monster's armor
    game_state["hero_hp"] = game_state["hero_hp"] - 1  # lose one hp as 'payment'
    append_damage_log("Hero", damage, damage)
    get_screen().show_hero_hp_changed(-1)
    get_screen().show_monster_hp_changed(monster, 0 - damage)  # view processing monster_hp_changed
    after_hero_turn()


def use_aoe_strike_inside():
    damage = calc_damage(game_state["hero_min_damage"], game_state["hero_max_damage"]) - 1
    get_screen().show_hero_attacks()
    for monster in get_active_monster_pack():
        effective_damage = damage - monster.armor
        if effective_damage > 0:
            monster.hp = monster.hp - effective_damage
            get_screen().show_monster_hp_changed(monster, 0 - effective_damage)  # view processing monster_hp_changed
        else:
            get_screen().show_monster_blocked(monster)
        append_damage_log("Hero", damage, effective_damage)
    after_hero_turn()


def use_combo_strike_inside():
    monster = get_first_alive_monster()
    hero_attacks_monster(monster)
    hero_attacks_monster(monster)
    game_state["hero_armor"] = game_state["hero_armor"] - 5
    after_hero_turn()


def use_block_inside():
    game_state["hero_in_block"] = True
    game_state["hero_armor"] = game_state["hero_armor"] + 15
    get_screen().show_hero_armor_changed(+15)
    after_hero_turn()


def attack_first_alive_monster():
    monster = get_first_alive_monster()
    hero_attacks_monster(monster)


def get_active_monster_pack() -> List[Monster]:
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


def monster_attacks_hero(monster: Monster):
    time.sleep(0.2)
    get_screen().show_monster_attacks(monster)
    print(f'outside screen is {screen}')
    damages = monster.deal_damage(calc_damage, game_state)
    append_damage_log("Monster", damages[0], damages[1])
    effective_damage = damages[1]
    if effective_damage > 0:
        get_screen().show_hero_hp_changed(min(0, 0 - effective_damage))
    else:
        get_screen().show_hero_blocked()


def hero_attacks_monster(monster: Monster):
    get_screen().show_hero_attacks()  # view processing hero_attacked event
    damage = calc_damage(game_state["hero_min_damage"], game_state["hero_max_damage"])
    damages = monster.take_damage(damage)
    append_damage_log("Hero", damages[0], damages[1])
    effective_damage = damages[1]
    # if effective_damage > 0:
    #     get_screen().show_monster_hp_changed(monster, 0 - effective_damage)  # view processing monster_hp_changed
    # else:
    #     get_screen().show_monster_blocked(monster)


def append_damage_log(attacker, damage, effective_damage):
    if (effective_damage <= 0):
        game_state.get("game_log").append(f"{attacker} hit {damage} damage, all absorbed")
    else:
        game_state.get("game_log").append(f"{attacker} hit {damage} damage, {effective_damage} passes armor")
    get_screen().show_updated_log()


def ask_for_hero_action():
    return input("Press any key or Q to end the programm. Press H to heal and hit")


def ask_for_monster_turn():
    return input("Press any key for monster turn ")


def hero_turn():
    return turn % 2 == 1


# let's make this method called from thread when it picks event from queue


def hero_attack_inside():
    attack_first_alive_monster()
    after_hero_turn()


def after_hero_turn():
    if pack_is_dead():
        hero_rest()
        if last_pack_active():
            get_screen().draw_game_over()
            game_state["monsters_dead"] = True
            return
        switch_to_next_monster_pack()
        return
    monster_pack_attack()


def monster_pack_attack():
    for monster in get_active_monster_pack():
        if monster.alive():
            monster_attacks_hero(monster)
            if hero_is_dead():
                game_state["hero_dead"] = True
                return
    monsters_turn_end()


def game_restart():
    game_state.update(new_game_state())


queue = Queue()
screen = Screen(game_state, queue)
screenHolder["screen"] = screen


def watch_queue(queue: Queue, hero_attack_inside, use_heal_inside, use_precision_strike_inside, use_aoe_strike_inside,
                use_combo_strike_inside,
                use_block_inside,
                screen: Screen):
    while True:
        if not queue.empty():
            event = queue.get()
            print(f"picked event {event}")
            if event == "hero_attack":
                hero_attack_inside()
            elif event == "hero_heal":
                use_heal_inside()
            elif event == "precision_strike":
                use_precision_strike_inside()
            elif event == "aoe_strike":
                use_aoe_strike_inside()
            elif event == "combo_strike":
                use_combo_strike_inside()
            elif event == "block":
                use_block_inside()
            elif event == "restart":
                screen.show_on_restart()


# start queue watcher thread here
queue_watcher = threading.Thread(target=watch_queue,
                                 args=[queue, hero_attack_inside, use_heal_inside, use_precision_strike_inside,
                                       use_aoe_strike_inside,
                                       use_combo_strike_inside,
                                       use_block_inside,
                                       screen])
queue_watcher.setDaemon(True)
queue_watcher.start()

screen.start()
