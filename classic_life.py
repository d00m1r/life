from set_field import * 
import numpy as np
import argparse
import pygame

size = [150, 150]
rule = 1

def randomField(): 
    if rule == 0:#classic
        val = [1, 0]
        return np.random.choice(val, size[0]*size[1], p=[0.3, 0.7]).reshape(size[0], size[1]) 
    elif rule == 1:
        val = [0, 1, 2, 3]#empty plant plant-eating predator
        return np.random.choice(val, size[0]*size[1], p=[0.0, 0.4, 0.3, 0.3]).reshape(size[0], size[1])
  
def update(grid): 
    '''update field based on relevant rules'''
    newGrid = grid.copy() 
    for i in range(size[0]): 
        for j in range(size[1]): 
            
            #classic rules 
            if rule == 0:
                
                #check neighbors
                total = (grid[i, (j-1)%size[1]] + grid[i, (j+1)%size[1]] + 
                        grid[(i-1)%size[0], (j-1)%size[1]] + grid[(i-1)%size[0], (j+1)%size[1]] + 
                        grid[(i+1)%size[0], (j-1)%size[1]] + grid[(i+1)%size[0], (j+1)%size[1]] + 
                        grid[(i-1)%size[0], j] + grid[(i+1)%size[0], j])

                if grid[i, j]  == 1:#dead
                    if (total < 2) or (total > 3): 
                        newGrid[i, j] = 0 
                else: #alive
                    if total == 3: 
                        newGrid[i, j] = 1 
            
            #my mode
            elif rule == 1:
                
                if grid[i,j] == 1:
                    newGrid[i,j] = func1(grid, i, j)
                elif grid[i,j] == 2:
                    newGrid[i,j] = func2(grid, i, j)
                elif grid[i,j] == 3:
                    newGrid[i,j] = func3(grid, i, j)
                else:
                    newGrid[i,j] = func0(grid, i, j)

    return newGrid

def draw_field(field):
    
    global screen

    for x in range(len(field)):
        for y in range(field.shape[1]):

            if rule == 0:
                if field[x, y] == 1:
                    draw_cell(screen, GREEN, (x, y))
                else:
                    draw_cell(screen, BLACK, (x, y))

            elif rule == 1:
                if field[x, y] == 1:
                    draw_cell(screen, GREEN, (x, y))
                elif field[x, y] == 2:
                    draw_cell(screen, BLUE, (x, y))
                elif field[x, y] == 3:
                    draw_cell(screen, RED, (x,y))
                else:
                    draw_cell(screen, BLACK, (x, y))
                

def parse_args():

    parser = argparse.ArgumentParser(description="Game of Life simulation") 
    parser.add_argument("-c", "--classic", action = 'store_true', help='run a classic mode of GoL')

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
        clock.tick(30)#FPS

    pygame.quit()

def func1(field, x, y):
    '''plant's rules'''
    if check(field, x, y, 2) > 0: 
        return 0
    if check(field, x, y, 1) < 6 and check(field, x, y, 1) > 1: 
        return 1
    return 0

def func2(field, x, y):
    '''plant-eating animal's rules'''
    if check(field, x, y, 3) > 0: 
        return 0
    if 2 <= check(field, x, y, 2) and  check(field, x, y, 2) <= 5 and check(field, x, y, 1) > 0:
        return 2
    return 0

def func3(field, x, y):
    '''predator's rules'''
    if 2 <= check(field, x, y, 3) and check(field, x, y, 3) <= 4 and check(field, x, y, 2) > 0:
        return 3
    return 0

def func0(field, x, y):
    '''dead cell'''
    plants = check(field, x, y ,1)
    pl_eats = check(field, x , y, 2)
    pred = check(field, x, y, 3)

    if 2 <= pred and pred <= 4 and pl_eats > 0:
        return 3

    elif 2 <= pl_eats and pl_eats <= 5 and plants > 0:
        return 2

    elif plants < 6 and plants > 1: 
        return 1

    else:
        return 0
    '''
    if pred > 0:
        if pred < 5 and pred > 1 and pl_eats > 0:
            return 3
        elif pl_eats <= 5 and pl_eats >= 2:
            return 2
        else:
            return 0

    else:
        if pl_eats <= 5 and pl_eats >= 2:
            return 2
        elif plants >= 2 and plants <= 3:
            return 1
        else:
            return 0
    '''



def check(field, x, y, val):
    '''check all neighbors'''
    num = 0

    for i in range(-1, 2, 2):
        if field[(x + i)%size[0] , (y + i)%size[1]] == val:
            num += 1
        if field[x , (y + i)%size[1]] == val or field[(x + i)%size[0] , y] == val:
            num += 1
        if field[(x + i)%size[0] , (y - i)%size[1]] == val:
            num += 1

    return num


if  __name__ == "__main__":

    args = parse_args()
    if args.classic:
        rule = 0
    run()

