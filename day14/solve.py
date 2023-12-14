import os 
import math
import numpy as np
from scipy.linalg import null_space
import scipy.sparse as sp
folder = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(folder,"input.txt")

def ripple(line):
    left = 0 
    right = 1
    while right < len(line):
        if line[left] == 'O' or line[left] == '#':
            left += 1
            right = left + 1
            continue

        if line[right] == '#':
            left = right 
            right = right + 1
            continue 
        
        if line[right] == '.':
            right += 1
            continue 
        
        line[left] = 'O'
        line[right] ='.'
    return line

def compute_load(array):
        weights =   (np.array(range(0,array.shape[0]))+1)[::-1]
        total = 0
        for i in range(0,array.shape[1]): 
            total += np.sum(weights[np.equal(array[:,i],'O')])

        return total
 

def tilt_north(array):
    for i in range(0,array.shape[1]):
        ripple(array[:,i])

def tilt_south(array):
    for i in range(0,array.shape[1]):
       ripple(array[::-1,i])

def tilt_west(array):
    for i in range(0,array.shape[0]):
        ripple(array[i,:])

def tilt_east(array):
    for i in range(0,array.shape[0]):
        ripple(array[i,::-1])

def spin(array):
    tilt_north(array)
    tilt_west(array)
    tilt_south(array)
    tilt_east(array)

def solve(): 
    with open(input_file,'r') as f:
        lines = []
        for link in f.readlines():
            lines.append([l for l in link.strip()])

        
        array = np.array(lines)
        start = array.copy()

        tilt_north(array)

        print(compute_load(array))

        start_key = str(list(start.flatten()))
        keys = [start_key]
        cache = {start_key:0}
        for i in range(1,1000000000):
            spin(array)
            key = str(list(array.flatten()))
            if key in cache:
                break  
            cache[key]=i
            keys.append(key)


        print(f"current i: {i}")
        print(f"previous instance {cache[key]}")
        N = i - cache[key]
        rem = (1000000000-cache[key]) % N
        print(f"cycle size: {N}")
        print(f"new length: {rem}")
        print(f"truncated cycles: {rem+cache[key]}")
        new = start.copy()
        for i in range(0,rem+cache[key]):
            spin(new)


        print(compute_load(new))





if __name__ == "__main__":
    solve()