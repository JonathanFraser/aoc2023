import os 
import math
import numpy as np
from scipy.linalg import null_space
import scipy.sparse as sp
folder = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(folder,"input.txt")


def get_value(puzzle):
    return (get_horizontal_symmetry(puzzle),get_horizontal_symmetry(puzzle.T))

def get_horizontal_symmetry(puzzle):
    (height,width) = puzzle.shape
    
    ret = set()
    for i in range(1,width):
        fill = min(width-i,i)
        forward = range(i,i+fill)
        backward = range(i-fill,i)
        if np.all(np.equal(puzzle[:,forward],np.fliplr(puzzle[:,backward]))):
            ret.add(i)

    return ret 

def opts_to_value(refl):
    t = 0 
    (r,c) = refl 
    for rl in r:
        t+=rl
    for rl in c:
        t+= 100*rl

    return t

def get_full_value(puzzle):
    (height,width) = puzzle.shape
    (rs,cs) = get_value(puzzle)

    locs = []
    clines = set()
    rlines = set()
    for w in range(0,width):
        for h in range(0,height):
            p = np.copy(puzzle)
            p[h,w]*=-1
            (rt,ct) = get_value(p)
            if len(rt-rs) or len(ct-cs) and len(rt-rs) + len(ct-cs) == 1:
                locs.append((h,w))
                clines.update(ct-cs)
                rlines.update(rt-rs)


    value_simp = opts_to_value((rs,cs))
    value_smudge = opts_to_value((rlines,clines))

    if len(clines) + len(rlines) > 1:
        print("XXX")

    print(f"{(rs,cs)} {(rlines,clines)}  {value_simp} {value_smudge} {locs}")

    return (value_simp,value_smudge)
    


def solve(): 

    with open(input_file,'r') as f:
        puzzles = []
        accum = []
        for link in f.readlines():
            if link.strip() == "":
                if accum:
                    puzzles.append(np.array(accum))
                accum = []
                continue

            accum.append(np.array([int(1) if l=='#' else int(-1) for l in list(link.strip())]))

        puzzles.append(np.array(accum))
           
        total_simple= 0
        total_smudge = 0 
        for p in puzzles:
            (simple,smudge) =  get_full_value(p)
            total_simple += simple
            total_smudge += smudge
        print(total_simple)
        print(total_smudge)





if __name__ == "__main__":
    solve()