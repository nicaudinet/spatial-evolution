import pygame
from game import *

def update(population):
    population = play_lattice(population, mistake, rounds)
    population = select_lattice(population)
    population = mutate_lattice(population, mut, max_len)
    #  print_lattice_population(population)
    return population

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
    width_rect = n * cell_size + 20
    width_text = width_rect + cell_size + 10
    for strat, count in zip(strats, counts):
        height = counter * (cell_size + 10) + 20
        rect = pygame.Rect(width_rect, height, cell_size, cell_size)
        pygame.draw.rect(canvas, colors[strat], rect)
        display_text = str(count).rjust(5, " ") + " - " + strat
        text = font.render(display_text, False, (255,255,255))
        canvas.blit(text, (width_text, height + 5))
        counter += 1

population_size = 20

rounds = 100
mistake = 0.01
mut = 0.01

max_len = 2

FPS = 11

CELL_SIZE = 30
LEGEND_SIZE = 300
FONT_SIZE = 30
WINDOW_HEIGHT = population_size * CELL_SIZE
WINDOW_WIDTH = population_size * CELL_SIZE + LEGEND_SIZE

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

while not exit:

    clock.tick(FPS)

    if animate:
        canvas.fill((0,0,0))
        population = update(population)
        draw(canvas, population, colors, CELL_SIZE)
        draw_legend(canvas, population, colors, font, CELL_SIZE)

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
