from game import *
import matplotlib.pyplot as plt

init_group_size = 2
generations = 1

rounds = 10
mistake = 0.01
mut = 0.01

max_len = 4

if __name__ == '__main__':
    population = init_population(init_group_size)

    present_strategies, history = count_strategies_all(population)
    print_strategies(present_strategies, history)
    history = [[k] for k in history]
    present_strategies = list(present_strategies)
    fig, ax = plt.subplots(figsize=(10, 6))

    for i in range(generations):
        start_time = time.time()
        print("Generation", i)
        population = play_all(population, mistake, rounds)
        population = select_all(population)
        population = mutate_all(population, mut, max_len)

        strats, counts = count_strategies_all(population)
        print_strategies(strats, counts)
        history, present_strategies = generate_history(i, history,
                present_strategies, strats,counts)
        dt = time.time() - start_time
        print(f"⏱️: {dt:2f} [s]")

    # sort history
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
    plt.savefig('strategy_history_all.png')

    print("🏁 Fin")
