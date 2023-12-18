import os 
import math
import numpy as np
from scipy.linalg import null_space
import scipy.sparse as sp
import queue 
from typing import List
from dataclasses import dataclass,field
folder = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(folder,"test.txt")


up = (-1,0)
down = (1,0)
left = (0,-1)
right = (0,1)

dirs = [left,right,up,down]

lefts = [3,2,0,1]
rights = [2,3,1,0]
back = [1,0,3,2]

@dataclass
class PathOption:
    location : (int,int)
    current_dir : int

    def encode(self,map:np.array)-> int:
        return np.ravel_multi_index(([self.location[0]],[self.location[1]],[self.current_dir]),dimensions(map))[0]

    @classmethod
    def decode(cls,index:int, map:np.array) -> "PathOption":      
        (h,w,d) = np.unravel_index([index],dimensions(map))
        return PathOption((h[0],w[0]),d[0])

def dimensions(map:np.array) -> (int,int,int):
    return (map.shape[0],map.shape[1],4)

def total(map:np.array)->int:
    return map.shape[0]*map.shape[1]*4

def is_outside(map,option) -> bool:
    if option[0] < 0 or option[0] >= map.shape[0]:
        return True 
    
    if option[1] <0 or option[1] >= map.shape[1]:
        return True 
    
    return False 

def options(map: np.array,current_option: PathOption,ultra=False) -> List[PathOption]:
    filtered_options = []
    dst = range(1,4)
    if ultra:
        dst = range(4,11)

    o = dirs[current_option.current_dir]

    next_locs = [(current_option.location[0]+d*o[0],current_option.location[1]+d*o[1]) for d in dst]
    next_locs = [nl for nl in next_locs if not is_outside(map,nl)]
    weights = [ map[nl[0],nl[1]] for nl in next_locs]
    weights = np.cumsum(weights)
    for (nl,w) in zip(next_locs,weights):

        left = lefts[current_option.current_dir]
        right = rights[current_option.current_dir]

   
        filtered_options.append((PathOption(nl,left),w))
        filtered_options.append((PathOption(nl,right),w))

    return filtered_options

def prepare_graph(map,ultra=False):
    N = total(map)
    data = []
    idx = []
    js = []
    for i in range(0,N):
        option :PathOption = PathOption.decode(i,map)
        next = options(map,option,ultra=ultra)
        for (l,weight) in next:
            index = l.encode(map)
            data.append(weight)
            idx.append(i)
            js.append(index)

    return sp.coo_matrix((data,(idx,js)),shape=(N,N))


def solve_graph(map,ultra=False):
    mat = prepare_graph(map,ultra=ultra)
    starts = [PathOption((0,0),1).encode(map), PathOption((0,0),3).encode(map)]
    (dist,pred,source) = sp.csgraph.dijkstra(mat,directed=True,indices=starts,return_predecessors=True,min_only=True,unweighted=False)
    ends = []
    for d in range(0,4):
        ends.append(PathOption((map.shape[0]-1,map.shape[1]-1),d).encode(map))
    return min(dist[ends])

def solve(): 
    with open(input_file,'r') as f:
        lines = []
        for link in f.readlines():
            lines.append(list([int(l) for l in link.strip()]))

        map = np.array(lines,dtype=int)
 
        print(solve_graph(map))
        print(solve_graph(map,ultra=True))


if __name__ == "__main__":

    solve()