from game import *
import matplotlib.pyplot as plt

init_group_size = 5
generations = 1000
save_generations = 50

rounds = 100
mistake = 0.01
mut = 0.01

max_len = 1#4

def save_data(history, present_strategies, generations, timestamp):

    fig, ax = plt.subplots(figsize=(10, 6))

    # sort history
    np_hist = np.array(history)
    np_hist_sum = np.sum(np_hist, axis=1)
    sorted_inds = np.argsort(-np_hist_sum)

    for j, n in enumerate(sorted_inds):
        if j < 10:
            ax.plot(range(generations+1), history[n], label=present_strategies[n])
        else:
            ax.plot(range(generations+1), history[n])

    ax.set_xlabel('Generation')
    ax.set_ylabel('# players with strategy')
    ax.set_xlim(0)
    ax.set_ylim(0)


    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.savefig('./data/' + timestamp + '_' + str(generations) + '.png')

    filename = 'data/try_' + timestamp + '_' + str(generations)

    results = {
        'present_strategies': present_strategies,
        'histories': np_hist,
    }

    np.save((filename+'.npy'), results)

    print("saved to", filename)

if __name__ == '__main__':
    population = init_population(init_group_size)
    timestamp = str(int(time.time())) + '_opt_all_mut_' + str(mut) + '_mist_' + str(mistake) + '_rounds_' + str(rounds)

    present_strategies, history = count_strategies_all(population)
    print_strategies(present_strategies, history)
    history = [[k] for k in history]
    present_strategies = list(present_strategies)

    for i in range(generations):

        if i % save_generations == 0 and not i == 0:
            save_data(history, present_strategies, i, timestamp)

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

    save_data(history, present_strategies, generations, timestamp)
    print("🏁 Fin")
