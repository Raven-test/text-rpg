import unittest
from testfixtures import Replacer
from testfixtures import replace

from rpg import *
from rooms import rooms
from player import player


# https://pythonhosted.org/testfixtures/mocking.html

class TestOne(unittest.TestCase):

    def test_get_all_desc_words(self):
        """all items in list"""
        # list by method is created randomly, test fails every now and then
        expected_item_list = ['gold']
        expected_desc_words = ['coin', 'gold']
        self.assertEqual(get_all_desc_words(expected_item_list), expected_desc_words)


class TestMoveDirection(unittest.TestCase):

    def test_move_direction_no_event(self):
        player['location'] = "v1"
        direction = "n"
        expected = None
        self.assertEqual(Rpg().move_direction(direction), expected)

    def test_do_north(self):
        player['location'] = "v1"
        direction = "n"
        expected = None
        self.assertEqual(Rpg().do_north(direction), expected)

    def test_move_direction_combat_event(self):
        player['location'] = "v1"
        direction = "e"
        expected = 'combat'
        self.assertEqual(Rpg().move_direction(direction), expected)

    def test_move_direction_invalid_direction(self):
        player['location'] = "v1"
        direction = "z"
        expected = "You cannot go in that direction."
        self.assertEqual(Rpg().move_direction(direction), expected)


class TestLocation(unittest.TestCase):
    def test_text_location_name(self):
        with Replacer() as replacer:
            loc = "v1"
            location_name = rooms[loc]['name']
            replacer('rooms.rooms.loc.name', 'Test name')
            expected_name = "Main square"
            self.assertEqual(Location().location_name(loc), expected_name)

    def test_location_no_npcs(self):
        loc = "v1"
        expected_npcs = None
        self.assertEqual(Location().location_npcs(loc), expected_npcs)

    def test_location_npcs(self):
        loc = "v2"
        expected_npcs = ("Greg", "shopkeeper")
        self.assertEqual(Location().location_npcs(loc), expected_npcs)

    def test_location_no_shop(self):
        loc = "v1"
        expected_shop = None
        self.assertEqual(Location().location_shop(loc), expected_shop)

    def test_location_has_shop(self):
        loc = "v2"
        expected_shop = ('potion', 1)
        self.assertEqual(Location().location_shop(loc), expected_shop)

    def test_location_has_items(self):
        loc = "v1"
        expected_items = ['gold description on the ground', 'stone description on the ground']
        self.assertEqual(Location().location_items(loc), expected_items)

    def test_location_no_items(self):
        loc = "v2"
        expected_items = None
        self.assertEqual(Location().location_items(loc), expected_items)

    def test_location_no_monsters(self):
        loc = "v1"
        expected_monsters = []
        self.assertEqual(Location().location_monsters(loc), expected_monsters)

    def test_location_has_monsters(self):
        loc = "v3"
        expected_monsters = ["small orc warrior", "big troll", "big orc warrior"]
        self.assertEqual(Location().location_monsters(loc), expected_monsters)

    def test_location_no_events(self):
        loc = "v1"
        expected_events = None
        self.assertEqual(Location().location_events(loc), expected_events)

    def test_location_combat_event(self):
        loc = "v3"
        expected_events = ["combat"]
        self.assertEqual(Location().location_events(loc), expected_events)


class TestActions(unittest.TestCase):

    def test_take_item(self):
        """Test not correct yet, need to override the items on the ground otherwise other tests will fail"""
        takable_items_list = ['item1', 'item2']
        item_to_take = "item1"
        expected = None
        self.assertEqual(Rpg().do_take(item_to_take), expected)


class TestBuy(unittest.TestCase):

    def test_buy_no_argument(self):
        with Replacer() as replacer:
            replacer('player.player.location', 'v2')
            item = "potion"
            expected = "What would you like to buy?"
            self.assertEqual(Shop().buy(''), expected)

    def test_buy_empty_argument(self):
        with Replacer() as replacer:
            replacer('player.player.location', 'v2')
            item = "potion"
            expected = "What would you like to buy?"
            self.assertEqual(Shop().buy(' '), expected)

    def test_buy_nonexisting_item(self):
        with Replacer() as replacer:
            replacer('player.player.location', 'v2')
            item = "zzzz"
            expected = "item is not sold here"
            self.assertEqual(Shop().buy(item), expected)

    def test_buy_not_a_shop(self):
        with Replacer() as replacer:
            replacer('player.player.location', 'v6')
            item = "potion"
            expected = "This is not a shop"
            # self.assertEqual(Rpg().do_buy(item), expected)
            self.assertEqual(Shop().buy(item), expected)

    @replace('player.player.inv', [])
    def test_buy_insufficient_funds(self):
        with Replacer() as replacer:
            replacer('player.player.location', 'v2')
            item = "potion"
            expected = "You do not have enough gold to buy that."
            self.assertEqual(Shop().buy(item), expected)

    @replace('player.player.inv', ['gold'])
    def test_buy_success(self):
        with Replacer() as replacer:
            replacer('player.player.location', 'v2')
            item = "potion"
            expected_text = "item bought"
            expected_inv = ['potion']
            inv = player['inv']
            self.assertEqual(Shop().buy(item), expected_text)
            self.assertEqual(inv, expected_inv)


class TestSell(unittest.TestCase):

    @replace('player.player.location', "v6")
    @replace('player.player.inv', ['potion'])
    def test_sell_not_a_shop(self):
        item = "potion"
        expected = "This is not a shop"
        self.assertEqual(Shop().sell(item), expected)

    @replace('player.player.location', "v2")
    def test_sell_no_argument(self):
        expected = "What would you like to sell?"
        self.assertEqual(Shop().sell(''), expected)

    @replace('player.player.location', "v2")
    def test_sell_empty_argument(self):
        expected = "What would you like to sell?"
        self.assertEqual(Shop().sell(' '), expected)

    @replace('player.player.location', "v2")
    @replace('player.player.inv', ['potion'])
    def test_sell_incorrect_item(self):
        item = "zzzz"
        expected = "no such item to sell"
        self.assertEqual(Shop().sell(item), expected)

    @replace('player.player.location', "v2")
    @replace('player.player.inv', ['potion'])
    def test_sell_success(self):
        item = "potion"
        expected_text = "item sold"
        expected_inv = ['gold']
        inv = player['inv']
        self.assertEqual(Shop().sell(item), expected_text)
        self.assertEqual(inv, expected_inv)


class TestTake(unittest.TestCase):

    @replace('player.player.location', "v1")
    @replace('rooms.rooms.v1.ground', ['stone'])
    @replace('player.player.inv', [])
    def test_take_no_argument(self):
        item = "stone"
        expected_text = "Take which item? (use the look command)"
        expected_inv = []
        inv = player['inv']
        self.assertEqual(DropTake().take(''), expected_text)
        self.assertEqual(inv, expected_inv)

    @replace('player.player.location', "v1")
    @replace('rooms.rooms.v1.ground', ['stone'])
    @replace('player.player.inv', [])
    def test_take_empty_argument(self):
        item = "stone"
        expected_text = "Take which item? (use the look command)"
        expected_inv = []
        inv = player['inv']
        self.assertEqual(DropTake().take(' '), expected_text)
        self.assertEqual(inv, expected_inv)

    @replace('player.player.location', "v1")
    @replace('rooms.rooms.v1.ground', ['stone'])
    @replace('player.player.inv', [])
    def test_take_nonexisting_item(self):
        item = "zzzzz"
        expected_text = "That is not on the ground."
        expected_inv = []
        inv = player['inv']
        self.assertEqual(DropTake().take(item), expected_text)
        self.assertEqual(inv, expected_inv)

    @replace('player.player.location', "v1")
    @replace('rooms.rooms.v1.ground', ['stone'])
    @replace('player.player.inv', [])
    def test_take_item_success(self):
        item = "stone"
        expected_text = "item taken"
        expected_inv = ['stone']
        expected_ground = []
        ground = rooms['v1']['ground']
        inv = player['inv']
        self.assertEqual(DropTake().take(item), expected_text)
        self.assertEqual(inv, expected_inv)
        self.assertEqual(ground, expected_ground)


class TestDrop(unittest.TestCase):

    @replace('player.player.location', "v1")
    @replace('rooms.rooms.v1.ground', [])
    @replace('player.player.inv', ['stone'])
    def test_drop_no_argument(self):
        item = "stone"
        expected_text = "Drop which item?"
        expected_inv = ['stone']
        inv = player['inv']
        self.assertEqual(DropTake().drop(''), expected_text)
        self.assertEqual(inv, expected_inv)

    @replace('player.player.location', "v1")
    @replace('rooms.rooms.v1.ground', [])
    @replace('player.player.inv', ['stone'])
    def test_drop_empty_argument(self):
        item = "stone"
        expected_text = "Drop which item?"
        expected_inv = ['stone']
        inv = player['inv']
        self.assertEqual(DropTake().drop(' '), expected_text)
        self.assertEqual(inv, expected_inv)

    @replace('player.player.location', "v1")
    @replace('rooms.rooms.v1.ground', [])
    @replace('player.player.inv', ['stone'])
    def test_drop_nonexisting_item(self):
        item = "zzzzz"
        expected_text = "no item in inventory to drop"
        expected_inv = ['stone']
        inv = player['inv']
        self.assertEqual(DropTake().drop(item), expected_text)
        self.assertEqual(inv, expected_inv)

    @replace('player.player.location', "v1")
    @replace('rooms.rooms.v1.ground', [])
    @replace('player.player.inv', ['stone'])
    def test_drop_item_success(self):
        item = "stone"
        expected_text = "item dropped"
        expected_inv = []
        expected_ground = ['stone']
        ground = rooms['v1']['ground']
        inv = player['inv']
        self.assertEqual(DropTake().drop(item), expected_text)
        self.assertEqual(inv, expected_inv)
        self.assertEqual(ground, expected_ground)


class TestPlayer(unittest.TestCase):

    @replace('player.player.inv', [])
    def test_player_empty_inventory(self):
        expected_text = "Inventory:\n (nothing)"
        expected_inv = []
        inv = player['inv']
        self.assertEqual(Player().inventory(), expected_text)
        self.assertEqual(inv, expected_inv)

    @replace('player.player.inv', ['gold'])
    def test_player_inventory_one_item(self):
        expected_items = 'gold'
        expected_inv = ['gold']
        inv = player['inv']
        self.assertEqual(Player().inventory(), expected_items)
        self.assertEqual(inv, expected_inv)

    @replace('player.player.inv', ['gold', 'gold'])
    def test_player_inventory_two_items(self):
        expected_items = {'gold': 2}
        expected_inv = ['gold', 'gold']
        inv = player['inv']
        self.assertEqual(Player().inventory(), expected_items)
        self.assertEqual(inv, expected_inv)


if __name__ == "__main":
    # unittest.main()
    test_classes_to_run = [TestOne, TestLocation, TestMoveDirection, TestActions]

    loader = unittest.TestLoader()
    suites_list = []
    for test_class in test_classes_to_run:
        suite = loader.loadTestsFromTestCase(test_class)
        suites_list.append(suite)

    big_suite = unittest.TestSuite(suites_list)

    runner = unittest.TextTestRunner()
    results = runner.run(big_suite)
