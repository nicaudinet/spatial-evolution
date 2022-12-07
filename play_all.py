from game import *

init_group_size = 2
generations = 100

rounds = 10
mistake = 0.01
mut = 0.01

max_len = 4

population = init_population(init_group_size)
for i in range(generations):
    start_time = time.time()
    print("Generation", i)
    population = play_all(population, mistake, rounds)
    population = select_all(population)
    population = mutate_all(population, mut, max_len)

    print_all_population(population)
    dt = time.time() - start_time
    print(f"⏱️: {dt:2f} [s]")

print("🏁 Fin")
