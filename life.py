from set_field import * 
import numpy as np
import argparse
import pygame
import random

size = [75, 75]
rule = 1

def randomField(): 
    if rule == 0:#classic
        val = [1, 0]
        return np.random.choice(val, size[0]*size[1], p=[0.3, 0.7]).reshape(size[0], size[1]) 

    elif rule == 1:
        val = [0, 1, 2, 3, 4, 5, 6, 7]#r(0) white(1) y(2) g(3) b(4) i(5) v(6) black(7)
        a = 0.05714285714285715
        b = 0.014285714285714287


        return np.random.choice(val, size[0]*size[1], p=[a, a, a, a, a, a, a, 0.6]).reshape(size[0], size[1])
  
def update(field): 
    '''update field based on relevant rules'''

    newField = field.copy()
    
    if rule == 0:

        for i in range(size[0]): 
            for j in range(size[1]): 

                #check neighbors
            
                total = check(field, i, j, 1)
                if field[i, j] == 1:
                    if (total < 2) or (total > 3): 
                        newField[i, j] = 0
                    else:
                        newField[i, j] = 1
                else:
                    if total == 3:
                        newField[i, j] = 1
                

    else:#my mode

        for i in range(size[0]): 
            for j in range(size[1]): 
            
                color_list, total = check_color(field, i, j)
                if field[i, j] != 7:
                    if (total >= 2) and (total <= 3):
                        newField[i, j] = field[i, j]#alive
                    else:
                        newField[i, j] = 7#dead
                else:
                    if total == 3:#revive
                        newField[i, j] = set_color(color_list)


    return newField

def set_color(l):#l[r,w,y,g,b,i,v]

    if l[1] > 0:
        return random.randint(0,6)#make more random

    sl = []#color of 3 neighbors[_,_,_]
    counter = 3

    for i in range(len(l)):
        if l[i] > 1:
            return i 

        if l[i] == 1:
            sl.append(i)

    for el in sl:
        if el == 0 or el == 3 or el == 4:
            counter += 1
        elif el == 2 or el == 5 or el == 6 :
            counter -= 1

    set_l = {0:(sl[0],sl[1]), 1:(sl[1],sl[0]), 2:(sl[0],sl[2]), 3:(sl[2],sl[0]), 4:(sl[1],sl[2]), 5:(sl[2],sl[1])}
    
    RGB = {(2,6):0, (6,2):0, (2,5):3, (5,2):3, (5,6):4, (6,5):4} #пурпурный и желтый дают красный, индиго и желтый дают зеленый,
    # а индиго и пурпурный дают синий.
    YIV = {(0,3):2, (3,0):2, (3,4):5, (4,3):5, (0,4):6, (4,0):6} # Синий и зеленый дают индиго, красный и синий дают пурпурный,
    # а красный и зеленый дают желтый.

    if counter == 6:
        return 1#random.randint(0,3)
    if counter == 0:#RGB -> W; #YIV -> W
        return 1#random.randint(4,6)


    if counter > 3:#return YIV
        for el in set_l.values():
            if el in YIV.keys():
                return YIV.pop(el)

    elif counter < 3:#return RGB
        for el in set_l.values():
            if el in RGB.keys():
                return RGB.pop(el)

        
    
def draw_field(field):
    
    global screen

    if rule == 0:#classic life

        for x in range(len(field)):
            for y in range(field.shape[1]):

                if field[x, y] == 1:
                    draw_cell(screen, GREEN, (x, y))
                else:
                    draw_cell(screen, BLACK, (x, y))

    else: 
        for x in range(len(field)):
            for y in range(field.shape[1]):
            
                if field[x, y] == 0:
                    draw_cell(screen, RED, (x, y))
                elif field[x, y] == 1:
                    draw_cell(screen, WHITE, (x, y))
                elif field[x, y] == 2:
                    draw_cell(screen, YELLOW, (x, y))
                elif field[x, y] == 3:
                    draw_cell(screen, GREEN, (x, y))
                elif field[x, y] == 4:
                    draw_cell(screen, BLUE, (x, y))
                elif field[x, y] == 5:
                    draw_cell(screen, INDIGO, (x, y))
                elif field[x, y] == 6:
                    draw_cell(screen, VIOLET, (x, y))
                else:
                    draw_cell(screen, BLACK, (x, y))

def parse_args():

    parser = argparse.ArgumentParser(description="Game of Life simulation") 
    parser.add_argument("-c", "--classic", action = 'store_true', help='run a classic mode of GoL')
    parser.add_argument("-s", "--spectrum", action = 'store_true', help = 'run a spectral life variation')
    return parser.parse_args()

def run():

    global screen

    pygame.init
    screen = set_mode(size)#make grid
    clock = pygame.time.Clock()

    field = randomField()

    running = True

    while running:
        
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                running = False

            pressed = pygame.mouse.get_pressed()
            pos = pygame.mouse.get_pos()

            if rule == 0:
                if pressed[0]:
                    field[pos[0]//SCALE,pos[1]//SCALE] = 1

            elif rule == 1:
                if pressed[0]:
                    field[pos[0]//SCALE,pos[1]//SCALE] = 0
                elif pressed[2]:
                    field[pos[0]//SCALE,pos[1]//SCALE] = 2

            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 1:  #left button cell alive
                    field[event.pos[0]//SCALE,event.pos[1]//SCALE] = 1 #ret tuple(x,y)
                if event.button == 3:  #right button cell dead
                    field[event.pos[0]//SCALE,event.pos[1]//SCALE] = 0

        
        draw_field(field)

        field = update(field)

        pygame.display.flip()
        clock.tick(10)#FPS

    pygame.quit()


def check_color(field, x, y):
    '''calculate neighbors for each color'''

    col_list = np.array([0, 0, 0, 0, 0, 0, 0])# num for each color
    total = 0 #summary of neighbors

    col_list[0] = check(field, x, y, 0)#check red...
    col_list[1] = check(field, x, y, 1)#white
    col_list[2] = check(field, x, y, 2)#yellow
    col_list[3] = check(field, x, y, 3)#green
    col_list[4] = check(field, x, y, 4)#blue
    col_list[5] = check(field, x, y, 5)#indigo
    col_list[6] = check(field, x, y, 6)#violet

    for i in range(7):
        if col_list[i] > 0:
            total += col_list[i]

    return col_list, total

def check(field, x, y, val):
    '''check all neighbors'''
    num = 0

    for i in range(-1, 2, 2):
        if field[(x + i)%size[0] , (y + i)%size[1]] == val: #x-1 y-1; x+1 y+1
            num += 1
        if field[x , (y + i)%size[1]] == val: #x, y-1 ; x, y+1
            num += 1
        if field[(x - i)%size[0] , y] == val: # x+1, y;  x-1, y
            num += 1
        if field[(x + i)%size[0] , (y - i)%size[1]] == val: #x-1, i+1; x+1, y-1
            num += 1
            
    return num


if  __name__ == "__main__":

    args = parse_args()
    if args.classic:
        rule = 0
    if args.spectrum:
        rule = 1
    run()

