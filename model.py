class Model:
    def __init__(self, prev_model, curr_model):
        self.prev_model=prev_model
        self.curr_model=curr_model

    def hero_hp_changed(self):
        return self.prev_model.get("hero_hp") != self.curr_model.get("hero_hp")

    def get_hero_hp_diff(self):
        return self.curr_model.get("hero_hp") - self.prev_model.get("hero_hp")