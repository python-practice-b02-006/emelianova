import numpy as np
import pygame as pg
from random import randint, gauss

SCREEN_SIZE = (900, 600)
SCREEN_COLOR = (0, 33, 55)
GOLD = (255, 215, 0)
SILVER = (192, 192, 192)
MIN_GUN_LEN = 10
MAX_GUN_LEN = 50

TARGET_COLORS = ((255, 0, 0), (0, 0, 255), (255, 255, 110), (255, 0, 255),
                (0, 255, 255), (0, 255, 0), (250, 250, 210), (128, 0, 128), 
                (169, 32, 62), (119, 221, 119), (251, 96, 72))


class Ball():
    
    def __init__(self, rad=18, vel=[0,0]):
        self.coord = []
        self.color = SILVER
        self.rad = rad
        self.vel = vel
    
    
    def draw(self, screen):
        pg.draw.circle(screen, self.color, self.coord, self.rad)
        
    def flip_vel(self, axis, coef_perp=0.7, coef_par=0.95):
        vel = np.array(self.vel)
        n = np.array(axis)
        n = n / np.linalg.norm(n)
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
        
    def move(self, t_step=1., a=0.7):
        for i in range(2):
            self.coord[i] += int(self.vel[i] * t_step)
        self.vel[1] += a * t_step
        self.check_walls()

class Gun():
    
    def __init__(self, alpha=0, leng=MIN_GUN_LEN):
        self.coord = [30, SCREEN_SIZE[1]//2]
        self.angle = alpha
        self.length = leng
        self.active = False
    
    def draw(self, screen, width=10):
        end_coord = [self.coord[0] + self.length*np.cos(self.angle), 
                     self.coord[1] + self.length*np.sin(self.angle)]
        pg.draw.line(screen, GOLD, self.coord, end_coord, width)


    def set_angle(self, mouse_pos):
        self.angle = np.arctan2(mouse_pos[1] - self.coord[1], 
                                mouse_pos[0] - self.coord[0])
        
    def strike(self, coef=0.7):
        new_ball = Ball()
        new_ball.coord = self.coord.copy()
        new_ball.vel = [self.length*np.cos(self.angle)*coef,
                        self.length*np.sin(self.angle)*coef]
        
        self.active = False  
        self.length = MIN_GUN_LEN
        return new_ball
        
    def move(self, step=0.7):
        if self.active == True and self.length < MAX_GUN_LEN:
            self.length += step
        
        
class Target():
    
    def __init__(self, radius=35):
        coord_x = gauss(SCREEN_SIZE[0]//2, 250)
        coord_y = gauss(SCREEN_SIZE[1]//2, 200)
        rad = gauss(radius, 10)
        while coord_x > SCREEN_SIZE[0] - 30 or coord_x < 30:
            coord_x = (coord_x + SCREEN_SIZE[0]//2)//2
        while coord_y > SCREEN_SIZE[1] - 30 or coord_y < 30:
            coord_y = (coord_y + SCREEN_SIZE[1]//2)//2
        while rad < 13:
            rad += 5
        self.coord = [int(coord_x), int(coord_y)]
        self.rad = int(rad)
        self.color = TARGET_COLORS[randint(0, len(TARGET_COLORS) - 1)]
        
    def draw(self, screen):
        pg.draw.circle(screen, self.color, self.coord, self.rad)    
    
    
                               
class Table():
    pass

class Manager():
    
    def __init__(self):
        self.gun = Gun()
        self.score = Table()
        self.balls = []
        self.targets = []
        for i in range(3):
            self.targets.append(Target())
        
    def draw(self, screen):
        screen.fill(SCREEN_COLOR)
        self.gun.draw(screen)
        for ball in self.balls:
            ball.draw(screen)
        for targ in self.targets:
            targ.draw(screen)
        
        
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
            elif event.type == pg.MOUSEBUTTONDOWN:
                 if event.button == 1:
                    self.gun.active = True
            elif event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:
                    self.balls.append(self.gun.strike())
        if pg.mouse.get_focused():
            mouse_pos = pg.mouse.get_pos()
            self.gun.set_angle(mouse_pos)
            
        return done
        
    def remove_balls(self):
        count = 0
        for ball in self.balls:
            if (ball.vel[0]**2 + ball.vel[1]**2) < 1 and (ball.coord[1] + 2*ball.rad) > SCREEN_SIZE[1]:
                self.balls.pop(count)
                count -= 1
            count += 1
            
    def add_targets(self, n=3):
        for i in range(n):
            self.targets.append(Target())
            
    def remove_targets(self):
        count = 0
        for targ in self.targets:
            for ball in self.balls:
                dist = np.sqrt((ball.coord[0]-targ.coord[0])**2 + 
                               (ball.coord[1]-targ.coord[1])**2)
                if dist < targ.rad + ball.rad:
                    self.targets.pop(count)
                    count -= 1
            count += 1
        if len(self.targets) == 0:
            self.add_targets()
            
    def process(self, events, screen):
        done = self.handle_events(events)
        self.move()
        return done
    
    def move(self):
        for ball in self.balls:
            ball.move()
        self.remove_balls()
        self.remove_targets()
        self.gun.move()

        
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