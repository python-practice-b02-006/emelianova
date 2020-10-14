import pygame
import numpy as np
from pygame.draw import *
from random import randint
pygame.init()

FPS = 50
screen = pygame.display.set_mode((1200, 700))
file = open('best_players.txt', 'a')
name = ''
global score
score = 0
DARK_BLUE = (0, 33, 55)  # background color
SILVER = (192, 192, 192)  # score color
GOLD = (255, 215, 0)  # superball color

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 110)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
LIME = (0, 255, 0)
BEIGE = (250, 250, 210)
PURPLE = (128, 0, 128)    
CARMINE = (169, 32, 62)
GREEN = (119, 221, 119)
ROSE = (251, 96, 72)

COLORS = [RED, BLUE, YELLOW, MAGENTA, CYAN, BEIGE, LIME, ROSE, PURPLE, CARMINE,
          GREEN]

n = 11

x_sup = 0
y_sup = 0
r1_sup = 18
r2_sup = 22
vr_sup = 0.05
vx_sup = 0
vy_sup = 0
superball_needed = False
superball_initiated = False

comment_needed = False
name_to_write = False
comment_count = 0

x = np.zeros(n, dtype=int)
y = np.zeros(n, dtype=int)
vx = np.zeros(n, dtype=int)
vy = np.zeros(n, dtype=int)
r = np.zeros(n, dtype=int)
color = []
for i in range(n):
    color.append(COLORS[i%(len(COLORS))])


def new_ball(i):
    '''
    creates a new ball at random coordinates x, y

    Returns
    -------
    None.

    '''
    global x, y, r, color
    x[i] = randint(100, 1100)
    y[i] = randint(100, 600)
    r[i] = randint(20, 40)
    vx[i] = randint(-10, 10)
    vy[i] = randint(-10, 10)
    circle(screen, color[i], (x[i], y[i]), r[i])
    
def new_balls(n):
    for i in range(n):
        new_ball(i)

def move_balls():
    '''
    changes the coordinates of usual balls

    Returns
    -------
    None.

    '''
    global x, y, r, vx, vy
    for i in range(n):
        if (x[i] + r[i]) > 1200 or (x[i] - r[i]) < 0 :
            vx[i] = - vx[i]
        if (y[i] + r[i]) > 700 or (y[i] - r[i]) < 0:
            vy[i] = - vy[i]
        x[i] += vx[i]
        y[i] += vy[i]
        circle(screen, color[i], (x[i], y[i]), r[i])
    

def check_click(event):
    '''
    checks if the player has catched a ball

    Parameters
    ----------
    event : pygame.MOUSECLICKBUTTON
        player's click

    Returns
    -------
    list of one string and maybe one int
    [0] - type of the ball that was catched
    [1] the number of the ball if list[0] == 'usual'

    '''
    ans = -1
    global n, x, y, r, x_sup, y_sup, r2_sup
    mouse_x, mouse_y = event.pos
    if (mouse_x - x_sup)**2 + (mouse_y - y_sup)**2 <= r2_sup:
        return ['super']
    for i in range(n):
        if (mouse_x - x[i])**2 + (mouse_y - y[i])**2 <= r[i]**2:
            ans = i
            return ['usual', ans]
    if ans == -1:
        return ['none']

def draw_sun(x, y, r, R):
    global GOLD
    """
    Функция рисует солнце с центром (x, y), радиусом r. R задает радиус лимба.
    """
    ls = [[x + r, y]]
    a = np.pi/6 - np.pi/12
    b = np.pi/6
    while a <= 2*np.pi:
        ls.append([x + R * np.cos(a), y + R * np.sin(a)])
        ls.append([x + r * np.cos(b), y + r * np.sin(b)])
        a += np.pi/6
        b += np.pi/6
    polygon(screen, GOLD, ls)

def new_superball():
    '''
     creates new superball

    Returns
    -------
    None.

    '''
    global x_sup, y_sup, r1_sup, r2_sup, vx_sup, vy_sup
    x_sup = randint(100, 1100)
    y_sup = randint(100, 600)
    r1_sup = 20
    r2_sup = 24
    vx_sup = (-1)^(randint(1, 2))*randint(1, 1)
    vy_sup = (-1)^(randint(1, 2))*randint(1, 1)
    draw_sun(x_sup, y_sup, r1_sup, r2_sup)
        
    
def move_superball():
    '''
    changes the coordinates of the superball

    Returns
    -------
    None.

    '''
    global x_sup, y_sup, r1_sup, r2_sup, vx_sup, vy_sup, vr_sup
    global superball_needed, superball_initiated
    if (x_sup + r2_sup) > 1200 or (x_sup - r2_sup) < 0 :
        vx_sup = - vx_sup
    if (y_sup + r2_sup) > 700 or (y_sup - r2_sup) < 0:
        vy_sup = - vy_sup
    x_sup += vx_sup
    y_sup += vy_sup
    r1_sup -= vr_sup
    r2_sup -= vr_sup
    draw_sun(x_sup, y_sup, r1_sup, r2_sup)
    if r1_sup < 0:
        superball_needed = False
        superball_initiated = False


def print_score():
    '''
    prints player's score

    Returns
    -------
    None.

    '''
    font = pygame.font.Font(None, 72)
    text = font.render("Score: " + str(score), True, SILVER)
    screen.blit(text, [500, 30])
      
    
def print_comment(comment, x, y, size):
    '''
    prints some comments

    Returns
    -------
    None.

    '''
    font = pygame.font.Font(None, size)
    text = font.render(comment, True, SILVER)
    screen.blit(text, [x, y])
    
    
def save_scores(final_score, name):
    if name == '':
        name = 'Player'
    file.write(name + " : " + str(final_score) + '\n')
    
pygame.display.update()
clock = pygame.time.Clock()
finished = False

new_balls(n)

while not finished:
    fps_change = FPS + score//100
    screen.fill(DARK_BLUE)
    clock.tick(fps_change)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.KEYDOWN:
            finished = True
            name_to_write = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if check_click(event)[0] == 'super':
                score += int(1/(r2_sup)*10000)
                comment_needed = True
                superball_needed = False
                superball_initiated = False
            elif check_click(event)[0] == 'usual':
                score += 50 - r[check_click(event)[1]]//2
                new_ball(check_click(event)[1])
            else:
                score -= 1
    move_balls()
    
    if score % 200 < 20 and not (superball_initiated):
        superball_needed = True
        new_superball()
        superball_initiated = True
    if  superball_needed and superball_initiated:
        move_superball()
    print_score()
    if comment_needed == True:
        comment_count += 1
        print_comment("AWESOME!", 500, 300, 72)
    if comment_count > 150:
        comment_count = 0
        comment_needed = False
    pygame.display.update()


while name_to_write:
    screen.fill(DARK_BLUE)
    clock.tick(FPS)
    print_comment("Enter your name:", 400, 300, 72)
    print_comment("Please, small letters and numbers only", 400, 350, 36)
    print_comment("Enter to save your result, close to exit without saving", 400, 500, 36)
    print_comment(name, 400, 400, 72)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            name_to_write = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                name_to_write = False
            elif (event.key < 123 and event.key > 96) or (event.key < 58 and event.key > 47):
                name += chr(event.key)
    pygame.display.update()

save_scores(score, name)

file.close()
pygame.quit()
