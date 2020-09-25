import pygame
from pygame.draw import *
BLACK = (0, 0, 0)
BLUE = (0, 0, 200)
pygame.init()

FPS = 30
screen = pygame.display.set_mode((400, 400))
pygame.display.set_caption("My first app window")

'''
rect(screen, (255, 0, 255), (100, 100, 200, 200))
rect(screen, (0, 0, 255), (100, 100, 200, 200), 5)
polygon(screen, (255, 255, 0), [(100,100), (200,50),
                               (300,100), (100,100)])
polygon(screen, (0, 0, 255), [(100,100), (200,50),
                               (300,100), (100,100)], 5)
circle(screen, (0, 255, 0), (200, 175), 50)
circle(screen, (255, 255, 255), (200, 175), 50, 5) '''

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
    screen.fill(BLACK)
    
    pygame.draw.line(screen, BLUE, [100, 50], [100, 150], 5)
    pygame.draw.lines(screen, BLUE, False, [[400, 50], [130, 150], [22, 85]], 5)
    pygame.draw.ellipse(screen, BLUE, [50, 30, 58, 19], 5)
    pygame.display.update()

pygame.quit()
