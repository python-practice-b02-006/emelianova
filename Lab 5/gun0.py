import numpy as np
import pygame as pg
from random import randint, gauss

SCREEN_SIZE = (600, 900)
SCREEN_COLOR = (0, 33, 55)
GOLD = (255, 215, 0)
SILVER = (192, 192, 192)

class Ball():
    pass

class Gun():
    
    def __init__(self, alpha=0, leng=30):
        self.coord = [30, SCREEN_SIZE[1]//2]
        self.angle = alpha
        self.length = leng
    
    def draw(self, width=10):
        end_coord = [self.coord[0] + self.length*np.cos(self.angle), 
                     self.coord[1] + self.length*np.sin(self.angle)]
        pg.draw.line(screen, GOLD, self.coord, end_coord, width)


    def set_angle(self, mouse_pos):
        self.angle = np.arctan2(mouse_pos[1] - self.coord[1], 
                                mouse_pos[0] - self.coord[0])
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
        self.gun.draw()
        
        
    def handle_events(self, events):
        done = False
        for event in events:
            if event.type == pg.QUIT:
                done = True
                
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    self.gun.coord[1] -= 5
                if event.key == pg.K_DOWN:
                    self.gun.coord[1] += 5      
        if pg.mouse.get_focused():
            mouse_pos = pg.mouse.get_pos()
            self.gun.set_angle(mouse_pos)
            
        return done
        
    def process(self, events, screen):
        done = self.handle_events(events)
        return done
    

        
screen = pg.display.set_mode(SCREEN_SIZE)
done = False
clock = pg.time.Clock()

mgr = Manager()

while not done:
    clock.tick(50)
    mgr.draw(screen)
    done = mgr.process(pg.event.get(), screen)
    pg.display.flip()
        

pg.quit()