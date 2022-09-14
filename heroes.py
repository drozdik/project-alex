from monsters import Monster


class Hero:
    def __init__(self, event_listener):
        self.event_listener = event_listener
        self.hero_stuned_rounds = 0
        self.max_hp = 100
        self.hp = 100
        self.min_damage = 3
        self.max_damage = 20
        self.base_max_damage = 20
        self.armor = 0
        self.base_armor = 10
        self.hero_in_block = False
        self.healing_potions = 5
        self.hero_dead = False

    def change_hp(self, diff):
        prev = self.hp
        self.hp = max(0, self.hp + diff)
        self.event_listener.push_event({"type": "hero_hp_changed", "value": self.hp - prev, "hero": self})
        if self.is_dead():
            self.event_listener.push_event({"type": "hero_dead", "hero": self})

    def set_max_hp(self):
        diff = self.max_hp - self.hp
        self.hp = self.max_hp
        self.event_listener.push_event({"type": "hero_hp_changed", "value": diff, "hero": self})

    def set_max_damage_to_base_max(self):
        diff = self.base_max_damage - self.max_damage
        self.max_damage = self.base_max_damage
        self.event_listener.push_event({"type": "hero_max_damage_changed", "value": diff, "hero": self})

    def increase_base_max_damage_by(self, diff: int):
        # should I verify that number is positive?
        self.base_max_damage += diff
        self.event_listener.push_event({"type": "hero_base_max_damage_changed", "value": diff, "hero": self})

    def increase_base_min_damage_by(self, diff):
        # should I verify that number is positive?
        self.min_damage += diff
        self.event_listener.push_event({"type": "hero_base_min_damage_changed", "value": diff, "hero": self})

    def set_armor_to_base(self):
        diff = self.base_armor - self.armor
        self.armor = self.base_armor
        self.event_listener.push_event({"type": "hero_armor_changed", "value": diff, "hero": self})

    def is_dead(self):
        return self.hp <= 0

    def change_armor(self, diff):
        prev = self.armor
        self.armor = max(0, (self.armor + diff))
        self.event_listener.push_event({"type": "hero_armor_changed", "value": self.armor - prev, "hero": self})

    def change_max_damage(self, diff):
        prev = self.max_damage
        self.max_damage = max(0, self.max_damage + diff)
        self.event_listener.push_event(
            {"type": "hero_max_damage_changed", "value": self.max_damage - prev, "hero": self})

    def use_healing_potion(self):
        self.healing_potions -= 1
        self.hp += 5
        self.event_listener.push_event({"type": "hero_hp_changed", "value": +5, "hero": self})
        self.event_listener.push_event({"type": "hero_health_potion_used"})

        # if (game_state["healing_potions"] <= 0):
        #         raise Exception("No healing potions")
        # game_state['healing_potions'] -= 1
        # # get_screen().show_number_of_health_potions_changed(-1)
        # diff = calc_heal()
        # get_hero().change_hp(diff)
        # # if hero_is_stunned():
        # #     game_state["hero_stuned_rounds"] = 0
        # #     double_hero_armor()
        # #     game_state["hero_max_damage"] = game_state["hero_max_damage"] * 2
        # # hero_restore()
        # # damage_restore()
        # # max_hp_heal()
        # # armor_restore()
        #
        pass

    def fortune_rest(self):
        print('fortune rest not implemented')
        # rest = randint(1, 100)
        # if rest <= 60:
        #     add_healing_potions(1)
        #     get_hero().use_healing_poiton()
        #     game_state.get("game_log").append("Fortune:60% luck")
        # if rest >= 80:
        #     add_healing_potions(2)
        #     get_hero().use_healing_poiton()
        #     get_hero().use_healing_poiton()
        #     game_state.get("game_log").append("Fortune:20% luck")
        # if rest >= 70 and rest <= 75:
        #     get_hero().set_max_hp()
        #     get_hero().set_max_damage_to_base_max()
        #     game_state.get("game_log").append("Fortune:5% luck")
        #

    def power_increase(self):
        print('power_increase not implemented')
        #     hero_power_icrease = randint(1, 100)
        # if hero_power_icrease <= 50:
        #     get_hero().increase_base_max_damage_by(1)
        #     get_hero().increase_base_min_damage_by(1)
        # if hero_power_icrease >= 95:
        #     get_hero().increase_base_max_damage_by(2)
        #     get_hero().increase_base_min_damage_by(2)
        #

    def hero_rest(self):
        print('hero_rest not implemented')

    #     get_hero().set_armor_to_base()
    # get_hero().power_increase()
    # fortune_rest()
    def hero_restore(self):
        print('hero_restore not implemented')

    #     health_points = calc_heal()
    # get_hero().change_hp(health_points)
    # get_hero().increase_max_damage_by(4)
    # get_hero().change_max_damage(+4)
    # get_hero().change_armor(get_hero().armor * 2)
    #
    def damage_restore(self):
        # if get_hero().max_damage >= get_hero().base_max_damage:
        #     get_hero().set_max_damage_to_base_max()
        #     game_state.get("game_log").append("Restored max damage")
        # pass
        print('damage_restore not implemented')

    def use_precision_strike(self, monster):
        #     get_screen().show_hero_attacks()
        # damage = calc_damage(game_state["hero_min_damage"], game_state["hero_max_damage"]) + 5
        # monster.hp = monster.hp - damage  # ignores monster's armor
        # game_state["hero_hp"] = game_state["hero_hp"] - 1  # lose one hp as 'payment'
        # append_damage_log("Hero", damage, damage)
        # get_screen().show_hero_hp_changed(-1)
        # get_screen().show_monster_hp_changed(monster, 0 - damage)  # view processing monster_hp_changed
        #     pass
        print('use_precision_strike is not implemented')

    def use_aoe_strike(self, param):
        #     damage = calc_damage(game_state["hero_min_damage"], game_state["hero_max_damage"]) - 1
        # get_screen().show_hero_attacks()
        # for monster in get_active_monster_pack():
        #     effective_damage = damage - monster.armor
        #     if effective_damage > 0:
        #         monster.hp = monster.hp - effective_damage
        #         get_screen().show_monster_hp_changed(monster, 0 - effective_damage)  # view processing monster_hp_changed
        #     else:
        #         get_screen().show_monster_blocked(monster)
        #     append_damage_log("Hero", damage, effective_damage)
        #     pass
        print('use_aoe_strike is not implemented')

    def use_combo_strikee(self, monster):
        #     hero_attacks_monster(monster)
        # hero_attacks_monster(monster)
        # game_state["hero_armor"] = game_state["hero_armor"] - 5
        #     pass
        print('use_combo_strikee not implemented')

    def use_block(self):
        # game_state["hero_in_block"] = True
        # game_state["hero_armor"] = game_state["hero_armor"] + 15
        # get_screen().show_hero_armor_changed(+15)
        #     pass
        print('use_block not implemented')

    def attack_monster(self, monster: Monster):
        self.event_listener.push_event({"type": "hero_attacks", "hero": self, "monster": monster})
        monster.change_health(-1)
        #     get_screen().show_hero_attacks()  # view processing hero_attacked event
        # damage = calc_damage(game_state["hero_min_damage"], game_state["hero_max_damage"])
        # damages = monster.take_damage(damage)
        # append_damage_log("Hero", damages[0], damages[1])
        # effective_damage = damages[1]
        # # if effective_damage > 0:
        # #     get_screen().show_monster_hp_changed(monster, 0 - effective_damage)  # view processing monster_hp_changed
        # # else:
        # #     get_screen().show_monster_blocked(monster)
        #     pass
        print('attack_monster is not implemented')

    def hero_is_stunned(self):
        return self.hero_stuned_rounds > 0

    def stun(self):
        # if not get_hero().hero_is_stunned():
        #         game_state["hero_armor"] = game_state["hero_armor"] / 2
        #         game_state["hero_max_damage"] = int(game_state["hero_max_damage"] / 2)
        # game_state["hero_stuned_rounds"] = game_state["hero_stuned_rounds"] + 3
        #     pass
        print('hero stun is not implemented')

    def on_turn_end(self):
        #     if get_hero().hero_is_stunned():
        #         game_state["hero_stuned_rounds"] = game_state["hero_stuned_rounds"] - 1
        #         if not get_hero().hero_is_stunned():
        #             print("restore damage and armor")
        #             game_state["hero_armor"] = game_state["hero_armor"] * 2
        #             game_state["hero_max_damage"] = game_state["hero_max_damage"] * 2
        # if game_state["hero_in_block"]:
        #     game_state["hero_in_block"] = False
        #     game_state["hero_armor"] = game_state["hero_base_armor"]
        #
        print('hero on_turn_end is not implemented')
