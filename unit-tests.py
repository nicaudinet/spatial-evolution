import numpy as np
import unittest
from main import *

class Test(unittest.TestCase):

    def test_init_population(self):
        result = init_population(1)
        expected = [[D,D],[C,D],[D,C],[C,C]]
        self.assertEqual(result.sort(), expected.sort())

    def test_duplicate(self):
        strat = [C,D]
        self.assertEqual(duplicate(strat), [C,D,C,D])

    def test_split(self):
        strat = [C,D]
        self.assertEqual(split(strat), strat)
        strat = [C,C,D,D]
        np.random.seed(0)
        self.assertEqual(split(strat), [D,D])

    def test_point_mutation(self):
        strat = [C,D,C,C,D,D,C,D]
        self.assertEqual(point_mutation(strat, mut=0), [C,D,C,C,D,D,C,D])
        self.assertEqual(point_mutation(strat, mut=1), [D,C,D,D,C,C,D,C])
        np.random.seed(0)
        self.assertEqual(point_mutation(strat, mut=0.5), [D,C,D,D,D,C,C,C])
        
    def test_find_index(self):
        self.assertEqual(find_index([D]), 0)
        self.assertEqual(find_index([C]), 1)
        self.assertEqual(find_index([D,D]), 0)
        self.assertEqual(find_index([C,D]), 1)
        self.assertEqual(find_index([D,C]), 2)
        self.assertEqual(find_index([C,C]), 3)
        self.assertEqual(find_index([D,D,D]), 0)

    def test_play_turn(self):
        strat = [D,C]
        history = [C]
        self.assertEqual(play_turn(strat, history, 0), C)
        self.assertEqual(play_turn(strat, history, 1), D)
        np.random.seed(0)
        self.assertEqual(play_turn(strat, history, 0.5), C)

    def test_eval(self):
        history = History()
        history.put(C,C)
        self.assertEqual(history.eval(), (3,3))
        history.put(D,D)
        self.assertEqual(history.eval(), (4,4))
        history.put(C,D)
        self.assertEqual(history.eval(), (4,9))
        history.put(D,C)
        self.assertEqual(history.eval(), (9,9))

    def test_put_show(self):
        history = History()
        history.put(C,D)
        self.assertEqual(history.show(1,P1), [D])
        self.assertEqual(history.show(1,P2), [C])
        self.assertEqual(history.show(2,P1), [D,C])
        self.assertEqual(history.show(2,P2), [C,D])
        history.put(C,D)
        self.assertEqual(history.show(2,P1), [D,C])
        self.assertEqual(history.show(2,P2), [C,D])
        self.assertEqual(history.show(4,P1), [D,C,D,C])
        self.assertEqual(history.show(4,P2), [C,D,C,D])

if __name__ == "__main__":
    unittest.main()
