import pygame
from game import *
import matplotlib.pyplot as plt

def update(population, history, present_strategies, generation):
    start_time = time.time()
    population = play_lattice(population, mistake, rounds)
    population = select_lattice(population)
    population = mutate_lattice(population, mut, max_len)

    strats, counts = count_strategies_lattice(population)
    #  print_strategies(strats, counts)
    history, present_strategies = generate_history(generation, history,
            present_strategies, strats,counts)
    dt = time.time() - start_time
    print(f"⏱️: {dt:2f} [s]")
    return population, history, present_strategies

def get_color(colors, strategy):
    name = strat_to_string(strategy)
    if name in colors:
        return colors[name]
    else:
        r = random.randint(0,255)
        g = random.randint(0,255)
        b = random.randint(0,255)
        colors[name] = (r, g, b)
        return colors[name]

def draw(canvas, population, colors, cell_size):
    n = len(population)
    for i in range(n):
        for j in range(n):
            color = get_color(colors, population[i][j].strategy)
            x = j * cell_size
            y = i * cell_size
            rect = pygame.Rect(x, y, cell_size, cell_size)
            pygame.draw.rect(canvas, color, rect)

def draw_legend(canvas, population, colors, font, cell_size):
    n = len(population)
    strategies = []
    for i in range(n):
        for j in range(n):
            strategies.append(strat_to_string(population[i][j].strategy))
    strats, counts = np.unique(strategies, return_counts=True)
    ind = np.argsort(-counts)
    strats = strats[ind]
    counts = counts[ind]
    counter = 0
    tile_size = 20
    width_rect = n * cell_size + 20
    width_text = width_rect + tile_size + 10
    for strat, count in zip(strats, counts):
        height = counter * (tile_size + 10) + 20
        rect = pygame.Rect(width_rect, height, tile_size, tile_size)
        pygame.draw.rect(canvas, colors[strat], rect)
        display_text = str(count).rjust(5, " ") + " - " + strat
        text = font.render(display_text, False, (255,255,255))
        canvas.blit(text, (width_text, height))
        counter += 1

######################################
# Config

population_size = 100

rounds = 50
mistake = 0.01
mut = 0.01

max_len = 2

FPS = 11

CELL_SIZE = 10
LEGEND_SIZE = 300
FONT_SIZE = 20
WINDOW_HEIGHT = population_size * CELL_SIZE
WINDOW_WIDTH = population_size * CELL_SIZE + LEGEND_SIZE

######################################
# Main

pygame.init()
pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', FONT_SIZE)

clock = pygame.time.Clock()
canvas = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Prisoner's Lattice")
animate = True
exit = False

population = init_square_lattice(population_size)
colors = {}

present_strategies, history = count_strategies_lattice(population)
history = [[k] for k in history]
present_strategies = list(present_strategies)
fig, ax = plt.subplots(figsize=(10, 6))

generation = 0

strats, counts = count_strategies_lattice(population)
#  print_strategies(strats, counts)

while not exit:

    clock.tick(FPS)

    if animate:
        canvas.fill((0,0,0))
        population, history, present_strategies = update(population, history,
                present_strategies, generation)
        draw(canvas, population, colors, CELL_SIZE)
        draw_legend(canvas, population, colors, font, CELL_SIZE)
        generation += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True
        if event.type == pygame.KEYDOWN:
            if event.unicode == 'q':
                exit = True
            if event.unicode == ' ':
                animate = not animate
            if event.key == 1073741906: # Up arrow
                FPS = min(61, FPS + 5)
            if event.key == 1073741905: # Down arrow
                FPS = max(1, FPS - 5)

    pygame.display.update()

# sort history
np_hist = np.array(history)
np_hist_sum = np.sum(np_hist, axis=1)
sorted_inds = np.argsort(-np_hist_sum)

for i, n in enumerate(sorted_inds):
    if i < 10:
        ax.plot(range(generation+1), history[n], label=present_strategies[n])
    else:
        ax.plot(range(generation+1), history[n])

ax.set_xlabel('Generation')
ax.set_ylabel('# players with strategy')
ax.set_xlim(0)
ax.set_ylim(0)

plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.savefig('strategy_history_lattice.png')

print("🏁 Fin")
