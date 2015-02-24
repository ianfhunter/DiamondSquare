import pygame, sys,pprint
from random import randint
from pygame.locals import *
from utils import *
from constants import *

#validate input size.
if (grid_size-1 & (grid_size - 2)) != 0:
    sys.exit("Invalid Number. Must be (2^n)+1 ")

pp = pprint.PrettyPrinter(indent=4)

def MaxMinValues(d):
     #Returns max and min values from a dictionary
     v=list(d.values())
     return (max(v),min(v))

#x,y - position in main grid
def DSFractal(main,x,y,grid,mx,my):

    square(grid)
    diamond(main,x,y,grid)

    minis = subgrid(grid)

    half = len(grid)/2

    #
    #   1  2
    #   3  4
    #
    if len(minis[0][0]) > 2 and len(minis[0]) > 2 :
        insert(grid,main,mx,my)
        insert(DSFractal(main,x,y,minis[0],mx,my),grid,0,0)
    
    if len(minis[1][0]) > 2 and len(minis[1]) > 2 :
        insert(grid,main,mx,my)
        insert(DSFractal(main,(half)+x,y,minis[1],mx+(half),my),grid,half,0)       

    if len(minis[2][0]) > 2 and len(minis[2]) > 2 :
        insert(grid,main,mx,my)
        insert(DSFractal(main,x,(half)+y,minis[2],mx,my+(half)),grid,0,half) 

    if len(minis[3][0]) > 2 and len(minis[3]) > 2 :
        insert(grid,main,mx,my)
        insert(DSFractal(main,(half)+x,(half)+y,minis[3],mx+(half),my+(half)),grid,half,half)   

    return grid



grid = [[0 for x in range(grid_size)] for x in range(grid_size)] 

grid[0][0] = max_height /2
grid[0][len(grid)-1] =  max_height /2
grid[len(grid)-1][0] =  max_height /2
grid[len(grid)-1][len(grid)-1] = max_height /2 


DSFractal(grid,0,0,grid,0,0)


################ DISPLAY




if output_type == 0:
    print '"x"',",",'"y"',",",'"value"'         #column headers
    for col,column in enumerate(grid):
        for row,item in enumerate(column):
            print col, ",",row,",",item



if output_type == 1:
    pygame.init()
    SCREENX = 800
    SCREENY = 800

    x_bit = SCREENX / len(grid)
    y_bit = SCREENY / len(grid[0])

    # Heatmap 

    #setup dictionary
    items = {}
    for col,column in enumerate(grid):
        for row,item in enumerate(column):
            items[item] = item 

    # Find max numbers & convert to a 0-1 scale
    ma,mi = MaxMinValues(items)
    span = ma - mi
    for x in items:
        #associated new value
        items[x] = (((items[x] - mi) * 1020) / span)         #765 is the range of colours we want to represent.


    #pygame setup
    screen = pygame.display.set_mode((SCREENX, SCREENY))    #display
    pygame.display.set_caption('Overhead View')             #window
    while True:                                             # main display loop
        for col,column in enumerate(grid):
            for row,item in enumerate(column):
                val = items[item]                           #Get heat value
                if val <= 255:
                    pygame.draw.rect(screen, (0,val,255), (x_bit*row,y_bit*col, x_bit, y_bit))  #blue -> cyan
                elif val <= 510:
                    pygame.draw.rect(screen, (0,255,val-255), (x_bit*row,y_bit*col, x_bit, y_bit))  #cyan -> green
                elif val <= 765:    
                    pygame.draw.rect(screen, (val-510,255,0), (x_bit*row,y_bit*col, x_bit, y_bit))  #green -> yellow
                elif val <= 1020:    
                    pygame.draw.rect(screen, (255,val-765,0), (x_bit*row,y_bit*col, x_bit, y_bit))  #yellow -> red
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        pygame.display.update()


if output_type == 2:
    import numpy
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    from matplotlib import cm

    # Set up grid and test data
    nx, ny = 256, 1024
    x = range(len(grid))
    y = range(len(grid))

    data = numpy.array(grid)

    hf = plt.figure()
    ha = hf.add_subplot(111, projection='3d')

    X, Y = numpy.meshgrid(x, y)  # `plot_surface` expects `x` and `y` data to be 2D
    ha.plot_surface(X, Y, data,shade=True,cmap=cm.terrain,rstride=1, cstride=1,)

    plt.show()