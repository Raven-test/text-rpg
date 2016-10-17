import unittest
# from testfixtures import Replacer
# from rpg import get_all_desc_words
from rpg import *


# https://pythonhosted.org/testfixtures/mocking.html

class TestTest(unittest.TestCase):

    # def test_move_direction(self):
    #     expected_text = "You cannot go in that direction"
    #     self.move_direction('w')
    
    def test_get_all_desc_words(self):
        """all items in list"""
        # list by method is created randomly, test fails every now and then
        expected_item_list = ['gold']
        expected_desc_words = ['coin', 'gold']
        self.assertEqual(get_all_desc_words(expected_item_list), expected_desc_words)

if __name__ == "__main":
    unittest.main()
