import pygame
from pygame.draw import *


ORANGE = (255, 160, 40)
PURPLE = (190, 70, 60)
PEACH = (255, 213, 170)
PURPLE_WHITE = (250, 214, 195)
YELLOW = (255, 255, 0)
VIOLET = (183, 131, 158)

pygame.init()

FPS = 30
screen = pygame.display.set_mode((900, 600))

rect(screen, PEACH, (0, 0, 900, 600)) 
polygon(screen, PURPLE, [(0, 429), (0, 319), (155, 399), (197, 336), (261, 369),
                         (289, 290), (370, 309), (430, 354), (516, 335),
                         (656, 265), (693, 296), (737, 336), (775, 292), 
                         (814, 310), (830, 275), (869, 280), (900, 235),
                         (900, 429)])
ellipse(screen, PURPLE, (555, 253, 733, 377))
ellipse(screen, PEACH, (552, -339, 446, 657))
rect(screen, PURPLE_WHITE, (0, 130, 900, 130))    # the sky stripe
polygon(screen, PURPLE, [(746, 370), (737, 338), (775, 292), (814, 316),
                         (830, 289), (869, 293), (900, 241), (900, 429)])
circle(screen, PURPLE, (614, 334), 63)

surface = pygame.Surface([200, 100], pygame.SRCALPHA)
ellipse(surface, PURPLE, [0, 0, 204, 80])
surface_rot = pygame.transform.rotate(surface, 37)
screen.blit(surface_rot, [470, 230])


polygon(screen, ORANGE, [(5, 300), (12, 266), (143, 193), (185, 149),
                         (221, 156), (233, 175), (347, 251), (405, 242),
                         (439, 254), (481, 214), (522, 225), (541, 206),
                         (649, 134), (673, 139), (714, 177), (750, 168),
                         (809, 197), (838, 181), (900, 211)])
ellipse(screen, PURPLE, (21, 264, 138, 309))

ellipse(screen, PURPLE_WHITE, (437, -152, 219, 359))
ellipse(screen, PURPLE_WHITE, (-274, -327, 500, 596))
rect(screen, PEACH, (0, 0, 900, 129))

polygon(screen, ORANGE, [(166, 168), (185, 149), (221, 156), (233, 175)])
polygon(screen, ORANGE, [(673, 139), (714, 177), (655, 182)])
ellipse(screen, ORANGE, (624, 125, 61, 103))
ellipse(screen, ORANGE, (620, 130, 67, 96))
ellipse(screen, ORANGE, (617, 137, 73, 73))
ellipse(screen, ORANGE, (722, 173, 64, 53))

polygon(screen, VIOLET, [(0, 420), (900, 400), (900, 600), (0, 600)])
circle(screen, YELLOW, (440, 120), 54)     # the sun


pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
