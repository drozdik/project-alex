
class GameEventsListener:
    def __init__(self, screenHolder):
        self.screenHolder = screenHolder

    def push_event(self, event):
        if event["type"] == "hero_armor_changed":
            self.get_screen().on_hero_armor_changed(-2)
        elif event["type"] == "monster_blocked":
            self.get_screen().show_monster_blocked(event["monster"])
        elif event["type"] == "monster_hp_changed":
            self.get_screen().show_monster_hp_changed(event["monster"], event["value"])
        elif event["type"] == "hero_max_damage_changed":
            self.get_screen().show_hero_max_damage_changed(event["value"])
        elif event["type"] == "hero_armor_changed":
            self.get_screen().show_hero_armor_changed(event["value"])
        elif event["type"] == "hero_potions_number_changed":
            self.get_screen().show_number_of_health_potions_changed(event["value"])
        else:
            raise Exception("Unknown type of event", event)

    def get_screen(self):
        return self.screenHolder["screen"]


class TestGameEventsListener:
    def __init__(self):
        self.events = []

    def push_event(self, event):
        self.events.append(event)
