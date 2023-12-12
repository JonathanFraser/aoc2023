import os 
import numpy as np 
from typing import List
folder = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(folder,"input.txt")


def add_connection(db,loc,curr):
    cons : list = db.get(loc,[])
    cons.append(curr)
    db[loc] = cons
    return db

def winding_number(loc,path,path_set):
    (y,x) = loc
    winding = 0
    for i in range(1,y+1):
        test_loc = (y-i,x+i)
        if test_loc in path_set:
            path_pos = [i for (i,c) in enumerate(path) if c == test_loc][0]
            path_next = (path_pos +1) % len(path)
            path_prev = (path_pos -1) % len(path)
            (yn,xn) = path[path_next]
            (yp,xp) = path[path_prev]
            next_right = (xn > x+i) or (yn > y-i)
            prev_right = (xp > x+i) or (yp > y-i)

            if next_right == prev_right:
                #stayed in quandrant, did not cross
                continue 

            if next_right:
                winding += 1
            
            if prev_right:
                winding -= 1

    return winding





def solve(): 

    with open(input_file,'r') as f:
        connections = {}
        back_connections = {}
        start = None 
        ground = []
        for (j,link) in enumerate(f.readlines()):
            for (i,c) in enumerate(link.strip()):
                north = (j-1,i)
                south = (j+1,i)
                west = (j,i-1)
                east = (j,i+1)
                center = (j,i)

                lookup = {
                    "|": [north,south],
                    "-": [east,west],
                    "L": [north,east],
                    "J": [north,west],
                    "7": [south,west],
                    ".": [],
                    "F": [south,east],
                }

                if c == "S":
                    start = center 
                    continue 

                if c == ".":
                    ground.append(center)
                    continue 


                paths = lookup[c]
                for p in paths:
                    connections = add_connection(connections,center,p)
                    back_connections = add_connection(back_connections,p,center)

        height = j+1
        width = i+1

        distances = {}
        seen = set()
        seen.add(start)
        distances[0] = [start]
        current_distance = 0
        connections[start]=back_connections[start]
        while distances[current_distance]:
            next_distance = []
            for p in distances[current_distance]:
                for n in connections.get(p,[]):
                    if n not in seen:
                        seen.add(n)
                        next_distance.append(n)
            if not next_distance:
                break
            distances[current_distance+1]=next_distance
            current_distance+=1

        
        path = [start]
        next = connections[start][0]
        while True:
            path.append(next)
            options = [c for c in connections[next] if c not in path]
            if not options:
                break
            next = options[0]

        print(len(path))

        path_set = set(path)


        interior = []

        for y in range(0,height):
            for x in range(0,width):
                if (y,x) in path_set:
                    continue

                if winding_number((y,x),path,path_set):
                    interior.append((y,x))

        print(len(interior))






        
    

            







 
        

if __name__ == "__main__":
    solve()