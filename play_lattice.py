from game import *

population_size = 100
generations = 100

rounds = 10
mistake = 0.01
mut = 0.01

max_len = 4

population = init_square_lattice(population_size)
for i in range(generations):
    start_time = time.time()
    print("Generation", i)
    population = play_lattice(population, mistake, rounds)
    population = select_lattice(population)
    population = mutate_lattice(population, mut, max_len)

    print_lattice_population(population)
    dt = time.time() - start_time
    print(f"⏱️: {dt:2f} [s]")

print("🏁 Fin")
