import unittest
from testfixtures import *
# from rpg import get_all_desc_words
from rpg import *


# https://pythonhosted.org/testfixtures/mocking.html

class TestTest(unittest.TestCase):

    # def test_move_direction(self):
    #     expected_text = "You cannot go in that direction"
    #     self.move_direction('w')

    # def test_display_location_name_nokey(self):
    #     with Replace('rpg.worldRooms[location}.name', not_there):
    #         location = "v1"
    #         expected_outcome = "Unnamed location"
    #         self.assertEqual(PrintText().display_location_name(location), expected_outcome)

    # def test_display_items_at_location_itemlist(self):
    #     location = "v1"
    #     expected_list = ["item1", "item2"]
    #     with Replacer() as replace:
    #         replace("worldRooms[location]['ground'].0", "item1")
    #         replace("worldRooms[location]['ground'].1", "item2")
    #         self.assertEqual(PrintText().display_items_at_location(location), "Items on the ground:")

    # def testtest(self):
    #     with Replacer() as replace:
    #         replace(worldRooms[location]["name"], "Testname")
    
    # def test_get_all_desc_words(self):
    #     """all items in list"""
    #     # list by method is creating list in random order, test fails every now and then
    #     expected_item_list = ['gold']
    #     expected_desc_words = ['coin', 'gold']
    #     self.assertEqual(get_all_desc_words(expected_item_list), expected_desc_words)

if __name__ == "__main":
    unittest.main()
