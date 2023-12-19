import os 
import math
import numpy as np
from scipy.linalg import null_space
import scipy.sparse as sp
import queue 
from typing import List
from dataclasses import dataclass,field
folder = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(folder,"input.txt")

def total_part(part: dict):
    return sum(part.values())

def run_rule(rule,part):
    for (match,tgt) in rule:
        if match is None:
            return tgt 
        (key,dir,val) = match
        if dir == '>':
            if part[key] > val:
                return tgt 
        if dir == '<':
            if part[key] < val:
                return tgt
        
    raise RuntimeError("no tail case")

def run_part(rules,part):
    current_rule = "in"
    while True:
        rule = rules[current_rule]
        prev_rule = current_rule
        current_rule = run_rule(rule,part)

        if current_rule == "A":
            return total_part(part)
        
        if current_rule == "R":
            return 0 

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

        print(sum([run_part(rules,p) for p in parts]))

    
        
            

            


        




            




if __name__ == "__main__":

    solve()