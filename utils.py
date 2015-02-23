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

def offset(gridsize):
    if landscape_type == 0:
        val = randint(0,roughness * gridsize) 
    else:
        val = randint(-roughness * gridsize,roughness * gridsize) 
    #print val
    return val

def square(grid):
    global square_step_amount
    global roughness

    x1,y1,x2,y2,x3,y3,x4,y4 = get_corners(grid)

    #Get midpoint
    mid_x = ((x2-x1) / 2 ) #+ x1    #x2 transformed to origin, halved and transformed back
    mid_y = ((y3-y1) / 2 )# + y1    #y3 transformed to origin, halved and transformed back


    #Assign mean + random
    mean = (grid[x1][y1] + grid[x2][y2] + grid[x3][y3] + grid[x4][y4]) / 4

    grid[mid_x][mid_y] = mean + offset(len(grid))

    return

#Gets the average of 4 points, excluding zero value items
def average(a,b,c,d,main):
    total = 0
    count = 0
    if a is not None:
        x = main[a[0]][a[1]]
        # print x
        if x != 0:
            total = total + x
            count = count + 1
    if b is not None:
        x = main[b[0]][b[1]]
        # print x
        if x != 0:
            total = total + x
            count = count + 1
    if c is not None:
        x = main[c[0]][c[1]]
        # print x
        if x != 0:
            total = total + x
            count = count + 1
    if d is not None:
        x = main[d[0]][d[1]]  
        # print x
        if x != 0:
            total = total + x 
            count = count + 1

    # print "average: ", (total/count)
    return total/count

def diamond(main,gx,gy,grid):
    global roughness
    
    last = len(grid)-1  #last grid index
    half = last / 2         #midpoint

    #Assign mean + random

    #top
    #
    #      a
    #    b O c
    #  e O d O f
    #    g O h
    #      i

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

    print a,b,c,d,e,f,g,h,i

    #averages
    top = average(a,b,c,d,main)
    left = average(b,e,d,g,main)
    right = average(c,d,f,h,main)
    bottom = average(d,g,h,i,main)

    #assign values
    grid[half][0] = top + offset(len(grid))
    grid[0][half] = left + offset(len(grid))
    grid[last][half] = right + offset(len(grid))
    grid[half][last] = bottom + offset(len(grid))

def subgrid(grid):
    x1,y1,x2,y2,x3,y3,x4,y4 = get_corners(grid)

    upper_left_grid =grid[:y3/2+1] #Halved on one dimension
    lower_left_grid = grid[:y3/2+1]
    for idx,row in enumerate(upper_left_grid):
        upper_left_grid[idx] = row[:(x2/2)+1]  #Halved on the second dimension
        lower_left_grid[idx] = row[x2/2:]  #Halved on the second dimension

    upper_right_grid =grid[y3/2:] #Halved on one dimension
    lower_right_grid = grid[y3/2:]
    for idx,row in enumerate(upper_right_grid):
        upper_right_grid[idx] = row[:(x2/2)+1]  #Halved on the second dimension
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
