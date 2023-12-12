import os 
import math
from typing import List
folder = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(folder,"input.txt")


def memoize(fnc):
    cache = {}
    def wrapper(state,groups,must_match="?.#"):
        key = ("".join(state),",".join([str(g) for g in groups]),must_match)
        if key in cache:
            return cache[key]
        res = fnc(state,groups,must_match=must_match)
        cache[key]=res
        return res
    return wrapper

@memoize
def options(state,groups,must_match='?.#'):
    if len(state) == 0:
        if len(groups):
            return 0
        else:
            return 1
        
    if len(groups) == 0:
        if "#" in state:
            return 0
        else:
            return 1
    
    if state[0] not in must_match:
        return 0 
    
    if groups[0] == 1: #first group is of length 1
        if state[0] == '.':
            return options(state[1:],groups) #eat the working gear
        if state[0] == '#':
            return options(state[1:],groups[1:],must_match='.?') #match the broken gear and consume group
        
        if state[0] == '?':
            t = 0
            if '.' in must_match:
                t +=  options(state[1:],groups) # assume next is '.' and carry forward
            if '#' in must_match:
                t += options(state[1:],groups[1:],must_match='.?') # assume next is '#' and carry forward
            return t
    else:
        if state[0] == '.':
            return options(state[1:],groups) #eag working gear, don't touch groups
        if state[0] == '#':
            return options(state[1:],[groups[0]-1]+groups[1:], must_match="?#")
        if state[0] == '?':
            t = 0
            if '.' in must_match:
                t += options(state[1:],groups)
            if '#' in must_match:
                t += options(state[1:],[groups[0]-1]+groups[1:], must_match="?#")
            return  t
        
    raise RuntimeError(f"WTF: {state} groups")
        
    


    

def solve(): 

    with open(input_file,'r') as f:
        m = 0
        mult = 0
        for link in f.readlines():
            (states,keys) = link.strip().split(' ')
            grps = [int(k.strip()) for k in keys.split(',')]
            m += options(list(states),grps)
            expand_options = "?".join(5*[states])
            expand_groups = 5*grps
            mult += options(list(expand_options),expand_groups)
            
        print(m)
        print(mult)






if __name__ == "__main__":
    solve()