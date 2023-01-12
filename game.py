from itertools import repeat, product
from math import log2
import numpy as np
import random
import time
import copy
import matplotlib.pyplot as plt
from multiprocessing import Pool
from functools import partial

from lib.player import Player
from lib.constants import *
from lib.game import Game

def play_game(player_pair, mistake, rounds):
    player1, player2 = player_pair
    game = Game(player1, player2, mistake, rounds)
    game.play_game()
    p1 = (player1.index, game.p1['score'])
    p2 = (player2.index, game.p2['score'])
    return (p1, p2)

def play_all(population, mistake, rounds):

    for player in population:
        player.score = 0

    player_pairs = list(product(population, repeat=2))

    with Pool(8) as pool:
        play = partial(play_game, mistake=mistake, rounds=rounds)
        chunksize = len(player_pairs) // 8
        players_and_scores = list(pool.map(play, player_pairs, chunksize))

    for i in players_and_scores:
        for player_index, score in i:
            population[player_index].score += score

    return population


# Lattice play
# ------------

def play_lattice(lat, mistake, rounds):    
    n = len(lat)

    for i in range(n):
        for j in range(n):
            lat[i][j].score = 0

    player_pairs = []
    for i in range(n):
        for j in range(n):
            player = lat[i][j]
            for ni, nj in neighborhood(i, j, n, n):
                neighba = lat[ni][nj]
                player_pairs.append((player, neighba))

    with Pool(8) as pool:
        play = partial(play_game, mistake=mistake, rounds=rounds)
        chunksize = len(player_pairs) // 8
        game_results = list(pool.map(play, player_pairs, chunksize))

    for game_result in game_results:
        for player_index, score in game_result:
            px, py = player_index
            lat[px][py].score += score

    return lat


def init_square_lattice(N, choose_random=True):
    player_types = []
    for combination in product(ALL_ACTIONS, repeat=len(ALL_ACTIONS)):
        strat = dict(zip(ALL_ACTIONS, combination))
        player_types += [Player(strat, init) for init in ALL_ACTIONS]

    lattice = []
    last_ind = -1

    for i in range(N):
        lattice.append([])
        for j in range(N):
            if choose_random:
                ind = np.random.choice(range(len(player_types)))
            else:
                ind = (last_ind + 1) % len(player_types)
                last_ind = ind
            
            player = copy.deepcopy(player_types[ind])
            player.index = (i,j)
            lattice[i].append(player)

    return lattice
# ------------

def init_population(N: int) -> list[Player]:
    """ Initialize the population with an equal number of all M=1 strategies.
    """

    # Create list of all possible strategies
    player_types = []
    for combination in product(ALL_ACTIONS, repeat=len(ALL_ACTIONS)):
        strat = dict(zip(ALL_ACTIONS, combination))
        player_types += [Player(strat, init) for init in ALL_ACTIONS]

    # Create the population
    population = []
    for player_type in player_types:
        population += [copy.deepcopy(player_type) for _ in range(N)]

    for index, player in enumerate(population):
        player.index = index

    return population

def select_one(players: list) -> Player:
    scores = [p.score for p in players]
    if sum(scores) == 0:
        return random.choices(players)[0]
    else:
        return random.choices(players, weights=scores)[0]

def select_all(population):
    """ Selects new population randomely from winners """
    new_population = [select_one(population) for _ in range(len(population))]

    return new_population

def select_lattice(population):

    n = len(population)
    new_population = []
    for i in range(n):
        new_population.append([])
        for j in range(n):
            neighbor_inds = neighborhood(i, j, n, n)
            neighbors_and_me_inds = neighbor_inds + [(i, j)]
            neighbors_and_me = list(map(lambda x: population[x[0]][x[1]], neighbors_and_me_inds))
            new_population[i].append(select_one(neighbors_and_me))

    return new_population

def neighborhood(i, j, n, m):

    right = ((i + 1) % n, j)
    left = ((i - 1) % n, j)
    up = (i, (j + 1) % m)
    down = (i, (j - 1) % m)

    if i != 0 and j != 0:
        return [down, right]
    elif i != 0:
        return [down, right, up]
    elif j != 0:
        return [down, right, left]
    else:
        return [down, right, left, up]

def duplicate(player: Player, max_len) -> Player:

    if player.memory_size < max_len:

        new_strategy = {}
        for key, value in player.strategy.items():
            for action in ALL_ACTIONS:
                new_strategy[(action+key)] = value

        player.strategy = new_strategy
        player.memory_size += 1
        player.initial_state = random.choice(ALL_ACTIONS) + player.initial_state

        return player
    else: 
        return player

def point_mutation(player: Player, mut: float) -> Player:
    # mutate actions
    for key, b in player.strategy.items():
        if random.random() < mut:
            player.strategy[key] = not_action(b)
    #  mutate initial state
    for i in range(len(player.initial_state)):
        if random.random() < mut:
            new_init_state = list(player.initial_state)
            new_init_state[i] = not_action(new_init_state[i])
            player.initial_state = ''.join(new_init_state)

    return player

def split(player: Player) -> Player:
    if player.memory_size == 1:
        return player
    else:
        new_strat = {}
        s = player.strategy
        keys = list(s.keys())

        n_actions = len(ALL_ACTIONS)
        start_idx = random.randint(0,(n_actions-1))
        
        # strart at one random position and keep every nth element
        for key in keys[start_idx::n_actions]:
            new_strat[key[1:]] = s[key]

        player.strategy = new_strat
        # remove first character in initial state
        player.initial_state = player.initial_state[1:]
        player.memory_size -= 1

        return player

def mutate_all(population, mut, max_len):
    new_population = []
    for player in population:
        new_player = copy.deepcopy(player)
        if random.random() < mut:
            new_player = duplicate(new_player, max_len)
        new_player = point_mutation(new_player, mut)
        if random.random() < mut:
            new_player = split(new_player)

        new_population.append(new_player)
    return new_population

def mutate_lattice(population, mut, max_len):
    new_population = []
    n = len(population)
    for i in range(n):
        new_population.append([])
        for j in range(n):
            player = population[i][j]
            new_player = copy.deepcopy(player)
            if random.random() < mut:
                new_player = duplicate(new_player, max_len)
            new_player = point_mutation(new_player, mut)
            if random.random() < mut:
                new_player = split(new_player)

            new_population[i].append(new_player)
    return new_population

def strat_to_string(gene_dict: dict) -> str:
    """ Converts a dict into a string of actions like 'ccdc' """
    actions = gene_dict.values()
    return ''.join(actions)


def count_strategies_all(population):
    strats = [strat_to_string(player.strategy) for player in population]
    strats, counts = np.unique(strats, return_counts=True)
    ind = np.argsort(-counts)
    return strats[ind], counts[ind]

def count_strategies_lattice(population):
    strats = []
    n = len(population)
    for i in range(n):
        for j in range(n):
            strat = population[i][j].strategy
            strats.append(strat_to_string(strat))
    strats, counts = np.unique(strats, return_counts=True)
    ind = np.argsort(-counts)
    return strats[ind], counts[ind]

def print_strategies(strats, counts):
    print("🥬 strategies: ", strats, counts)

def generate_history(i, history, present_strategies, strats, counts):
    
    for j, strat in enumerate(strats):

        if strat in present_strategies:
            idx = present_strategies.index(strat)
            history[idx] = [*history[idx], *[counts[j]]]
        else:
            pad = list((-1)*np.ones(i+1,dtype=int))
            history.append([*pad,*[counts[j]]])
            present_strategies.append(strat)
                
    for dict in present_strategies:
        if dict not in strats: 
            idx = present_strategies.index(dict)
            history[idx] = [*history[idx], *[0]]
    
    return history, present_strategies

if __name__ == "__main__":

    population_size = 100
    generations = 10

    rounds = 10
    mistake = 0.01
    mut = 0.01

    max_len = 4

    mode = 'lattice'
    if mode == 'lattice':
        population = init_square_lattice(population_size)
        selection = select_lattice
        playing = play_lattice
        mutate = mutate_lattice
        count_strategies = count_strategies_lattice
    elif mode == 'all':
        population = init_population(population_size)
        selection = select_all
        playing = play_all
        mutate = mutate_all
        count_strategies = count_strategies_all

    present_strategies, history = count_strategies(population)
    print_strategies(present_strategies, history)
    history = [[k] for k in history]
    present_strategies = list(present_strategies)
    fig, ax = plt.subplots(figsize=(10, 6))

    for i in range(generations):
        start_time = time.time()
        print("Generation", i)
        population = playing(population, mistake, rounds)
        population = selection(population)
        population = mutate(population, mut, max_len)

        strats, counts = count_strategies(population)
        print_strategies(strats, counts)
        history, present_strategies = generate_history(i,history, present_strategies,strats,counts)

        dt = time.time() - start_time
        print(f"⏱️: {dt:2f} [s]")
    
    for n, strat in enumerate(history):
        if n < 10:
            ax.plot(range(generations+1), strat, label=present_strategies[n])
        else:
            ax.plot(range(generations+1), strat)

    ax.set_xlabel('Generation')
    ax.set_ylabel('# players with strategy')
    ax.set_xlim(0)
    ax.set_ylim(0)

    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.savefig('strategy_history.png')

    print("🏁 Fin")
