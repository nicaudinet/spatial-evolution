import numpy as np
import random
from lib.player import Player
from lib.constants import *

class Game:
    def __init__(self, player1, player2, mistake, rounds):
        self.p1 = { 'player': player1, 'history': player1.initial_state, 'score': 0 }
        self.p2 = { 'player': player2, 'history': player2.initial_state, 'score': 0 }
        self.mistake = mistake
        self.rounds = rounds

        self.scores = np.array([
            [[R,R],  [S,T],  [L,L],],
            [[T,S],  [P,P],  [L,L],],
            [[L,L],  [L,L],  [L,L],],
        ])

        self.action_idx_map = {
            'c': 0,
            'd': 1,
            'a': 2,
        }
    
    def update(self, action1, action2):
        """ Evaluate the history of the two players for Prisoner's Dilemma,
        where:
                  a2
                C    D    A
        a1  C  R,R  S,T  L,L
            D  T,S  P,P  L,L
            A  L,L  L,L  L,L
            """

        self.p1['history'] += action1 + action2
        self.p2['history'] += action2 + action1

        a1_idx = self.action_idx_map[action1]
        a2_idx = self.action_idx_map[action2]

        self.p1['score'] += self.scores[a1_idx, a2_idx, P1]
        self.p2['score'] += self.scores[a1_idx, a2_idx, P2]

    def play_turn(self, p):
        """ Play a single turn for a single player with some probability of a
        mistake happening """
        strategy = p['player'].strategy
        m = p['player'].memory_size
        assert len(p['history']) >= m
        prev_actions = p['history'][-m:]
        action = strategy[prev_actions]
        if random.random() < self.mistake:
            return not_action(action)
        else:
            return action

    def play_game(self):
        """ Play a game between two players from start to finish """
        for _ in range(self.rounds):
            action1 = self.play_turn(self.p1)
            action2 = self.play_turn(self.p2)
            self.update(action1, action2)
