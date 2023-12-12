import os 
import numpy as np 
from typing import List
folder = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(folder,"input.txt")


def solve(): 

    with open(input_file,'r') as f:
        galaxies = set()
        rows_seen = set()
        cols_seen = set()
        rows = set()
        cols = set()
        for (j,link) in enumerate(f.readlines()):
            for (i,c) in enumerate(link.strip()):
                rows.add(j)
                cols.add(i)
                if c == "#":
                    rows_seen.add(j)
                    cols_seen.add(i)
                    galaxies.add((j,i))

        row_expand = rows - rows_seen
        col_expand = cols - cols_seen
        R = max(rows)+1
        C = max(cols)+1
        col_expansion = 0 
        row_expansion = 0
        
        row_map = []
        for r in range(0,R):
            if r in row_expand:
                row_expansion += 999999
            row_map.append(r+row_expansion)

        col_map = []
        for c in range(0,C):
            if c in col_expand:
                col_expansion += 999999
            
            col_map.append(c+col_expansion)

        print(row_map)

        expanded_galaxies = set()
        for (r,c) in galaxies:
            expanded_galaxies.add((row_map[r],col_map[c]))

        total = 0
        l = list(expanded_galaxies)
        for (i,(y1,x1)) in enumerate(l):
            for (y2,x2) in l[i+1:]:
                total += abs(y2-y1) + abs(x2-x1)

        print(total)
  


if __name__ == "__main__":
    solve()