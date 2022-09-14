from random import randint

from game_events import GameEventsListener


class Monster:
    max_hp = 30
    armor = 3
    hp = 30
    name = "Skeleton"
    clazz = "Skeleton"
    min_damage = 3
    max_damage = 15

    # def __init__(self, screenHolder):
    #     self.screenHolder = screenHolder

    def __init__(self, event_listener: GameEventsListener):
        self.event_listener = event_listener

    def alive(self):
        return self.hp > 0

    def dead(self):
        return not self.alive()

    def take_damage(self, damage):
        effective_damage = damage - self.armor
        if effective_damage > 0:
            self.hp = self.hp - effective_damage
            self.event_listener.push_event({"type": "monster_hp_changed", "value": -1, "monster": self})
        else:
            self.event_listener.push_event({"type": "monster_blocked", "monster": self})
        return (damage, effective_damage)

    def deal_damage(self, calc_damage, game_state):
        damage = calc_damage(self.min_damage, self.max_damage)
        effective_damage = damage - game_state["hero_armor"]
        if effective_damage > 0:
            game_state["hero_hp"] = game_state["hero_hp"] - effective_damage
            self.special(game_state)
        return (damage, effective_damage)

    def special(self, game_state):
        pass

    def attack(self, param):
        #     time.sleep(0.2)
        # get_screen().show_monster_attacks(monster)
        # print(f'outside screen is {screen}')
        # damages = monster.deal_damage(calc_damage, game_state)
        # append_damage_log("Monster", damages[0], damages[1])
        # effective_damage = damages[1]
        # if effective_damage > 0:
        #     get_screen().show_hero_hp_changed(min(0, 0 - effective_damage))
        # else:
        #     get_screen().show_hero_blocked()
        #     pass
        #
        print('monster attack is not implemented')

    def change_health(self, diff):
        self.hp = max(0, self.hp + diff)


class Skeleton(Monster):
    max_hp = 3
    armor = 3
    hp = 3
    name = "Skeleton"
    clazz = "Skeleton"
    min_damage = 3
    max_damage = 15

    def __init__(self, event_listener: GameEventsListener):
        Monster.__init__(self, event_listener)

    def special(self, game_state):
        game_state["hero_armor"] = game_state["hero_armor"] - 2
        # events.push({source=self, name="armor_changed", value=-2})
        # self.screenHolder["screen"].on_hero_armor_changed(-2)  # should be called from Hero class
        self.event_listener.push_event({
            "type": "hero_armor_changed",
            "value": -2
        })


class SkeletonMage(Monster):
    max_hp = 10
    hp = 10
    armor = 2
    name = "Skeleton-mage"
    clazz = "Skeleton-mage"
    min_damage = 10
    max_damage = 14

    def special(self, game_state):
        print("SkeletonMAge special")
        prev_max_damage = game_state["hero_max_damage"]
        game_state["hero_max_damage"] = game_state["hero_max_damage"] - 5
        if game_state["hero_max_damage"] <= game_state["hero_min_damage"]:
            game_state["hero_max_damage"] = game_state["hero_min_damage"]
        damage_diff = game_state["hero_max_damage"] - prev_max_damage
        if damage_diff == 0:
            return
        self.event_listener.push_event({
            "type": "hero_max_damage_changed",
            "value": damage_diff,
            "hero": game_state
        })


class SkeletonLich(Monster):
    max_hp = 60
    hp = 60
    armor = 18
    name = "Skeleton-Lich"
    clazz = "Skeleton-Lich"
    min_damage = 10
    max_damage = 20

    def hero_is_stunned(self, game_state):
        return game_state["hero_stuned_rounds"] > 0

    def lich_stun(self, game_state):
        if not self.hero_is_stunned(game_state):
            game_state["hero_armor"] = game_state["hero_armor"] / 2
            game_state["hero_max_damage"] = int(game_state["hero_max_damage"] / 2)
        game_state["hero_stuned_rounds"] = game_state["hero_stuned_rounds"] + 3

    def special(self, game_state):
        print("SkeletonLich special")
        lich_will_stun = randint(1, 10) <= 2
        if lich_will_stun:
            self.lich_stun(game_state)
