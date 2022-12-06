import numpy as np
import unittest
from main import *

class Test(unittest.TestCase):

    def test_strat_to_string(self):
        strat = {
            'cc': 'c',
            'dc': 'd',
            'cd': 'd',
            'dd': 'd',
        }
        expected = 'cddd'
        self.assertEqual(strat_to_string(strat), expected)

    def test_split(self):
        strat1 = {
            'c': C,
            'd': D,
        }
        self.assertEqual(split(strat1), strat1)
        strat2 = {
            'cc': 'c',
            'dc': 'd',
            'cd': 'd',
            'dd': 'd',
        }
        expected2_1 = {
            'c': 'c',
            'd': 'd',
        }
        expected2_2 = {
            'c': 'd',
            'd': 'd',
        }
        np.random.seed(0)
        self.assertEqual(split(strat2), expected2_1)
        np.random.seed(10)
        self.assertEqual(split(strat2), expected2_2)

    def test_point_mutation(self):
        strat = {
            'cc': 'c',
            'dc': 'd',
            'cd': 'd',
            'dd': 'd',
        }
        
        self.assertEqual(point_mutation(strat, mut=0), strat)
        expected1 = {
            'cc': 'd',
            'dc': 'c',
            'cd': 'c',
            'dd': 'c',
        }
        self.assertEqual(point_mutation(strat, mut=1), expected1)
        expected2 = {
            'cc': 'd',
            'dc': 'c',
            'cd': 'd',
            'dd': 'd',
        }
        np.random.seed(0)
        random.seed(0)
        self.assertEqual(point_mutation(strat, mut=0.5), expected2)

    def test_duplicate(self):
        strat = {
            'cc': 'c',
            'dc': 'd',
            'cd': 'd',
            'dd': 'c',
        }
        expected = {
            'ccc': 'c',
            'dcc': 'c',
            'cdc': 'd',
            'ddc': 'd',
            'ccd': 'd',
            'dcd': 'd',
            'cdd': 'c',
            'ddd': 'c',
        }
        self.assertEqual(duplicate(strat), expected)
        strat2 = {
            'ccc': 'd',
            'dcc': 'c',
            'cdc': 'd',
            'ddc': 'd',
            'ccd': 'd',
            'dcd': 'c',
            'cdd': 'd',
            'ddd': 'c',
        }
        expected2 = {
            'cccc': 'd',
            'dccc': 'd',
            'cdcc': 'c',
            'ddcc': 'c',
            'ccdc': 'd',
            'dcdc': 'd',
            'cddc': 'd',
            'dddc': 'd',
            'cccd': 'd',
            'dccd': 'd',
            'cdcd': 'c',
            'ddcd': 'c',
            'ccdd': 'd',
            'dcdd': 'd',
            'cddd': 'c',
            'dddd': 'c',
        }
        self.assertEqual(duplicate(strat2), expected2)

    def test_init_population(self):
        result = init_population(1)

        tft = {'strat': {'c': C,'d': D},'initial': C}
        all_coop = {'strat': {'c': C,'d': C}, 'initial': C}
        all_def = {'strat': {'c': D,'d': D}, 'initial': C}
        anti_tft = {'strat': {'c': D,'d': C}, 'initial': C}
        expected = [tft,all_coop,anti_tft, all_def]
        self.assertCountEqual(result, expected)

    def test_play_turn(self):
        strat = {
            'ccc': 'c',
            'dcc': 'c',
            'cdc': 'd',
            'ddc': 'd',
            'ccd': 'd',
            'dcd': 'd',
            'cdd': 'c',
            'ddd': 'c',
        }
        history = 'cdd'
        self.assertEqual(play_turn(strat, history, 0), C)
        self.assertEqual(play_turn(strat, history, 1), D)
        np.random.seed(0)
        random.seed(0)
        self.assertEqual(play_turn(strat, history, 0.5), C)

    def test_update_score(self):
        history = History()
        history.put(C,C)
        self.assertEqual((history.score1, history.score2), (3,3))
        history.put(D,D)
        self.assertEqual((history.score1, history.score2), (4,4))
        history.put(C,D)
        self.assertEqual((history.score1, history.score2), (4,9))
        history.put(D,C)
        self.assertEqual((history.score1, history.score2), (9,9))

    def test_not_action(self):
        c = 'c'
        d = 'd'
        self.assertEqual(not_action(c), d)
        self.assertEqual(not_action(d), c)

if __name__ == "__main__":
    unittest.main()
