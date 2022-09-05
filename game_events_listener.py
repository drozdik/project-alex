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
        else:
            raise Exception("Unknown type of event", event)

    def get_screen(self):
        return self.screenHolder["screen"]


class TestGameEventsListener:
    def __init__(self):
        self.events = []

    def push_event(self, event):
        self.events.append(event)
