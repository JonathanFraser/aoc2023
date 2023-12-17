import os 
import math
import numpy as np
from scipy.linalg import null_space
import scipy.sparse as sp
folder = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(folder,"input.txt")

up = np.array([-1,0],dtype=int)
down = np.array([1,0],dtype=int)
right = np.array([0,1],dtype=int)
left = np.array([0,-1],dtype=int)

isUp = lambda x: np.all(np.equal(up,x))
isDown = lambda x: np.all(np.equal(down,x))
isLeft = lambda x: np.all(np.equal(left,x))
isRight = lambda x: np.all(np.equal(right,x))

def beyond_bounds(puzzle,current_loc):
   (h,w) = current_loc

   if h < 0 or h >= puzzle.shape[0]:
      return True 
   
   if w < 0 or w >= puzzle.shape[1]:
      return True
   
def step(puzzle,current_state):
    (current_loc,current_dir) = current_state

    #if beyond_bounds(puzzle,current_loc):
    #    return []

    current_obj = puzzle[current_loc[0],current_loc[1]]

    if current_obj == '.':
        return [(current_loc+current_dir,current_dir)]
   
    if current_obj == '/':
        if isLeft(current_dir):
            return [(current_loc+down,down)]
      
        if isRight(current_dir):
            return [(current_loc+up,up)]
      
        if isDown(current_dir):
            return [(current_loc+left,left)]
      
        if isUp(current_dir):
            return [(current_loc+right,right)]
      
    if current_obj == '\\':
        if isLeft(current_dir):
            return [(current_loc+up,up)]
        
        if isRight(current_dir):
            return [(current_loc+down,down)]
        
        if isUp(current_dir):
            return [(current_loc+left,left)]
        
        if isDown(current_dir):
            return [(current_loc+right,right)]
        
    if current_obj == '|':
        if isUp(current_dir) or isDown(current_dir):
            return [(current_loc+current_dir,current_dir)]
        
        return [(current_loc+up,up),(current_loc+down,down)]
    
    if current_obj == '-':
        if isLeft(current_dir) or isRight(current_dir):
            return [(current_loc+current_dir,current_dir)]
        
        return [(current_loc+left,left),(current_loc+right,right)]
    
    raise RuntimeError(f"unknown path for {current_state} and {puzzle[current_loc]}")
      
def run_puzzle(puzzle,start=(np.array([0,0],dtype=int),right)):
    paths = [start]
    cache = set()
    seen = set()
    while paths:
        path = paths[0]
        paths = paths[1:]
        (loc,dir) = path
        if (tuple(loc),tuple(dir)) in cache:
            continue
        if beyond_bounds(puzzle,loc):
            continue
        cache.add((tuple(loc),tuple(dir)))
        seen.add(tuple(loc))
        paths+=step(puzzle,path)

    return seen
      

def solve(): 
    with open(input_file,'r') as f:
        lines = []
        for link in f.readlines():
         lines.append(np.array(list(link.strip())))

    puzzle = np.array(lines)

    out = run_puzzle(puzzle)
    print(f"tl-r: {len(out)}")
    (h,w) = puzzle.shape
    directions = []
    for i in range(0,w):
        directions.append((np.array([0,i],dtype=int),down))
        directions.append((np.array([h-1,i],dtype=int),up))

    for i in range(0,h):
        directions.append((np.array([i,0],dtype=int),right))
        directions.append((np.array([i,w-1],dtype=int),left))

    results = []
    for d in directions:
        results.append(len(run_puzzle(puzzle,start=d)))

    print(results)
    print(max(results))
 


if __name__ == "__main__":

    solve()