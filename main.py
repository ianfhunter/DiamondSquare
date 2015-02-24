import sys,pprint
from random import randint
from utils import *
from constants import *

#x,y - position in main grid
def DSFractal(main,x,y,grid):

    square(grid)
    diamond(main,x,y,grid)

    minis = subgrid(grid)

    half = len(grid)/2

    # Order of recursion
    #   1  2
    #   3  4
    #
    if len(minis[0]) > 2 :
        insert(grid,main,x,y)
        insert(DSFractal(main,x,y,minis[0]),grid,0,0)
    
    if len(minis[1]) > 2 :
        insert(grid,main,x,y)
        insert(DSFractal(main,(half)+x,y,minis[1]),grid,half,0)       

    if len(minis[2]) > 2 :
        insert(grid,main,x,y)
        insert(DSFractal(main,x,(half)+y,minis[2]),grid,0,half) 

    if len(minis[3]) > 2 :
        insert(grid,main,x,y)
        insert(DSFractal(main,(half)+x,(half)+y,minis[3]),grid,half,half)   

    return grid


# Validate size of grid
if (grid_size-1 & (grid_size - 2)) != 0:
    sys.exit("Invalid Number. Must be (2^n)+1 ")

pp = pprint.PrettyPrinter(indent=4)

#init 2d array with 0s
grid = [[0 for x in range(grid_size)] for x in range(grid_size)]   

#set corners to half height
grid[0][0] = initial_height
grid[0][len(grid)-1] = initial_height
grid[len(grid)-1][0] = initial_height
grid[len(grid)-1][len(grid)-1] = initial_height


DSFractal(grid,0,0,grid)
display(output_type,grid)
