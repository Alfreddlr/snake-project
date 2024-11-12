import random
import pygame as pg

# Initialisation de Pygame
pg.init()

# Définition des variables (taille de l'écran + couleurs)
# J'ai choisi de faire un damier carré de 20 cases, pour imiter davantage le vrai jeu
width, height, size = 20, 20, 20
blanc, noir, rouge, vert = (255, 255, 255), (0, 0, 0), (255, 0, 0), (0, 255, 0)
screen = pg.display.set_mode((400, 400))
clock = pg.time.Clock()
running = True

# Initialisation de la tête, du corps et du fruit
tete = [(10, 15)]
corps = [(11, 15), (12, 15), (13, 15)]
mouv = [(0, 0)]
fruit = [(10, 10)]

# Fonction initialisant l'écran (fond blanc)
def init_screen():
    screen.fill(blanc)
    pg.display.update()

#gère les évênements du joueur (soit il quitte la partie, soit il fait bouger la tête du serpent dans l'une des 4 directions)
def handle_events(running):
    if running ==True : 
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
    else : 
        running = False

#dessine le damier au-dessus du fond blanc
def draw_grid():
    for x in range(width):
        for y in range(height):
            rect = pg.Rect(x * size, y * size, size, size)
            color = noir if (x % 2 == y % 2) else blanc
            pg.draw.rect(screen, color, rect)

#fonction dessinant le fruit ("fruit" étant une liste répertoriant les positions des fruits placés sur le damier)
def draw_fruit():
    fr = pg.Rect(fruit[-1][0] * size, fruit[-1][1] * size, size, size)
    pg.draw.rect(screen, vert, fr)

#fonction dessinant la tête du serpent, et son corps
def draw_tete():
    """Dessine la tête et le corps sur l'écran."""
    for segment in tete:
        rect = pg.Rect(segment[0] * size, segment[1] * size, size, size)
        pg.draw.rect(screen, rouge, rect)
    for segment in corps:
        rect = pg.Rect(segment[0] * size, segment[1] * size, size, size)
        pg.draw.rect(screen, rouge, rect)

#lorsque le joueur bouge, la position de la tête se trouve modifiée
#cette fonction, à partir du premier déplacement, fonctionne de la façon suivante :
#le dernier carré du serpent (en bout de file) devient la position venant d'être quittée par la tête 
#tete_head prend les nouvelles coordonnées de la tête (à partir des anciennes, en rajoutant le dernier déplacement)
#de telle sorte que si l'on appuie sur une seule touche, tant qu'on n'appuie pas sur une nouvelle le serpent continue d'avancer dans une direction
def move_tete():
    if len(mouv) > 1:
        corps[-1] = tete[-1]
        tete_head = [(mouv[-1][0] + x, mouv[-1][1] + y) for x, y in tete]
        corps.insert(0, corps.pop())  # Déplace le corps
        tete[:] = tete_head  # Met à jour la tête

# vérifie si les coordonnées de la tête sont sur celles du fruit, auquel cas un nouveau fruit est rajouté
# pour rajouter un fruit, des tirages sont fait, jusqu'à ce que les coordonnées proposées soient différentes de celles occupées par le serpent tout entier
# lorsque le fruit est mangé, le serpent grossi
def check_fruit_collision():
    if tete[-1] == fruit[-1]:
        corps.append(corps[-1])  # Agrandit le corps
        u = (random.randint(0, width - 1), random.randint(0, height - 1))
        while u in tete or u in corps:
            u = (random.randint(0, width - 1), random.randint(0, height - 1))
        fruit.append(u)

# cette fonction vérifie si le serpent se mord la queue (tête arrive sur corps) ou si la tête cogne un des bords du plateau
# auquel cas, la partie s'arrête (running=False)
def check_collisions():
    global running
    if (tete[-1] in corps) or (not 0 <= tete[-1][0] < width) or (not 0 <= tete[-1][1] < height):
        running = False

# Boucle de jeu, dans l'ordre à chaque tour de jeu les évênements du joueur sont pris en compte
# puis le amier est dessiné, ensuite le fruit. La position de la tête est actualisé et le nouveau serpent dessiné. 
# ce dernier grossi si un fruit a été mangé (et alors un nouveau est placé sur le damier de jeu)
# on vérifie que la partie continue (le serpent ne s'est pas mordu la queue et n'a pas cogné un bord)
# enfin, on affiche l'image. Le jeu fonctionne donc par affichages successifs d'images, tant que la partie continue
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

# Quitter Pygame
pg.quit()

