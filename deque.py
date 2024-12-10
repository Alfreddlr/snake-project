import random
from collections import deque
import pygame as pg

# Initialisation de Pygame
pg.init()

# Définition des variables (taille de l'écran + couleurs)
width, height, size = 20, 20, 20
blanc, noir, rouge, vert = (255, 255, 255), (0, 0, 0), (255, 0, 0), (0, 255, 0)
screen = pg.display.set_mode((width * size, height * size))
clock = pg.time.Clock()
running = True

# Initialisation de la tête, du corps et du fruit
tete = deque([(10, 15)])  # La tête est maintenant un deque
corps = deque([(11, 15), (12, 15), (13, 15)])  # Le corps est aussi un deque
mouv = [(0, 0)]
fruit = [(10, 10)]

# Fonction initialisant l'écran (fond blanc)
def init_screen():
    screen.fill(blanc)
    pg.display.update()

# Gère les événements du joueur
def handle_events(running):
    if running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_o:
                    running = False
                if (event.key == pg.K_z) and (mouv[-1] != (0, 1)):
                    mouv.append((0, -1))
                if (event.key == pg.K_s) and (mouv[-1] != (0, -1)):
                    mouv.append((0, 1))
                if (event.key == pg.K_q) and (mouv[-1] != (1, 0)):
                    mouv.append((-1, 0))
                if (event.key == pg.K_d) and (mouv[-1] != (-1, 0)):
                    mouv.append((1, 0))
    else:
        running = False

# Dessine le damier
def draw_grid():
    for x in range(width):
        for y in range(height):
            rect = pg.Rect(x * size, y * size, size, size)
            color = noir if (x % 2 == y % 2) else blanc
            pg.draw.rect(screen, color, rect)

# Dessine le fruit
def draw_fruit():
    fr = pg.Rect(fruit[-1][0] * size, fruit[-1][1] * size, size, size)
    pg.draw.rect(screen, vert, fr)

# Dessine la tête et le corps du serpent
def draw_tete():
    """Dessine la tête et le corps sur l'écran."""
    for segment in tete:
        rect = pg.Rect(segment[0] * size, segment[1] * size, size, size)
        pg.draw.rect(screen, rouge, rect)
    for segment in corps:
        rect = pg.Rect(segment[0] * size, segment[1] * size, size, size)
        pg.draw.rect(screen, rouge, rect)

# Met à jour la position du serpent
def move_tete():
    if len(mouv) > 1:
        corps.pop()  # Supprime la dernière cellule du corps
        corps.appendleft(tete[-1])  # Ajoute la position actuelle de la tête au corps
        tete_head = (tete[-1][0] + mouv[-1][0], tete[-1][1] + mouv[-1][1])
        tete.append(tete_head)  # Ajoute la nouvelle position de la tête
        tete.popleft()  # Supprime l'ancienne position de la tête

# Vérifie si le serpent mange un fruit
def check_fruit_collision():
    if tete[-1] == fruit[-1]:
        corps.append(corps[-1])  # Agrandit le corps
        u = (random.randint(0, width - 1), random.randint(0, height - 1))
        while u in tete or u in corps:
            u = (random.randint(0, width - 1), random.randint(0, height - 1))
        fruit.append(u)

# Vérifie les collisions du serpent
def check_collisions():
    global running
    if (tete[-1] in corps) or (not 0 <= tete[-1][0] < width) or (not 0 <= tete[-1][1] < height):
        running = False

# Boucle de jeu
init_screen()
while running:
    clock.tick(8)
    handle_events(running)
    draw_grid()
    draw_fruit()
    move_tete()
    draw_tete()
    check_fruit_collision()
    check_collisions()
    pg.display.update()

pg.quit()

