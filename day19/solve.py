import os 
import math
import numpy as np
from scipy.linalg import null_space
import scipy.sparse as sp
import queue
import copy
from typing import List
import pprint
from dataclasses import dataclass,field
folder = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(folder,"input.txt")

keys = ['x','m','a','s']
def total_part(part: dict):
    return sum(part.values())

def in_options(opts,part):
    for o in opts:
        is_in = True 
        for (k,value) in part.items():
            if value > o[k][1]:
                is_in = False 
                break 

            if value < o[k][0]:
                is_in = False
                break

        if is_in:
            return True
    return False

def opt_calc(opt):
    o = 1 
    for k in keys:
        (srt,end) = opt[k]
        o *= (end-srt+1)
    return o 
        
def run_part_match(rule,part_match):
    outputs = []
    remainder = copy.deepcopy(part_match)
    for (match,tgt) in rule:
        if remainder is None:
            continue 

        if match is None:
            outputs.append((tgt,remainder))
            remainder = None 
            continue 

        (key,dir,val) = match 

        keep = None 
        rej = None 

        (srt,end) = remainder[key]

        if dir == '>':
            keep = (val+1,end)
            rej = (srt,val)

        if dir == '<':
            keep = (srt,val-1)
            rej = (val,end)

        (ksrt,kend) = keep
        if ksrt <= kend and ksrt >= srt and kend <= end:
            new_out = copy.deepcopy(remainder)
            new_out[key]=keep
            outputs.append((tgt,new_out))

        (rsrt,rend) = rej 
        if rsrt <= rend and rsrt >= srt and rend <= end:
            remainder[key]=rej
        else:
            remainder = None

    return outputs 

        
def run_part_matches(rules):
    run_set = [("in",{'x':(1,4000),'m':(1,4000),'a':(1,4000),'s':(1,4000),"seen":[]})]
    accepted = []
    while len(run_set):
        (tgt,options) = run_set[0]
        options['seen'].append(tgt)
        run_set = run_set[1:]
        rule = rules[tgt]
        results = run_part_match(rule,options)
        for (t,o) in results:
            if t == "A":
                accepted.append(o)
                continue 
            if t == "R":
                continue 
            run_set.append((t,o))

    return accepted

def construct_rule(str):
    end = str.find(":")
    key = str[0]
    dir = str[1]
    val = int(str[2:end])
    tgt = str[end+1:]

    return ((key,dir,val),tgt)
    
    

def solve(): 
    with open(input_file,'r') as f:
        parts = []
        rules = {}
        for link in f.readlines():
            if link[0] == '{':
                p = {}
                for d in link.strip()[1:-1].split(','):
                    (k,v) = d.split('=')
                    p[k]=int(v)
                parts.append(p)
                continue

            if link.strip() == "":
                continue

            rem = link.strip()
            idx = rem.find('{')
            name = rem[:idx]
            cond = rem[idx+1:-1]
            rule_step = []
            step_strings = cond.split(',')
            for c in step_strings[:-1]:
                rule_step.append(construct_rule(c))

            rule_step.append((None, step_strings[-1]))
            rules[name] =rule_step

        opts =  run_part_matches(rules)
        accepted_parts = [p for p in parts if in_options(opts,p)]
        print(sum([total_part(p) for p in accepted_parts]))
        print(sum([opt_calc(o) for o in opts]))



    
        
            

            


        




            




if __name__ == "__main__":

    solve()