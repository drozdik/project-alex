import unittest
from unittest import TestCase

from game_events import TestGameEventsListener
from heroes import Hero


class TestHero(unittest.TestCase):

    def test_hero_set_max_hp_will_raise_hp_back_to_max(self):
        # given
        events = TestGameEventsListener()
        hero = Hero(events)
        hero.hp = hero.max_hp - 1
        # when
        hero.set_max_hp()
        # then
        message = f"Expect hp {hero.hp} to be {hero.max_hp}"
        self.assertEqual(hero.max_hp, hero.hp, message)
        self.assertEqual([{"type": "hero_hp_changed", "value": 1, "hero": hero}], events.events)

    def test_hero_set_max_hp_will_lower_hp_back_to_max(self):
        # given
        events = TestGameEventsListener()
        hero = Hero(events)
        hero.hp = hero.max_hp + 1
        # when
        hero.set_max_hp()
        # then
        message = f"Expect hp {hero.hp} to be {hero.max_hp}"
        self.assertEqual(hero.max_hp, hero.hp, message)

    def test_set_max_damage_to_base_max_will_raise_max_damage(self):
        # given
        events = TestGameEventsListener()
        hero = Hero(events)
        hero.max_damage = hero.base_max_damage - 1
        # when
        hero.set_max_damage_to_base_max()
        # then
        message = f"Expect max damage {hero.max_damage} to be {hero.base_max_damage}"
        self.assertEqual(hero.base_max_damage, hero.max_damage, message)
        self.assertEqual([{"type": "hero_max_damage_changed", "value": 1, "hero": hero}], events.events)

    def test_set_max_damage_to_base_max_will_lower_max_damage(self):
        # given
        events = TestGameEventsListener()
        hero = Hero(events)
        hero.max_damage = hero.base_max_damage + 1
        # when
        hero.set_max_damage_to_base_max()
        # then
        message = f"Expect max damage {hero.max_damage} to be {hero.base_max_damage}"
        self.assertEqual(hero.base_max_damage, hero.max_damage, message)

    def test_increase_base_max_damage_by(self):
        # given
        events = TestGameEventsListener()
        hero = Hero(events)
        initial_base_max_damage = hero.base_max_damage
        # when
        hero.increase_base_max_damage_by(1)
        # then
        message = f"Expect base max damage {hero.base_max_damage} to be {hero.base_max_damage + 1}"
        self.assertEqual(initial_base_max_damage + 1, hero.base_max_damage, message)
        self.assertEqual([{"type": "hero_base_max_damage_changed", "value": 1, "hero": hero}], events.events)

    def test_increase_base_min_damage_by(self):
        # given
        events = TestGameEventsListener()
        hero = Hero(events)
        initial_base_min_damage = hero.min_damage
        # when
        hero.increase_base_min_damage_by(1)
        # then
        message = f"Expect base min damage {hero.min_damage} to be {hero.min_damage + 1}"
        self.assertEqual(initial_base_min_damage + 1, hero.min_damage, message)
        self.assertEqual([{"type": "hero_base_min_damage_changed", "value": 1, "hero": hero}], events.events)

    def test_set_armor_to_base_will_increase_armor(self):
        # given
        events = TestGameEventsListener()
        hero = Hero(events)
        hero.armor = hero.base_armor - 1
        # when
        hero.set_armor_to_base()
        # then
        message = f"Expect armor {hero.armor} to be base armor {hero.base_armor}"
        self.assertEqual(hero.base_armor, hero.armor, message)
        self.assertEqual([{"type": "hero_armor_changed", "value": 1, "hero": hero}], events.events)

    def test_set_armor_to_base_will_decrease_armor(self):
        # given
        events = TestGameEventsListener()
        hero = Hero(events)
        hero.armor = hero.base_armor + 1
        # when
        hero.set_armor_to_base()
        # then
        message = f"Expect armor {hero.armor} to be base armor {hero.base_armor}"
        self.assertEqual(hero.base_armor, hero.armor, message)

    def test_change_hp_wont_set_below_zero(self):
        # given
        events = TestGameEventsListener()
        hero = Hero(events)
        hero.hp = 10
        # when
        hero.change_hp(-11)
        # then
        self.assertEqual(0, hero.hp, f"Expect hp to be 0")
        self.assertIn({"type": "hero_hp_changed", "value": -10, "hero": hero}, events.events)

    def test_change_hp(self):
        # given
        events = TestGameEventsListener()
        hero = Hero(events)
        hero.hp = 10
        # when
        hero.change_hp(1)
        # then
        self.assertEqual(11, hero.hp, f"Expect hp to be 11")

    def test_change_hp(self):
        # given
        events = TestGameEventsListener()
        hero = Hero(events)
        hero.hp = 10
        # when
        hero.change_hp(1)
        # then
        self.assertEqual(11, hero.hp, f"Expect hp to be 11")

    def test_hero_is_dead(self):
        # given
        events = TestGameEventsListener()
        alive_hero = Hero(events)
        alive_hero.change_hp(+1)
        dead_hero = Hero(events)
        dead_hero.change_hp(-dead_hero.hp)
        # then
        self.assertFalse(alive_hero.is_dead(), f"Expect hero with hp {alive_hero.hp} to be alive")
        self.assertTrue(dead_hero.is_dead(), f"Expect hero with hp {dead_hero.hp} to be dead")
        self.assertIn({"type": "hero_dead", "hero": dead_hero}, events.events)

    def test_change_armor_increases(self):
        # given
        events = TestGameEventsListener()
        hero = Hero(events)
        hero.armor = 10
        # when
        hero.change_armor(2)
        # then
        self.assertEqual(12, hero.armor, f"Expect armor to be {12}")
        self.assertEqual([{"type": "hero_armor_changed", "value": 2, "hero": hero}], events.events)

    def test_change_armor_decreases(self):
        # given
        events = TestGameEventsListener()
        hero = Hero(events)
        hero.armor = 10
        # when
        hero.change_armor(-2)
        # then
        self.assertEqual(8, hero.armor, f"Expect armor to be {8}")

    def test_change_armor_adds_event(self):
        # given
        events = TestGameEventsListener()
        hero = Hero(events)
        hero.armor = 10
        # when
        hero.change_armor(-2)
        # then
        self.assertEqual(8, hero.armor, f"Expect armor to be {8}")
        self.assertEqual([{"type": "hero_armor_changed", "value": -2, "hero": hero}], events.events)

    def test_change_armor_wont_decrease_below_zero(self):
        # given
        events = TestGameEventsListener()
        hero = Hero(events)
        hero.armor = 1
        # when
        hero.change_armor(-2)
        # then
        self.assertEqual(0, hero.armor, f"Expect armor to be {0}")
        self.assertIn({"type": "hero_armor_changed", "value": -1, "hero": hero}, events.events)

    def test_set_armor_to_base(self):
        # given
        events = TestGameEventsListener()
        hero = Hero(events)
        hero.base_armor = 10
        hero.armor = 0
        # when
        hero.set_armor_to_base()
        # then
        self.assertEqual(10, hero.armor, f"Expect armor to be {10}")
        self.assertIn({"type": "hero_armor_changed", "value": 10, "hero": hero}, events.events)

    def test_change_max_damage(self):
        # given
        events = TestGameEventsListener()
        hero = Hero(events)
        hero.max_damage = 10
        # when
        hero.change_max_damage(+1)
        # then
        self.assertEqual(11, hero.max_damage, f"Expect max damage to be 11")
        self.assertIn({"type": "hero_max_damage_changed", "value": 1, "hero": hero}, events.events)

    def test_change_max_damage_wont_change_below_zero(self):
        # given
        events = TestGameEventsListener()
        hero = Hero(events)
        hero.max_damage = 10
        # when
        hero.change_max_damage(-11)
        # then
        self.assertEqual(0, hero.max_damage, f"Expect max damage to be 0")
        self.assertIn({"type": "hero_max_damage_changed", "value": -10, "hero": hero}, events.events)

    def test_use_healing_potion(self):
        events = TestGameEventsListener()
        hero = Hero(events)
        hero.healing_potions = 3
        hero.hp = 10

        hero.use_healing_potion()

        self.assertEqual(2, hero.healing_potions, f"Expect number of healing potions to be 2")
        self.assertGreater(hero.hp, 10, f"Expect hp greater than 10")
        event_types = [event["type"] for event in events.events]
        self.assertIn("hero_hp_changed", event_types)
        self.assertIn("hero_health_potion_used", event_types)
