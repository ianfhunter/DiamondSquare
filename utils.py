from random import randint
from constants import *

############# Math #############

#Gets the average of 4 points on the grid. Ignores points that don't exist & zero points
def average(a,b,c,d,main):
    total = 0
    count = 0
    if a is not None:
        x = main[a[0]][a[1]]
        if x != 0:
            total = total + x
            count = count + 1
    if b is not None:
        x = main[b[0]][b[1]]
        if x != 0:
            total = total + x
            count = count + 1
    if c is not None:
        x = main[c[0]][c[1]]
        if x != 0:
            total = total + x
            count = count + 1
    if d is not None:
        x = main[d[0]][d[1]]  
        if x != 0:
            total = total + x 
            count = count + 1

    return total/count


def MaxMinValues(d):
     #Returns max and min values from a dictionary
     v=list(d.values())
     return (max(v),min(v))

############# Algorithm #############

def offset(gridsize):
    global roughness

    if landscape_type == 0:
        val = randint(0,roughness * gridsize) 
    else:
        val = randint(-roughness * gridsize,roughness * gridsize) 

    return val


# midpoint = average of corners + random_step
def square(grid):
    #      
    #    a   b
    #      O  
    #    c   d
    #      

    last = len(grid)-1  #last grid index
    half = last / 2         #midpoint

    #Assign mean + random
    mean = (grid[0][0] + grid[last][0] + grid[0][last] + grid[last][last]) / 4

    grid[half][half] = mean + offset(len(grid))

    return


# edges = average of surrounding edges + random_step
def diamond(main,gx,gy,grid):
    #
    #      a
    #    b O c
    #  e O d O f
    #    g O h
    #      i
    
    last = len(grid)-1  #last grid index
    half = last / 2         #midpoint

    #surrounding corners
    b = (gx,gy)
    c = (gx + last, gy)
    g = (gx, gy + last)
    h = (gx + last, gy + last)

    #midpoint
    d = (gx+half,gy+half)

    #extreme corners
    a = (gx + half, gy - half) if gy - half >= 0 else None
    e = (gx - half, gy + half) if gx - half >= 0 else None
    f = (gx + last + half, gy + half) if gx + last + half < len(main) else None
    i = (gx + half, gy + last + half) if gy + last + half < len(main) else None

    #print a,b,c,d,e,f,g,h,i

    #averages
    top    = average(a,b,c,d,main)
    left   = average(b,e,d,g,main)
    right  = average(c,d,f,h,main)
    bottom = average(d,g,h,i,main)

    #assign values
    grid[half][0] = top + offset(len(grid))
    grid[0][half] = left + offset(len(grid))
    grid[last][half] = right + offset(len(grid))
    grid[half][last] = bottom + offset(len(grid))

def subgrid(grid):
    last = len(grid)-1  #last grid index
    half = last / 2         #midpoint

    upper_left_grid =grid[:half+1] #Halved on one dimension
    lower_left_grid = grid[:half+1]
    for idx,row in enumerate(upper_left_grid):
        upper_left_grid[idx] = row[:half+1]  #Halved on the second dimension
        lower_left_grid[idx] = row[half:]  #Halved on the second dimension

    upper_right_grid =grid[half:] #Halved on one dimension
    lower_right_grid = grid[half:]
    for idx,row in enumerate(upper_right_grid):
        upper_right_grid[idx] = row[:half+1]  #Halved on the second dimension
        lower_right_grid[idx] = row[half:]  #Halved on the second dimension

    return (upper_left_grid,upper_right_grid,lower_left_grid,lower_right_grid)


# Insert sub into grid at position x,y
def insert(sub,grid,x,y):
    for r_idx,row in enumerate(sub):
        for c_idx,item in enumerate(row):
            grid[x+r_idx][y+c_idx] = item
