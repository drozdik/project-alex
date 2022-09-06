import unittest

from game_events_listener import TestGameEventsListener
from monsters import SkeletonMage


class TestSkeletonMage(unittest.TestCase):
    def test_special_ability_decrease_hero_max_damage(self):
        # given
        game_events = TestGameEventsListener()
        skeleton_mage = SkeletonMage({}, game_events)
        initial_max_damage = 15
        game_state = new_game_state()
        game_state["hero_max_damage"] = initial_max_damage

        # when
        skeleton_mage.special(game_state)

        # then
        message = f"Expect initial max damage {initial_max_damage} decreased by 5"
        self.assertEqual(game_state["hero_max_damage"], initial_max_damage - 5, message)
        self.assertIn({"type": "hero_max_damage_changed", "value": -5, "hero": game_state}, game_events.events)

    def test_special_ability_will_not_decrease_hero_max_damage_below_minimum(self):
        # given
        game_events = TestGameEventsListener()
        skeleton_mage = SkeletonMage({}, game_events)
        game_state = new_game_state()
        game_state["hero_min_damage"] = 5
        game_state["hero_max_damage"] = 6

        # when
        skeleton_mage.special(game_state)

        # then
        message = f"Expect initial max damage 6 decreased to min damage 5"
        self.assertEqual(game_state["hero_max_damage"], 5, message)
        self.assertIn({"type": "hero_max_damage_changed", "value": -1, "hero": game_state}, game_events.events)

    def test_special_ability_will_not_change_hero_max_damage_if_already_at_minimum(self):
        # given
        game_events = TestGameEventsListener()
        skeleton_mage = SkeletonMage({}, game_events)
        game_state = new_game_state()
        game_state["hero_min_damage"] = 5
        game_state["hero_max_damage"] = 5

        # when
        skeleton_mage.special(game_state)

        # then
        message = f"Expect initial max damage same 5"
        self.assertEqual(game_state["hero_max_damage"], 5, message)
        self.assertEquals(0, len(game_events.events), "Expect no game events")


def new_game_state():
    state = {
        "hero_stuned_rounds": 0,
        "hero_max_hp": 100,
        "hero_hp": 100,
        "hero_min_damage": 3,
        "hero_max_damage": 20,
        "hero_base_max_damage": 20,
        "hero_armor": 10,
        "hero_base_armor": 10,
        "hero_in_block": False,
        "healing_potions": 5,
        "monster_packs": [],
        "active_monster_pack_index": 0,
        "active_monster_pack": [],
        "game_log": [],
        "hero_dead": False,
        "monsters_dead": False
    }
    return state


if __name__ == '__main__':
    unittest.main()
