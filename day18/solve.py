import os 
import math
import numpy as np
from scipy.linalg import null_space
import scipy.sparse as sp
import queue 
from typing import List
from dataclasses import dataclass,field
folder = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(folder,"input.txt")

look = {"R":np.array([0,1]),"L":np.array([0,-1]),"U":np.array([-1,0]),"D":np.array([1,0])}

dir_order = ["R","D","L","U"]

def area_np(x, y):        
    x = np.asanyarray(x)
    y = np.asanyarray(y)
    n = len(x)
    shift_up = np.arange(-n+1, 1)
    shift_down = np.arange(-1, n-1)    
    return (x * (y.take(shift_up) - y.take(shift_down))).sum() / 2.0

def compute_area(directions):
    path = [np.array([0,0])]
    length = 0 
    for (dir,distance) in directions:
        path.append(path[-1] + look[dir]*distance)
        length += distance 

    pthmat = np.array(path)
    return abs(area_np(pthmat[:,0],pthmat[:,1]))+length/2+1



def solve(): 
    with open(input_file,'r') as f:
        colors = []
        directions = []
        for link in f.readlines():
            (dir,dist,colour) = link.strip().split(' ')
            directions.append((dir,int(dist)))
            colors.append(colour)

        print(compute_area(directions))

        directions2 = []
        for c in colors:
            directions2.append((dir_order[int(c[-2])],int(c[2:-2],16)))

        print(compute_area(directions2))


        




            




if __name__ == "__main__":

    solve()