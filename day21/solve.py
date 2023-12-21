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

def neighbours(s):
   (i,j) = s 
   return [(i+1,j),(i-1,j),(i,j+1),(i,j-1)]

def walk(available,start,steps=64):
    step_count = np.zeros(shape=(2*steps+1,2*steps+1),dtype=int)
    step_count[:,:]=steps+5
    step_count[steps,steps]=0
    convert = lambda x : (x[0]-steps+start[0],x[1]-steps+start[1])
    for step in range(0,steps):
        for loc in np.argwhere(step_count==step):
            s = (loc[0],loc[1])
            for n in neighbours(s):
                if convert(n) in available:
                    (i,j) = n 
                    step_count[i,j]=min(step+1,step_count[i,j])
    print(np.sum(np.logical_and(step_count <= steps,np.mod(step_count,2) == 0)))

def solve(): 
    with open(input_file,'r') as f:
        available=set()
        start=None
        for (i,link) in enumerate(f.readlines()):
         for (j,s) in enumerate(list(link.strip())):

            if s == '.':
               available.add((i,j))

            if s == 'S':
               start=(i,j)
               available.add((i,j))

        walk(available,start)
        print(start)


    
        
            

            


        




            




if __name__ == "__main__":

    solve()