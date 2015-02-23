from random import randint
from constants import *

def get_corners(grid):
    # x1,y2     x2,y2
    #
    #
    # x3,y3     x4,y4

    return (
        0,0,
        len(grid)-1,0,
        0,len(grid[0])-1,
        len(grid)-1,len(grid[0])-1
        )

def square(grid):
    global square_step_amount
    global roughness

    x1,y1,x2,y2,x3,y3,x4,y4 = get_corners(grid)

    #Get midpoint
    mid_x = ((x2-x1) / 2 ) #+ x1    #x2 transformed to origin, halved and transformed back
    mid_y = ((y3-y1) / 2 )# + y1    #y3 transformed to origin, halved and transformed back


    #Assign mean + random
    mean = (grid[x1][y1] + grid[x2][y2] + grid[x3][y3] + grid[x4][y4]) / 4

    grid[mid_x][mid_y] = mean + randint(0,roughness * len(grid)) 

    return

def diamond(grid):
    global diamond_step_amount
    global roughness
    x1,y1,x2,y2,x3,y3,x4,y4 = get_corners(grid)

    #get midpoints
    half_x = ((x2-x1) / 2 ) + x1
    half_y = ((y3-x1) / 2 ) + y1 

    left = (half_x , y3)
    right = (half_x, y1)
    top = (x1, half_y)
    bottom = (x2, half_y) 


    #Assign mean + random
    mean = (grid[x1][y1] + grid[x2][y2] + grid[x3][y3] + grid[x4][y4]) / 4


    grid[top[0]][top[1]] = mean + randint(0,roughness * len(grid)) 
    grid[left[0]][left[1]] = mean + randint(0,roughness * len(grid)) 
    grid[right[0]][right[1]] = mean + randint(0,roughness * len(grid)) 
    grid[bottom[0]][bottom[1]] = mean + randint(0,roughness * len(grid)) 


def subgrid(grid):
    x1,y1,x2,y2,x3,y3,x4,y4 = get_corners(grid)

    upper_left_grid =grid[:y3/2+1] #Halved on one dimension
    upper_right_grid = grid[:y3/2+1]
    for idx,row in enumerate(upper_left_grid):
        upper_left_grid[idx] = row[:(x2/2)+1]  #Halved on the second dimension
        upper_right_grid[idx] = row[x2/2:]  #Halved on the second dimension

    lower_left_grid =grid[y3/2:] #Halved on one dimension
    lower_right_grid = grid[y3/2:]
    for idx,row in enumerate(lower_left_grid):
        lower_left_grid[idx] = row[:(x2/2)+1]  #Halved on the second dimension
        lower_right_grid[idx] = row[x2/2:]  #Halved on the second dimension

    return (upper_left_grid,upper_right_grid,lower_left_grid,lower_right_grid)


def insert(sub,grid,x,y):
    for r_idx,row in enumerate(sub):
        for c_idx,item in enumerate(row):
            #if grid[x+r_idx][y+c_idx] == 0:
            grid[x+r_idx][y+c_idx] = item
            #else:
                #grid[x+r_idx][y+c_idx] = item
                #print  grid[x+r_idx][y+c_idx] 
               # grid[x+r_idx][y+c_idx] = (grid[x+r_idx][y+c_idx] + item )/ 2
