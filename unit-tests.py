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
        player1 = Player(strat1, 'c')
        result1 = split(player1)
        self.assertEqual(result1.strategy, player1.strategy)
        self.assertEqual(result1.initial_state, player1.initial_state)
        strat2 = {
            'cc': 'c',
            'dc': 'd',
            'cd': 'd',
            'dd': 'd',
        }
        player2 = Player(strat2, 'cc')
        player2.memory_size = 2
        expected2= {
            'c': 'd',
            'd': 'd',
        }
        exp_player2 = Player(expected2, 'c')
        random.seed(0)
        results2 = split(player2)
        self.assertEqual(results2.strategy, exp_player2.strategy)
        self.assertEqual(results2.initial_state, exp_player2.initial_state)
        self.assertEqual(results2.memory_size, 1)

    def test_point_mutation(self):
        strat = {
            'cc': 'c',
            'dc': 'd',
            'cd': 'd',
            'dd': 'd',
        }
        player = Player(strat, 'c')
        result1 = point_mutation(player, mut=0)
        self.assertEqual(result1.strategy, player.strategy)
        self.assertEqual(result1.initial_state, player.initial_state)

        expected1 = {
            'cc': 'd',
            'dc': 'c',
            'cd': 'c',
            'dd': 'c',
        }
        exp_player1 = Player(expected1, 'd')
        result2 = point_mutation(player, mut=1)
        self.assertEqual(result2.strategy, exp_player1.strategy)
        self.assertEqual(result2.initial_state, exp_player1.initial_state)

        expected2 = {
            'cc': 'd',
            'dc': 'c',
            'cd': 'd',
            'dd': 'd',
        }
        np.random.seed(0)
        random.seed(0)
        exp_player2 = Player(expected2, 'd')
        result3 = point_mutation(player, mut=0.5)
        self.assertEqual(result3.strategy, exp_player2.strategy)
        self.assertEqual(result3.initial_state, exp_player2.initial_state)

    def test_duplicate(self):
        max_len = 10
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
        player1 = Player(strat, 'cc')
        player1.memory_size = 2
        exp_player1 = Player(expected, 'dcc')
        exp_player1.memory_size = 3
        np.random.seed(0)
        random.seed(0)
        result = duplicate(player1, max_len)
        self.assertEqual(result.strategy, exp_player1.strategy)
        self.assertEqual(result.initial_state, exp_player1.initial_state)
        self.assertEqual(result.memory_size, exp_player1.memory_size)

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
        player2 = Player(strat2, 'ccd')
        player2.memory_size = 3
        exp_player2 = Player(expected2, 'dccd')
        exp_player2.memory_size = 4

        result2 = duplicate(player2, max_len)
        self.assertEqual(result2.strategy, exp_player2.strategy)
        self.assertEqual(result2.initial_state, exp_player2.initial_state)
        self.assertEqual(result2.memory_size, exp_player2.memory_size)

    def test_init_population(self):
        result = init_population(1)

        strategy_pool = [{'c': c, 'd': d} for c in [C,D] for d in [C,D]]

        expected = [Player(strat, init) for strat in strategy_pool for init in [C,D]]

        strategies = lambda pop: [p.strategy for p in pop]
        self.assertCountEqual(strategies(result), strategies(expected))

        initial_states = lambda pop: [p.initial_state for p in pop]
        self.assertCountEqual(initial_states(result), initial_states(expected))


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
