from game import *
import matplotlib.pyplot as plt



######################################
# Config

# game
group_size = 10
generations = 30

rounds = 100
mistake = 0.#.01
mut = 0.#01

max_len = 2#4

# trials / getting stats
trials = 10
quasi_extict_limit = 3


######################################
# Functions

def play_game():
    population = init_population(group_size)

    present_strategies, history = count_strategies_all(population)
    # print_strategies(present_strategies, history)
    history = [[k] for k in history]
    present_strategies = list(present_strategies)
    fig, ax = plt.subplots(figsize=(10, 6))

    for i in range(generations):
        start_time = time.time()
        # print("Generation", i)
        population = play_all(population, mistake, rounds)
        population = select_all(population)
        population = mutate_all(population, mut, max_len)

        strats, counts = count_strategies_all(population)
        # print_strategies(strats, counts)
        history, present_strategies = generate_history(i, history,
                present_strategies, strats,counts)

        # how many are still present
        np_present_strategies = np.array(present_strategies)

        last_gen = np.array(history)[:,-1]
        last_strats = np_present_strategies[last_gen > quasi_extict_limit]
        n_present_strategies = len(last_strats)
        # print(f"n BIG strats: {n_present_strategies}")

        # dt = time.time() - start_time
        # print(f"⏱️: {dt:2f} [s]")

    return history, present_strategies

######################################
# Main

if __name__ == '__main__':
    all_last_strats = []

    for trial in range(trials):
        history, present_strategies = play_game()

        history = np.array(history)
        present_strategies = np.array(present_strategies)

        # check for dominant stategies
        hist_sum = np.sum(history, axis=1)

        last_gen = history[:,-1]

        last_strats = present_strategies[last_gen > quasi_extict_limit]
        all_last_strats.append(last_strats)
        print(f"finished trial {trial}: \nlast strats: {last_strats}")

    print("🏁 Fin")

    flat_strats = []

    for trial in all_last_strats:
        for x in trial:
            flat_strats.append(str(x))

    print(flat_strats)

    winner_strats_key, winner_strat_count = np.unique(flat_strats, return_counts=True)
    plt.bar(winner_strats_key, winner_strat_count)

    timestamp = str(int(time.time())) + '_mut_' + str(mut) + '_mist_' + str(mistake)
    plt.savefig(('winner_stats_all_'+timestamp+'.png'))

    filename = 'try_'+timestamp
    np.save((filename+'_strat_keys.npy'), winner_strats_key)
    np.save((filename+'_strat_counts.npy'), winner_strat_count)