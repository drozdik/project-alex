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
