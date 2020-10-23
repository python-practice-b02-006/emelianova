import numpy as np
import pygame as pg
from random import randint, gauss

SCREEN_SIZE = (600, 900)
SCREEN_COLOR = (0, 33, 55)

class Ball():
    pass

class Gun():
    pass

class Target():
    pass

class Table():
    pass

class Manager():
    
    def __init__(self):
        self.gun = Gun()
        self.score = Table()
        
    def draw(self, screen):
        screen.fill(SCREEN_COLOR)
        
        
    def handle_events(self, events):
        done = False
        for event in events:
            if event.type == pg.QUIT:
                done = True
        return done
        
    def process(self, events, screen):
        done = self.handle_events(events)
        return done
    

        
screen = pg.display.set_mode(SCREEN_SIZE)
done = False
clock = pg.time.Clock()

mgr = Manager()

while not done:
    clock.tick(15)
    done = mgr.process(pg.event.get(), screen)
    pg.display.flip()
        

pg.quit()
