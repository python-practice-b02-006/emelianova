import pygame
import numpy as np
from pygame.draw import *


pygame.init()

screen = pygame.display.set_mode([600, 402])

BLACK = (0, 0, 0)
ORANGE = (255, 160, 40)
PURPLE = (190, 70, 60)
PEACH = (255, 213, 170)
PURPLE_WHITE = (250, 214, 195)
YELLOW = (255, 255, 0)
VIOLET = (183, 131, 158)
DARK_VIOLET = (51, 0, 41)
BROWN = (51, 26, 0)
pygame.display.set_caption("Sea")

cloud1_coord = [60, 40, 5, 5]
cloud2_coord = [400, 40, 8, 10]
cloud3_coord = [200, 70, 6, 6]

ship1_coord = [140, 188, 1, 1]
ship2_coord = [320, 220, 2, 2]

birds_coordinates = [[427, 22, 30, 1], [40, 75, 32, 1], [357, 28, 25, 1]]

step_cloud_x = 1
step_cloud_y = 0.1
step_ship = 2
step_alpha = 1


done = False
clock = pygame.time.Clock()
pi = 3.141


def draw_ship(x, y, s, v):
    """
    Функция рисует корабль.

    Parameters
    ----------
    x : x координата кормы
    y : у координата кормы
    s : задает размеры корабля
    v : задает толщину линий прорисовки деталей корабля

    Returns
    -------
    None.

    """
    lsh = [[x, y]]
    r = 10 * s
    c = np.pi/20
    while c <= np.pi/2:
        lsh.append([x + r - r * np.cos(c), y + r * np.sin(c)])
        c += pi/20
    lsh.append([x + 7*r, y + r])
    lsh.append([x + 9*r, y])
    polygon(screen, (170, 50, 0), lsh)
    line(screen, (30, 30, 30), [x + 3*r, y], [x + 3*r, y - 4*r], v)
    polygon(screen, (180, 180, 180), [[x + 3*r, y - 4*r], [x + 3.75*r, y - 2*r],
                                      [x + 3*r, y], [x + 5.25*r, y - 2*r]])
    polygon(screen, (30, 30, 30), [[x + 3*r, y - 4*r], [x + 3.75*r, y - 2*r],
                                   [x + 3*r, y], [x + 5.25*r, y - 2*r]], 1)
    line(screen, (30, 30, 30), [x + 3.75*r, y - 2*r], [x + 5.25*r, y - 2*r], 1)
    circle(screen, (20, 20, 20), [x + 7*r + 5*s, y + 4*s], 3*s)
    circle(screen, (255, 255, 255), [x + 7*r + 5*s, y + 4*s], 2*s)
    line(screen, (30, 30, 30), [x + r, y], [x + r, y + r])
    line(screen, (30, 30, 30), [x + 7*r, y], [x + 7*r, y + r])
    

def draw_cloud(x, y, d, h):
    """
    Функция рисует облако.

    Parameters
    ----------
    x : x координата левого нижнего угла облака
    y : y координата левого нижнего угла облака
    d : длина ячейки облака
    h : высота ячейки обака

    Returns
    -------
    None.

    """
    ellipse(screen, (255, 255, 255), [x + 2*d, y, 4*d, 4*h])
    ellipse(screen, (180, 180, 180), [x + 2*d, y, 4*d, 4*h], 1)
    ellipse(screen, (255, 255, 255), [x + 4*d, y, 4*d, 4*h])
    ellipse(screen, (180, 180, 180), [x + 4*d, y, 4*d, 4*h], 1)
    ellipse(screen, (255, 255, 255), [x, y + 2*h, 4*d, 4*h])
    ellipse(screen, (180, 180, 180), [x, y + 2*h, 4*d, 4*h], 1)
    ellipse(screen, (255, 255, 255), [x + 3*d, y + 2*h, 4*d, 4*h])
    ellipse(screen, (180, 180, 180), [x + 3*d, y + 2*h, 4*d, 4*h], 1)
    ellipse(screen, (255, 255, 255), [x + 5*d, y + 2*h, 4*d, 4*h])
    ellipse(screen, (180, 180, 180), [x + 5*d, y + 2*h, 4*d, 4*h], 1)
    ellipse(screen, (255, 255, 255), [x + 6*d, y, 4*d, 4*h])
    ellipse(screen, (180, 180, 180), [x + 6*d, y, 4*d, 4*h], 1)
    ellipse(screen, (255, 255, 255), [x + 7*d, y + 2*h, 4*d, 4*h])
    ellipse(screen, (180, 180, 180), [x + 7*d, y + 2*h, 4*d, 4*h], 1)
        
    
def draw_sun(x, y, r, R):
    """
    Функция рисует солнце с центром (x, y), радиусом r. R задает радиус лимба.

    """
    ls = [[x + r, y]]
    a = np.pi/20 - np.pi/40 
    b = np.pi/20
    while a <= 2*np.pi:
        ls.append([x + R * np.cos(a), y + R * np.sin(a)])
        ls.append([x + r * np.cos(b), y + r * np.sin(b)])
        a += pi/20
        b += pi/20
    polygon(screen, (233, 255, 0), ls)
    
    
def draw_coast():
    """
    Функция рисует береговую линию

    Returns
    -------
    None.

    """
    i = 0
    while i <= 600:
        circle(screen, (233, 255, 0), (i, 309), 30)
        circle(screen, (59, 56, 255), (i + 30, 257), 30)
        i += 60
    line(screen, (100, 100, 100), [0, 283], [600, 283], 1)
        
    
def draw_bird(surface, x, y, alpha, color=BROWN, k=1):
    '''
    draws a bird on the surface
    Parameters
    ----------
    surface : pygame.surface
        the function draws the bird on it
    x : int
        x-coordinate of the lowest point of the bird
    y : int
        y-coordinate of the lowest point of the bird
    alpha : int
        angle of the bird's wings
    k : int, optional
        size parametr. The default is 1.
    color : tuple,  optional
        color in format fitting pygame.Color. The default is BROWN.


    Returns
    -------
    None.

    '''
    surface1 = pygame.Surface([int(32*k), int(8*k)], pygame.SRCALPHA)
    ellipse(surface1, color, [0, 0, int(32*k), int(20*k)])
    surface1_rot = pygame.transform.rotate(surface1, -alpha)
    screen.blit(surface1_rot, [x - int(10.5*k), y])
    
    surface2 = pygame.Surface([int(32*k), int(8*k)], pygame.SRCALPHA)
    ellipse(surface2, color, [0, 0, int(32*k), int(20*k)])
    surface2_rot = pygame.transform.rotate(surface2, alpha)
    surface.blit(surface2_rot, [x + int(10.5*k), y])
    
    
def draw_birds(surface, color, birds_coordinates):
    '''
    

    Parameters
    ----------
    surface : pygame.surface
        the function draws the birds on it
    color : tuple
        color in format fitting pygame.Color
        the color of the birds
    birds_coordinates : tuple of tuples
        the tuple contains tuples of (x_coordinate, y_coordinate, k)

    Returns
    -------
    None.

    '''
    for elem in (birds_coordinates):
        draw_bird(surface, elem[0], elem[1], elem[2], color=BROWN, k=elem[3])
        
        
def draw_umbrella(x, y, d): 
    """
    Функция рисует зонтик.

    Parameters
    ----------
    x : x координата основания зонтика
    y : y координата основания зонтика
    d : задает размер зонтика

    Returns
    -------
    None.

    """
    line(screen, (255, 149, 0), [x, y], [x, y - 30*d], d)
    polygon(screen, (255, 70, 100), [[x - 15*d, y - 25*d], [x + 15*d, y - 25*d], [x, y - 30*d]])
    
    line(screen, (60, 60, 60), [x, y - 30*d], [x - 12*d, y - 25*d])
    line(screen, (60, 60, 60), [x, y - 30*d], [x - 8*d, y - 25*d])
    line(screen, (60, 60, 60), [x, y - 30*d], [x - 4*d, y - 25*d])
    line(screen, (150, 150, 150), [x, y - 30*d], [x, y - 25*d])
    line(screen, (60, 60, 60), [x, y - 30*d], [x + 4*d, y - 25*d])
    line(screen, (60, 60, 60), [x, y - 30*d], [x + 8*d, y - 25*d])
    line(screen, (60, 60, 60), [x, y - 30*d], [x + 12*d, y - 25*d])
    

def move_ships(step):
    '''
    
    changes the coordinates of the ships
    
    Parameters
    ----------
    step : int
        step of the ship in pixels

    Returns
    -------
    None.

    '''
    draw_ship(ship1_coord[0], ship1_coord[1], ship1_coord[2],
               ship1_coord[3])
    draw_ship(ship2_coord[0], ship2_coord[1], ship2_coord[2],
               ship2_coord[3])
    
    ship1_coord[0] += step
    ship2_coord[0] += step
    
    if ship1_coord[0] > 600:
        ship1_coord[0] = -100
    if ship2_coord[0] > 600:
        ship2_coord[0] = -300
        
        
def move_clouds(step_x, step_y):
    '''
    changes the coordinates of the clouds
    
    Parameters
    ----------
    step_x : float
        step of the ship in pixels, x axis
    step_y : float
        step of the ship in pixels, y axis

    Returns
    -------
    None.

    '''
    draw_cloud(cloud1_coord[0], cloud1_coord[1], cloud1_coord[2],
               cloud1_coord[3])
    draw_cloud(cloud2_coord[0], cloud2_coord[1], cloud2_coord[2],
               cloud2_coord[3])
    draw_cloud(cloud3_coord[0], cloud3_coord[1], cloud3_coord[2],
               cloud3_coord[3])
    cloud1_coord[0] += step_x
    cloud1_coord[1] += step_y
    cloud2_coord[0] += step_x
    cloud2_coord[1] += step_y
    cloud3_coord[0] += step_x
    cloud3_coord[1] += step_y
    
    if cloud1_coord[0] > 600:
        cloud1_coord[0] = -50
        cloud1_coord[1] = 0
    if cloud2_coord[0] > 600:
        cloud2_coord[0] = -80
        cloud2_coord[1] = 0
    if cloud3_coord[0] > 600:
        cloud3_coord[0] = -80
        cloud3_coord[1] = -5


def move_birds(step):
    '''
    
    changes the angle of the bird's wings
    
    Parameters
    ----------
    step : float
        step of the angle betweeen bird's wings

    Returns
    -------
    None.

    '''
    
    draw_birds(screen, BROWN, birds_coordinates)
    for bird_coord in birds_coordinates:
        bird_coord[2] += step
    
    
def check_direction_birds(step_alpha):
    '''
    
    prevents the angle between the bird's wings from becoming more than 37 
    or less than 3 degrees
    
    Parameters
    ----------
    step_alpha : int
        step of the angle betweeen bird's wings

    Returns
    -------
    step_alpha : int
        returns the right step: plus or minus abs(step)

    '''
    
    if np.max(birds_coordinates, axis=0)[2] >= 37:
        step_alpha = -np.abs(step_alpha)
    elif np.min(birds_coordinates, axis=0)[2] <= 3:
        step_alpha = np.abs(step_alpha)
    return step_alpha
        
    
pygame.display.update()
clock = pygame.time.Clock()
finished = False
pygame.display.update()

while not finished:
    clock.tick(28)
    rect(screen, (140, 254, 243), (0, 0, 600, 183))
    rect(screen, (59, 56, 255), (0, 183, 600, 100))
    rect(screen, (233, 255, 0), (0, 283, 600, 119))
    draw_sun(530, 80, 40, 60)

    draw_coast()
    draw_umbrella(100, 370, 4)
    draw_umbrella(200, 340, 2)
    
    move_clouds(step_cloud_x, step_cloud_y)
    move_ships(step_ship)
    step_alpha = check_direction_birds(step_alpha)
    move_birds(step_alpha)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
    pygame.display.update()
    

pygame.quit()
