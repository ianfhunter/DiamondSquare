import pygame, sys
from random import randint
import pprint
from pygame.locals import *
from utils import *
from constants import *
import sys

#validate amount
if (grid_size-1 & (grid_size - 2)) != 0:
    sys.exit("Invalid Number. Must be power of 2 +1")


pp = pprint.PrettyPrinter(indent=4)
depth = 0


def MaxMinKeys(d):
     """ a) create a list of the dict's keys and values; 
         b) return the key with the max value"""  
     v=list(d.values())
     k=list(d.keys())
     return (k[v.index(max(v))],k[v.index(min(v))])

def DSFractal(grid,depth):
    # print "Grid of size ", len(grid), "x", len(grid[0])
    depth = depth + 1

    square(grid)
    diamond(grid)
    minis = subgrid(grid)

    if depth == 1:
        pp.pprint(grid)
    if len(minis[0][0]) > 2 and len(minis[0]) > 2 :
        insert(DSFractal(minis[0],depth),grid,0,0)
    if depth == 1:
        pp.pprint(grid)
    
    if len(minis[1][0]) > 2 and len(minis[1]) > 2 :
        insert(DSFractal(minis[1],depth),grid,len(grid)/2,0)

    if len(minis[2][0]) > 2 and len(minis[2]) > 2 :
        insert(DSFractal(minis[2],depth),grid,0,len(grid[0])/2)

    if len(minis[3][0]) > 2 and len(minis[3]) > 2 :
       insert(DSFractal(minis[3],depth),grid,len(grid)/2,len(grid[0])/2)
    #pp.pprint(grid)
    return grid



grid = [[0 for x in range(grid_size)] for x in range(grid_size)] 

#Random Heights for corners
# grid[0][0] = randint(1,initial_step)
# grid[0][len(grid)-1] = randint(1,initial_step)
# grid[len(grid)-1][0] = randint(1,initial_step)
# grid[len(grid)-1][len(grid)-1] = randint(1,initial_step)

grid[0][0] = max_height /2
grid[0][len(grid)-1] =  max_height /2
grid[len(grid)-1][0] =  max_height /2
grid[len(grid)-1][len(grid)-1] = max_height /2 


DSFractal(grid,depth)

#pp.pprint(grid)

################ DISPLAY


pygame.init()
SCREENX = 800
SCREENY = 800

x_bit = SCREENX / len(grid)
y_bit = SCREENY / len(grid[0])

#get colour list

items = {}
for col,column in enumerate(grid):
    for row,item in enumerate(column):
        if not item in items:
            items[item] = 0
        items[item] = items[item] + 1

#To a 0-1 scale
ma,mi = MaxMinKeys(items)
ma = items[ma]
mi = items[mi]
span = ma - mi
for x in items:
    items[x] = (((items[x] - mi) * 765) / span)


print '"x"',",",'"y"',",",'"value"'
for col,column in enumerate(grid):
    for row,item in enumerate(column):
        print col, ",",row,",",item


screen = pygame.display.set_mode((SCREENX, SCREENY))
pygame.display.set_caption('Hello World!')
while True: # main game loop
    for col,column in enumerate(grid):
        for row,item in enumerate(column):
            val = items[item]
            if val <= 255:
                pygame.draw.rect(screen, (0,val,255), (x_bit*row,y_bit*col, x_bit, y_bit))
            elif val <= 510:
                pygame.draw.rect(screen, (0,255,val-255), (x_bit*row,y_bit*col, x_bit, y_bit))
            elif val <= 765:    
                pygame.draw.rect(screen, (255,val-510,0), (x_bit*row,y_bit*col, x_bit, y_bit))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()

