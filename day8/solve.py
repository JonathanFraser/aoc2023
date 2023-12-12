import os 
from math import gcd
folder = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(folder,"input.txt")

def walk(start,keep_going,collection,instructions):
        counter = 0
        location = start
        while keep_going(location):
            instruction = instructions[counter % len(instructions)]
            (l,r) = collection[location]
            if instruction == 'L':
                location = l 
            else: 
                location = r
            
            counter += 1

        return counter

def compute_lcm(arr):
    val = 1
    for v in arr:
        val = val*v // gcd(val,v)
    return val 

def solve(): 

    with open(input_file,'r') as f:
        instructions = f.readline().strip()
        f.readline()
        collection = {}
        for link in f.readlines():
            (start,paths) = link.split('=')
            (left,right) = paths.replace('(','').replace(')','').strip().split(',')
            collection[start.strip()]=(left.strip(),right.strip())


        counter = walk("AAA",lambda x: x != 'ZZZ',collection,instructions)

        path_lengths = []
        for start in collection.keys():
            if not start.endswith('A'):
                continue
             
            length = walk(start,lambda x: not x.endswith('Z'),collection,instructions)
            path_lengths.append(length)
    

    print(counter)
    print(compute_lcm(path_lengths))
            

if __name__ == "__main__":
    solve()