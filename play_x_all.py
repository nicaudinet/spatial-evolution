from game import *
import matplotlib.pyplot as plt

######################################
# Config

# game
group_size = 10 # population size is group_size * 81
generations = 50

rounds = 20
mistake = 0.#.01
mut = 0.#01

max_len = 1#4

# trials / getting stats
trials = 50
quasi_extict_limit = 10

######################################
# Functions

def play_game(trial, timestamp):
    population = init_population(group_size)

    present_strategies, history = count_strategies_all(population)
    history = [[k] for k in history]
    present_strategies = list(present_strategies)
    fig, ax = plt.subplots(figsize=(10, 6))

    for i in range(generations):
        population = play_all(population, mistake, rounds)
        population = select_all(population)
        population = mutate_all(population, mut, max_len)

        strats, counts = count_strategies_all(population)
        history, present_strategies = generate_history(i, history,
                present_strategies, strats,counts)

    np_hist = np.array(history)
    np_hist_sum = np.sum(np_hist, axis=1)
    sorted_inds = np.argsort(-np_hist_sum)

    for i, n in enumerate(sorted_inds):
        if i < 10:
            ax.plot(range(generations+1), history[n], label=present_strategies[n])
        else:
            ax.plot(range(generations+1), history[n])

    ax.set_xlabel('Generation')
    ax.set_ylabel('# players with strategy')
    ax.set_xlim(0)
    ax.set_ylim(0)

    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.savefig('data/'+timestamp+'strategy_history_lattice_'+str(trial)+'.png')

    return history, present_strategies

######################################
# Main

if __name__ == '__main__':
    all_histories = []
    all_last_strats = []
    all_present_strategies = []

    timestamp = str(int(time.time())) + '_mut_' + str(mut) + '_mist_' + str(mistake) + '_rounds_' + str(rounds)

    for trial in range(trials):
        history, present_strategies = play_game(trial, timestamp)

        history = np.array(history)
        present_strategies = np.array(present_strategies)

        # check for dominant stategies
        hist_sum = np.sum(history, axis=1)
        last_gen = history[:,-1]
        last_strats = present_strategies[last_gen > quasi_extict_limit]

        all_last_strats.append(last_strats)
        all_histories.append(copy.deepcopy(history))
        all_present_strategies.append(copy.deepcopy(present_strategies))

        print(f"finished trial {trial}: \nlast strats: {last_strats}")

    print("🏁 Fin")

    flat_strats = []

    for trial in all_last_strats:
        for x in trial:
            flat_strats.append(str(x))

    print("strats: ", flat_strats)

    winner_strats_key, winner_strat_count = np.unique(flat_strats, return_counts=True)
    plt.bar(winner_strats_key, winner_strat_count)

    plt.savefig(('data/winner_stats_all_'+timestamp+'.png'))

    filename = 'data/try_'+timestamp

    results = {
        'last_strats': all_last_strats,
        'histories': all_histories,
        'present_strategies': all_present_strategies,
        'winner_strat_keys': winner_strats_key,
        'winner_strat_counts': winner_strat_count,
    }

    np.save((filename+'.npy'), results)