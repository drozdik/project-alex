import threading
from queue import Queue
from random import randint
from typing import List

from game_events import GameEventsListener
from gameui import Screen
from heroes import Hero
from monsters import Monster, Skeleton, SkeletonLich, SkeletonMage


class Game:
    def __init__(self, event_listener):
        self.event_listener = event_listener
        self.screen = None
        self.screenHolder = {"screen": self.screen}
        event_listener = GameEventsListener(self.screenHolder)
        turn = 1
        self.game_state = self.new_game_state()
        self.game_state["active_monster_pack"] = self.game_state["monster_packs"][
            self.game_state["active_monster_pack_index"]]

    def calc_damage(self, min_damage, max_damage):
        damage = randint(min_damage, max_damage)
        luck = self.roll_dice(20)
        if luck == 10:
            damage = damage * 2
            self.game_state.get("game_log").append("Critical damage")
        if luck == 1:
            damage = min_damage
            self.game_state.get("game_log").append("Critical miss")
        return damage

    def roll_dice(self, sides):
        result = randint(1, sides)
        return result

    def calc_heal(self):
        health_points = randint(20, 40)
        luck = self.roll_dice(10)
        if luck == 10:
            self.game_state.get("game_log").append("God loves you")
            health_points = health_points * 2
        return health_points

    def new_game_state(self):
        state = {
            "hero": Hero(self.event_listener),
            "monster_packs": self.create_monster_packs(),
            "active_monster_pack_index": 0,
            "active_monster_pack": [Monster(self.screenHolder, self.event_listener),
                                    Monster(self.screenHolder, self.event_listener)],
            "game_log": [],
            "monsters_dead": False
        }
        state["active_monster_pack"] = state["monster_packs"][state["active_monster_pack_index"]]
        return state

    def create_monster_packs(self) -> List[Monster]:
        packs = []
        for i in range(3):
            pack = [Skeleton(self.screenHolder, self.event_listener), Skeleton(self.screenHolder, self.event_listener)]
            mage_chance = randint(1, 100)
            if mage_chance < 20:
                pack[1] = SkeletonMage(self.screenHolder, self.event_listener)
                mage_chance = randint(1, 100)
                if mage_chance < 10:
                    pack[0] = SkeletonMage(self.screenHolder, self.event_listener)
            lich_chance = randint(1, 100)
            if lich_chance < (0 + i * 10):
                pack = [Skeleton(self.screenHolder, self.event_listener),
                        SkeletonLich(self.screenHolder, self.event_listener)]
                packs.append(pack)
                break
            packs.append(pack)
        return packs

    def switch_to_next_monster_pack(self, ):
        print('switching to next monster pack')
        self.game_state["active_monster_pack_index"] += 1
        self.game_state["active_monster_pack"] = self.game_state["monster_packs"][
            self.game_state["active_monster_pack_index"]]
        self.get_screen().show_new_monsters_pack()
        self.game_state.get("game_log").append("\nNew monsters arrived\n")

    def add_healing_potions(self, count):
        self.game_state["healing_potions"] = self.game_state["healing_potions"] + count

    def get_hero(self, ) -> Hero:
        return self.game_state["hero"]

    def pack_is_dead(self, ):
        for monster in self.get_active_monster_pack():
            if monster.alive():
                return False
        return True

    def all_packs_are_dead(self, ):
        return self.game_state["active_monster_pack_index"] == len(self.game_state["monster_packs"])

    def last_pack_active(self, ):
        return self.game_state["active_monster_pack_index"] == len(self.game_state["monster_packs"]) - 1

    def get_screen(self, ) -> Screen:
        return self.screenHolder["screen"]

    def use_heal_inside(self, ):
        self.get_hero().use_healing_poiton()

    def use_precision_strike_inside(self, ):
        monster = self.get_first_alive_monster()
        self.get_hero().use_precision_strike(monster)
        self.after_hero_turn()

    def use_aoe_strike_inside(self, ):
        self.get_hero().use_aoe_strike(self.get_active_monster_pack())
        self.after_hero_turn()

    def use_combo_strike_inside(self, ):
        monster = self.get_first_alive_monster()
        self.get_hero().use_combo_strikee(monster)
        self.after_hero_turn()

    def use_block_inside(self, ):
        self.get_hero().use_block()
        self.after_hero_turn()

    def attack_first_alive_monster(self, ):
        monster = self.get_first_alive_monster()
        self.get_hero().attack_monster(monster)

    def get_active_monster_pack(self, ) -> List[Monster]:
        return self.game_state["active_monster_pack"]

    def get_first_alive_monster(self, ):
        for monster in self.get_active_monster_pack():
            if monster.alive():
                return monster

    def monsters_turn_end(self, ):
        self.get_hero().on_turn_end()

    def hero_attack_inside(self, ):
        self.attack_first_alive_monster()
        self.after_hero_turn()

    def after_hero_turn(self, ):
        if self.pack_is_dead():
            self.get_hero().hero_rest()
            if self.last_pack_active():
                self.get_screen().draw_game_over()
                self.game_state["monsters_dead"] = True
                return
            self.switch_to_next_monster_pack()
            return
        self.monster_pack_attack()

    def monster_pack_attack(self, ):
        for monster in self.get_active_monster_pack():
            if monster.alive():
                monster.attack(self.get_hero())
                if self.get_hero().is_dead():
                    self.game_state["hero_dead"] = True
                    return

    def game_restart(self, ):
        self.game_state.update(self.new_game_state())

    def listen(self, ui_events: Queue):
        self.start_listening(ui_events)

    def watch_queue(self):
        print('start watch_queue')
        while True:
            if not self.queue.empty():
                event = self.queue.get()
                print(f"picked event {event}")
                if event == "hero_attack":
                    self.hero_attack_inside()
                elif event == "hero_heal":
                    self.use_heal_inside()
                elif event == "precision_strike":
                    self.use_precision_strike_inside()
                elif event == "aoe_strike":
                    self.use_aoe_strike_inside()
                elif event == "combo_strike":
                    self.use_combo_strike_inside()
                elif event == "block":
                    self.use_block_inside()
                elif event == "restart":
                    self.screen.show_on_restart()

    def start_listening(self, queue: Queue):
        self.queue = queue
        queue_watcher = threading.Thread(target=self.watch_queue)

        queue_watcher.setDaemon(True)
        queue_watcher.start()
