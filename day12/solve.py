import os 
import math
from typing import List
folder = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(folder,"input.txt")

def memoize(fnc):
    cache = {}
    def wrapper(state,groups,group_index=None):
        key = ("".join(state),",".join([str(g) for g in groups]),group_index)
        if key in cache:
            return cache[key]
        res = fnc(state,groups,group_index=group_index)
        cache[key]=res
        return res
    return wrapper

@memoize
def options(state,groups,group_index=None):
    groups_left = len(groups) or (group_index and group_index > 0)

    if len(state) == 0:
        if groups_left:
            return 0
        else:
            return 1
        
    if not groups_left:
        if "#" in state: #no groups but broken gear, not possible no options
            return 0
        else:
            return 1 #assume all remaining is 

    if group_index == None:
        if state[0] == '#':
            return options(state[1:],groups[1:],group_index=groups[0]-1) #enter group
        
        if state[0] == '.':
            return options(state[1:],groups,group_index=None) # carry on
        
        return options(state[1:],groups[1:],group_index=groups[0]-1) + options(state[1:],groups,group_index=None)

    if group_index == 0: #we've just left a group
        if state[0] in '?.': # it needs to be a '.'
            return options(state[1:],groups,group_index=None) 
        
        return 0
    
    # we're in a group it can't be anything but '.'
    if state[0] == '.':
        return 0
    
    return options(state[1:],groups,group_index=group_index-1) # eat '#' or '?' and assume '#', shrink group


    

def solve(): 

    with open(input_file,'r') as f:
        m = 0
        mult = 0
        for link in f.readlines():
            (states,keys) = link.strip().split(' ')
            grps = [int(k.strip()) for k in keys.split(',')]
            opts = options(list(states),grps)
            m += opts
            expand_options = "?".join(5*[states])
            expand_groups = 5*grps
            mult += options(list(expand_options),expand_groups)
            
        print(m)
        print(mult)






if __name__ == "__main__":
    solve()