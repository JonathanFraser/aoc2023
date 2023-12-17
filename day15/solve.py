import os 
import math
import numpy as np
from scipy.linalg import null_space
import scipy.sparse as sp
folder = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(folder,"input.txt")

def hash_step(state,char):
    return ((state+char)*17)%256

def hash(line):
    line_bytes = line.encode('ascii')
    state = 0 
    for l in line_bytes:
        state = hash_step(state,l)

    return state 

def hash2(line):
    line_bytes = line.encode('ascii')
    return sum([l*17**(r+1) for (r,l) in enumerate(line_bytes[::-1])])%256


def insert_lens(box,new_label,focal_length):
    for (i,(label,length)) in enumerate(box):
        if label == new_label:
            box[i] = (new_label,focal_length)
            return box 
    
    box.append((new_label,focal_length))
    return box 

def remove_lens(box,new_label):
    remove = None 
    for (i,(label,length)) in enumerate(box):
        if label == new_label:
            remove = i 
            break 
    
    if remove is not None:
        return box[:remove]+box[remove+1:]
    
    return box

def box_power(box):
    t = 0
    for (i,(label,lens)) in enumerate(box):
        t += lens*(i+1)
    return t 

def boxes_power(boxes):
    t = 0
    for i in range(0,256):
        box = boxes.get(i,[])
        t += (i+1)*(box_power(box))

    return t 

def process_instruction(boxes,instruction):
    if instruction[-1] == '-':
        lens_label = instruction[:-1]
        box_idx = hash2(lens_label)
        box = boxes.get(box_idx,[])
        box_new = remove_lens(box,lens_label)
        boxes[box_idx]=box_new
        return boxes 
    
    if instruction[-2] == '=':
        lens_label = instruction[:-2]
        lens_focal = instruction[-1]
        box_idx = hash2(lens_label)
        box = boxes.get(box_idx,[])
        box_new = insert_lens(box,lens_label,int(lens_focal))
        boxes[box_idx]=box_new 
        return boxes 
    
    raise RuntimeError(f"incorrect instruction {instruction}")




def solve(): 
    with open(input_file,'r') as f:
        t = 0
        boxes = {}
        for link in f.readlines():
            for v in link.strip().split(','):
                t += hash2(v)
                boxes = process_instruction(boxes,v)


        print(t)
        print(boxes)
        print(boxes_power(boxes))







if __name__ == "__main__":

    solve()