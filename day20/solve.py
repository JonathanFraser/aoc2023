import os 
import math
import numpy as np
from scipy.linalg import null_space
import scipy.sparse as sp
import queue 
import copy
from typing import List
from dataclasses import dataclass,field
folder = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(folder,"input.txt")
def contains(pulses):
    for (to_node,from_node,dir) in pulses:
        if to_node == "rx" and not dir:
            return True 
        
    return False 
    
def save_state(mem):
    return  "".join(['x' if m else 'o' for m in mem])

def load_state(mem):
    return [m=='x' for m in mem]

def evaluate(pulses):
    up=0
    down=0
    for (_,_,d) in pulses:
        if d:
            up+=1
        else:
            down+=1

    return (up,down)

def scale(p,n):
    (u,d) = p 
    return (u*n,d*n)

def aggregate(res):
    u=0
    d=0
    for (up,dp) in res:
        u+=up
        d+=dp 

    return (u,d)

def step(machine,state,pulse):
    state = copy.deepcopy(state)
    (to_node,from_node,dir) = pulse
    if to_node not in machine:
        return (state,[])
    
    desc = machine[to_node]


    if desc['type'] == 'broad':
        return (state,[(o,to_node,dir) for o in desc['outputs']])

    mem_ptr = desc['index']

    if desc['type'] == 'flip':
        if dir:
            return (state,[])
        
        state[mem_ptr] = not state[mem_ptr]
        return (state,[(o,to_node,state[mem_ptr]) for o in desc['outputs']])
    
    inputs = desc['inputs']
    input_len = len(inputs)
    
    if desc['type'] == 'conj':
        state[mem_ptr + inputs[from_node]] = dir 
        all_high = all(state[mem_ptr:(mem_ptr+input_len)])
        return (state,[(o,to_node,not all_high) for o in desc['outputs']])
    
    raise RuntimeError(f"unknown type {desc['type']}")



def push_button(machine,state):
    pointer = 0
    pulses = [("broadcaster","button",False)]

    while pointer < len(pulses):
        pulse = pulses[pointer]
        (new_state,new_pulses) = step(machine,state,pulse)   
        pulses += new_pulses 
        state = new_state
        pointer += 1 

    return (state,pulses)



def solve(): 
    with open(input_file,'r') as f:
        machine = {}
        input_map = {}
        for link in f.readlines():
            (name,lst) = link.strip().split('-')
            name = name[:-1]
            if name != "broadcaster":
                typ = "flip" if name[0] == '%' else 'conj'
                name = name[1:]
            if name == "broadcaster":
                typ = "broad"
                name = "broadcaster"

            outputs = [l.strip() for l in lst[2:].split(',')]
            for o in outputs:
                inputs = input_map.get(o,[])
                inputs.append(name)
                input_map[o]=inputs

            machine[name]={
                'type':typ, 
                'outputs':outputs,
            }

        state = []
        for (k,v) in machine.items():
            if v['type'] =='flip':
                machine[k]['index']=len(state)
                state.append(False)
            
            if v['type'] == 'conj':
                machine[k]['inputs']={input:i for (i,input) in enumerate(input_map[k])}
                machine[k]['index']=len(state)
                state+=[False for k in input_map[k]]



        print(machine)
        seen = dict()
        seen[save_state(state)]=0
        states = [state]
        results = []
        looped=False
        N=1000
        while len(states) <= 100000:
            (new_state,pulses) = push_button(machine,state)
            if contains(pulses):
                print("sent:", len(states))

            res = evaluate(pulses)
            results.append(res)

            if save_state(new_state) in seen:
                looped=True
                break

            states.append(new_state)
            seen[save_state(new_state)]=len(states)-1
            state = new_state

        if not looped:
            print(len(results))
            (u,d) = aggregate(results)
            print(u*d)
            quit()

        loop_point = seen[save_state(new_state)]
        loop_size = len(states[loop_point:])
        loop_remainder = (N-loop_point) % loop_size
        loop_factor = (N-loop_point - loop_remainder) // loop_size
        loop_prelude = results[:loop_point]
        loop = results[loop_point:]
        loop_tail = results[loop_point:(loop_point+loop_remainder)]
        print(loop_size,loop_point,loop_remainder)
        (u,d) = aggregate([aggregate(loop_prelude), scale(aggregate(loop),loop_factor), aggregate(loop_tail)])
        print(u*d)






if __name__ == "__main__":

    solve()