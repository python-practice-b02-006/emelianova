import numpy as np
import pygame as pg
from random import randint, gauss

SCREEN_SIZE = (600, 900)
SCREEN_COLOR = (0, 33, 55)
GOLD = (255, 215, 0)
SILVER = (192, 192, 192)

class Ball():
    
    def __init__(self, rad=40, vel=[0,0]):
        self.coord = []
        self.color = SILVER
        self.rad = rad
        self.vel = vel
    
    def draw(self, screen):
        pg.draw.circle(screen, self.color, self.coord, self.rad)
        
    def flip_vel(self, axis, coef_perp=1.0, coef_par=1.0):
        vel = np.array(self.vel)
        n = np.array(axis)
        n = n / n.norm()
        vel_perp = vel*n
        vel_par = vel - vel_perp
        
        vel_perp = -vel_perp*coef_perp
        vel_par = vel_par*coef_par
        vel = vel_perp + vel_par
        
        self.vel = vel.astype(np.int).tolist()
        
        
        
    def check_walls(self):
        norm = [[1,0], [0,1]]
        for i in range(2):
            if self.coord[i] < self.rad:
                self.coord[i] = self.rad + 1
                self.flip_vel(norm[i])
            if self.coord[i] > -self.rad + SCREEN_SIZE[i]:
                self.coord[i] = -self.rad + SCREEN_SIZE[i] - 1
                self.flip_vel(norm[i])
        
    def move(self, t_step=1.):
        for i in range(2):
            self.coord[i] += int(self.vel[i] * t_step)
        self.check_walls()

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
        self.balls = []
        self.balls.append(Ball([100, 100], [10, 20]))
        
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
    
    def move(self):
        for ball in self.balls:
            ball.move()

        
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