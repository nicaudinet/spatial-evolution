import copy
import random

C = 'c' # Cooperate
D = 'd' # Defect
A = 'a' # Abstain

ALL_ACTIONS = [C,D,A]

# T > R > L > P > S
# to compare with prisoners dilemma
T = 5
R = 3
L = 2
P = 1
S = 0

P1 = 0
P2 = 1

def not_action(action):
    """ Returns another action """
    all_actions_copy = copy.deepcopy(ALL_ACTIONS)
    all_actions_copy.remove(action)
    return random.choice(all_actions_copy)
