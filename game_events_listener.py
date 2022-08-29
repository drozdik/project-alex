class GameEventsListener:
    def __init__(self, screenHolder):
        self.screenHolder = screenHolder

    def push_event(self, event):
        if event["type"] == "hero_armor_changed":
            self.screenHolder["screen"].on_hero_armor_changed(-2)
        else:
            raise Exception("Unknown type of event", event)


class TestGameEventsListener:
    def __init__(self):
        self.events = []

    def push_event(self, event):
        self.events.append(event)
