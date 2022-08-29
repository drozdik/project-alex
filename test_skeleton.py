import unittest

from game_events_listener import TestGameEventsListener
from monsters import Skeleton


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


class TestUser(unittest.TestCase):
    screen_holder = {}

    def test_skeleton_special_ability_decrease_hero_armor(self):
        # given
        initial_hero_armor = 10
        game_state = new_game_state()
        game_state["hero_armor"] = initial_hero_armor
        events_listener = TestGameEventsListener()
        skeleton = Skeleton(self.screen_holder, events_listener)

        # when
        skeleton.special(game_state)

        # then
        message = f"Expect initial armor {initial_hero_armor} decreased by 2"
        self.assertEqual(game_state["hero_armor"], initial_hero_armor - 2, message)

    def test_skeleton_hp_same_when_damage_less_or_equal_to_armor(self):
        events_listener = TestGameEventsListener()
        skeleton = Skeleton(self.screen_holder, events_listener)
        initial_hp = skeleton.hp
        skeleton.take_damage(skeleton.armor - 1)
        skeleton.take_damage(skeleton.armor)
        message = f"Expect initial hp {initial_hp} stays same"
        self.assertEqual(skeleton.hp, initial_hp, message)


if __name__ == '__main__':
    unittest.main()
