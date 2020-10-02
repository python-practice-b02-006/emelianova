import pygame
from pygame.draw import *

BLACK = (0, 0, 0)
ORANGE = (255, 160, 40)
PURPLE = (190, 70, 60)
PEACH = (255, 213, 170)
PURPLE_WHITE = (250, 214, 195)
YELLOW = (255, 255, 0)
VIOLET = (183, 131, 158)
DARK_VIOLET = (51, 0, 41)
BROWN = (51, 26, 0)
birds_coordinates = ((345, 216, 1), (427, 223, 1), (425, 253, 1), (357, 280, 1),
                     (715, 433, 1), (614, 451, 1), (699, 482, 1.5), (564, 406, 1.3))
sun_coordinates =  ((440, 120), 54)


def draw_bird(surface, x, y, color=BROWN, k=1):
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
    surface1_rot = pygame.transform.rotate(surface1, -30)
    screen.blit(surface1_rot, [x - int(10.5*k), y])
    
    surface2 = pygame.Surface([int(32*k), int(8*k)], pygame.SRCALPHA)
    ellipse(surface2, color, [0, 0, int(32*k), int(20*k)])
    surface2_rot = pygame.transform.rotate(surface2, 30)
    surface.blit(surface2_rot, [x + int(10.5*k), y])
    
    
    
def first_mountains(surface, color=ORANGE):
    '''
    

    Parameters
    ----------
    surface : pygame.surface
        the function draws the mountains on it
    color : tuple,  optional
        color in format fitting pygame.Color. The default is ORANGE.

    Returns
    -------
    None.

    '''
    polygon(surface, color, [(5, 300), (12, 266), (143, 193), (185, 149),
                         (221, 156), (233, 175), (347, 251), (405, 242),
                         (439, 254), (481, 214), (522, 225), (541, 206),
                         (649, 134), (673, 139), (714, 177), (750, 168),
                         (809, 197), (838, 181), (900, 211)])
    polygon(surface, color, [(166, 168), (185, 149), (221, 156), (233, 175)])
    polygon(surface, color, [(673, 139), (714, 177), (655, 182)])
    ellipse(surface, color, (624, 125, 61, 103))
    ellipse(surface, color, (620, 130, 67, 96))
    ellipse(surface, color, (617, 137, 73, 73))
    ellipse(surface, color, (722, 173, 64, 53))


def second_mountains(surface, color=PURPLE):
    '''
    

    Parameters
    ----------
    surface : pygame.surface
        the function draws the mountains on it
    color : tuple,  optional
        color in format fitting pygame.Color. The default is PURPLE.

    Returns
    -------
    None.

    '''
    polygon(surface, color, [(0, 429), (0, 319), (155, 399), (197, 336), (261, 369),
                         (289, 290), (370, 309), (430, 354), (516, 335), (656, 265),
                         (693, 296),
                         (737, 336),
                         (775, 292), (814, 310), (830, 275), (869, 280), (900, 235),
                         (900, 429)])
    ellipse(surface, color, (21, 264, 138, 309))
    polygon(surface, color, [(746, 370), (737, 338), (775, 292), (814, 316),
                         (830, 289), (869, 293), (900, 241), (900, 429)])
    circle(surface, color, (614, 334), 63)

    surface1 = pygame.Surface([200, 100], pygame.SRCALPHA)
    ellipse(surface1, color, [0, 0, 204, 80])
    surface1_rot = pygame.transform.rotate(surface1, 37)
    screen.blit(surface1_rot, [470, 230])
    polygon(surface, color, [(746, 370), (737, 338), (775, 292), (814, 316),
                         (830, 289), (869, 293), (900, 241), (900, 429)])
    ellipse(screen, PURPLE, (21, 264, 138, 309))



def third_mountains(surface, color=DARK_VIOLET, background_color=VIOLET):
    '''
    

    Parameters
    ----------
    surface : pygame.surface
        the function draws the mountains on it
    color : tuple,  optional
        color in format fitting pygame.Color. The default is DARK_VIOLET.
    background_color : tuple,  optional
        color in format fitting pygame.Color. The default is VIOLET.

    Returns
    -------
    None.

    '''
    polygon(surface, color, [(0, 323), (105, 354), (193, 466), (283, 560),
                              (467, 575), (556, 509), (690, 547), (900, 396),
                              (900, 600), (0, 600)])

    ellipse(surface, background_color, (281, 514, 205, 75))
    surface1 = pygame.Surface([350, 130], pygame.SRCALPHA)
    ellipse(surface1, background_color, [0, -340, 330, 438])
    surface.blit(surface1, [517, 450])
    surface2 = pygame.Surface([350, 130], pygame.SRCALPHA)
    ellipse(surface2, color, [0, 0, 170, 270])
    surface.blit(surface2, [808, 377])


def draw_sun(surface, color, sun_coordinates):
    '''
    

    Parameters
    ----------
    surface : pygame.surface
        the function draws the msun on it
    color : tuple
        color in format fitting pygame.Color
    sun_coordinates : tuple
        the tuple contains a tuple (x_coordinate, y_coordinate), radius
        (x_coordinate, y_coordinate) of the centre of the sun
        radius of the sun

    Returns
    -------
    None.

    '''
    circle(surface, color, sun_coordinates[0], sun_coordinates[1]) 


def draw_background(surface, color1, color2, color3):
    '''


    Parameters
    ----------
    surface : pygame.surface
        the function draws the background on it
    color1 : tuple
        color in format fitting pygame.Color
        the main color
    color2 : tuple
        color in format fitting pygame.Color
        the color of the stripe
    color3 : tuple
        color in format fitting pygame.Color
        the color of the water

    Returns
    -------
    None.

    '''
    
    rect(surface, color1, (0, 0, 900, 600)) 

    ellipse(surface, color1, (552, -339, 446, 657))
    rect(surface, color2, (0, 130, 900, 130)) 
    rect(surface, color1, (0, 0, 900, 129))
    polygon(surface, color3, [(0, 420), (900, 400), (900, 600), (0, 600)])

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
        draw_bird(surface, elem[0], elem[1], color=BROWN, k=elem[2])


def main():
    '''
    the main function

    Returns
    -------
    None.

    '''
    draw_background(screen, PEACH, PURPLE_WHITE, VIOLET)
    first_mountains(screen, ORANGE)
    second_mountains(screen, PURPLE)
    third_mountains(screen, DARK_VIOLET, VIOLET)
    draw_sun(screen, YELLOW, sun_coordinates)
    draw_birds(screen, BROWN, birds_coordinates)
    
    
pygame.init()

FPS = 30
screen = pygame.display.set_mode((900, 600))

main()

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
