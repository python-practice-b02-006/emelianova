import numpy as np
import pygame as pg
from random import randint, gauss

SCREEN_SIZE = (900, 600)
SCREEN_COLOR = (0,0,51)
GUN_COLOR = (204,136,0)
BALL_COLOR = (255,0,128)
TABLE_COLOR = (192, 192, 192)
WALL_COLOR = (255,255,0)
MIN_GUN_LEN = 10
MAX_GUN_LEN = 50

TARGET_COLORS = ((255,128,128), (255,191,128), (255,255,128), (191,255,128), 
                 (128,255,128), (128,255,191), (128,255,255), (128,191,255),
                 (128,128,255), (191,128,255), (255,128,255), (255,128,191))

class Ball():
    
    def __init__(self, rad=18, vel=[0,0]):
        self.coord = []
        self.color = BALL_COLOR
        self.rad = rad
        self.vel = vel
    
    
    def draw(self, screen):
        pg.draw.circle(screen, self.color, self.coord, self.rad)
        
        
    def flip_vel(self, axis, coef_perp=0.8, coef_par=0.85):
        vel = np.array(self.vel)
        n = np.array(axis)
        n = n / np.linalg.norm(n)
        vel_perp = vel.dot(n) * n
        vel_par = vel - vel_perp
        ans = -vel_perp * coef_perp + vel_par * coef_par
        self.vel = ans.astype(np.int).tolist()
        
        
    def check_corners(self):
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
        self.check_corners()

class Gun():
    
    def __init__(self, alpha=0, leng=MIN_GUN_LEN):
        self.coord = [30, SCREEN_SIZE[1]//2]
        self.angle = alpha
        self.length = leng
        self.active = False
    
    def draw(self, screen, width=16):
        coord1 = [self.coord[0] - width//2*np.sin(self.angle),
                  self.coord[1] + width//2*np.cos(self.angle)]
        coord2 = [self.coord[0] + width//2*np.sin(self.angle),
                  self.coord[1] - width//2*np.cos(self.angle)]
        end_coord1 = [self.coord[0] + self.length*np.cos(self.angle) - width//2*np.sin(self.angle), 
                     self.coord[1] + self.length*np.sin(self.angle) + width//2*np.cos(self.angle)]
        end_coord2 = [self.coord[0] + self.length*np.cos(self.angle) + width//2*np.sin(self.angle),
                     self.coord[1] + self.length*np.sin(self.angle) - width//2*np.cos(self.angle)]
        
        pg.draw.polygon(screen, GUN_COLOR, [coord1, coord2, end_coord2, end_coord1])

    def set_angle(self, mouse_pos):
        self.angle = np.arctan2(mouse_pos[1] - self.coord[1], 
                                mouse_pos[0] - self.coord[0])
        
    def strike(self, coef=0.6):
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
    
    def __init__(self, radius=30):
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

class Wall():
    
    def __init__(self, length=150):
        coord_x = gauss(SCREEN_SIZE[0]//2, 250)
        coord_y = gauss(SCREEN_SIZE[1]//2, 200)
        while coord_x > SCREEN_SIZE[0] - 50 or coord_x < 50:
            coord_x = (coord_x + SCREEN_SIZE[0]//2)//2
        while coord_y > SCREEN_SIZE[1] - 50 or coord_y < 50:
            coord_y = (coord_y + SCREEN_SIZE[1]//2)//2
        self.coord = [coord_x, coord_y]
        self.length = length
        self.angle = randint(0, 179)
        self.width = 12
        self.n = [+np.sin(self.angle), -np.cos(self.angle)]
        self.m = [-np.cos(self.angle), -np.sin(self.angle)]
    
    def draw(self, screen):
        coord1 = [self.coord[0] - self.length*np.cos(self.angle)//2 - self.width//2*np.sin(self.angle),
                  self.coord[1] - self.length*np.sin(self.angle)//2 + self.width//2*np.cos(self.angle)]
        coord2 = [self.coord[0] - self.length*np.cos(self.angle)//2 + self.width//2*np.sin(self.angle),
                  self.coord[1] - self.length*np.sin(self.angle)//2 - self.width//2*np.cos(self.angle)]
        end_coord1 = [self.coord[0] + self.length*np.cos(self.angle)//2 - self.width//2*np.sin(self.angle), 
                     self.coord[1] + self.length*np.sin(self.angle)//2 + self.width//2*np.cos(self.angle)]
        end_coord2 = [self.coord[0] + self.length*np.cos(self.angle)//2 + self.width//2*np.sin(self.angle),
                     self.coord[1] + self.length*np.sin(self.angle) //2- self.width//2*np.cos(self.angle)]
        
        pg.draw.polygon(screen, WALL_COLOR, [coord1, coord2, end_coord2, end_coord1])
        
                             
class Table():
    
    def __init__(self):
        self.coord = [SCREEN_SIZE[0]//2 - 90, 20]
        self.balls_used = 0
        self.targets_hit = 0
        self.score = 0
        
    def count(self):
        self.score = self.targets_hit*2 - self.balls_used
        
    def draw(self, screen, size=60):
        font = pg.font.Font(None, size)
        text_score = font.render("Score: " + str(self.score), False, TABLE_COLOR)
        screen.blit(text_score, self.coord)        


class Manager():
    
    def __init__(self, number_of_targets=3, number_of_walls=2):
        self.gun = Gun()
        self.table = Table()
        self.balls = []
        self.targets = []
        self.walls = []
        for i in range(number_of_targets):
            self.targets.append(Target())
        for i in range(number_of_walls):
            self.walls.append(Wall())
        
    def draw(self, screen):
        screen.fill(SCREEN_COLOR)
        self.gun.draw(screen)
        for ball in self.balls:
            ball.draw(screen)
        for targ in self.targets:
            targ.draw(screen)
        for wall in self.walls:
            wall.draw(screen)
        self.table.draw(screen)
        
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
                    self.table.balls_used += 1
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
            
    def add_targets(self, number_of_targets=3):
        for i in range(number_of_targets):
            self.targets.append(Target())
            
    def add_walls(self, number_of_walls=2):
        for i in range(number_of_walls):
            self.walls.append(Wall())
            
            
    def remove_targets(self):
        count = 0
        for targ in self.targets:
            for ball in self.balls:
                dist = np.sqrt((ball.coord[0] - targ.coord[0])**2 + 
                               (ball.coord[1] - targ.coord[1])**2)
                if dist < targ.rad + ball.rad:
                    self.table.targets_hit += 1
                    self.targets.pop(count)
                    count -= 1
            count += 1
            if len(self.targets) == 0:
                self.add_targets()
            
    def remove_walls(self, number_of_walls=2):
        for ball in self.balls:
            count = 0
            for wall in self.walls:
                delta_coord = [wall.coord[0] - ball.coord[0], 
                                wall.coord[1] - ball.coord[1]]
                dist = [delta_coord[0]*wall.n[0] + delta_coord[1]*wall.n[1], 
                        delta_coord[0]*wall.m[0] + delta_coord[1]*wall.m[1]]
                if  np.abs(dist[0]) < ball.rad + wall.width and np.abs(dist[1]) < wall.length//2 + wall.width: 
                    self.walls.pop(count)
                    count -= 1
                    if dist[0] >= 0:
                        ball.coord[0] = int((wall.coord[0] - 
                                            (wall.width + ball.rad)*np.sin(wall.angle)
                                            + dist[1]*np.cos(wall.angle)))
                        ball.coord[1] = int(wall.coord[1] +
                                            (wall.width + ball.rad)*np.cos(wall.angle)
                                            + dist[1]*np.sin(wall.angle))
                        ball.flip_vel(wall.n)
                    elif dist[0] < 0:
                        ball.coord[0] = int(wall.coord[0] + 
                                            (wall.width + ball.rad)*np.sin(wall.angle)
                                            + dist[1]*np.cos(wall.angle))
                        ball.coord[1] = int(wall.coord[1] -
                                            (wall.width + ball.rad)*np.cos(wall.angle)
                                            + dist[1]*np.sin(wall.angle))
                        ball.flip_vel([-wall.n[0], -wall.n[1]])
                count += 1
        if len(self.walls) <= 1:
            self.add_walls()
        
    def process(self, events, screen):
        done = self.handle_events(events)
        self.move()
        return done
    
    def move(self):
        for ball in self.balls:
            ball.move()
        self.remove_walls()
        self.remove_balls()
        self.remove_targets()
        self.table.count()
        self.gun.move()

pg.init()        
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