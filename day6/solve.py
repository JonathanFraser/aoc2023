import os 

import math
folder = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(folder,"input.txt")

def evaluate(t,tpress):
    return (t-tpress)*tpress

def compute_combos(t,d):
    disc = math.sqrt((t/2.0)**2 - d)
    left = t/2.0-disc 
    right = t/2.0+disc 
    lefti = round(left)
    righti = round(right)
    lefti = lefti if evaluate(t,lefti) > d else lefti+1
    righti = righti if evaluate(t,righti) > d else righti - 1
    combos = righti-lefti+1
    return combos


def solve(): 

    with open(input_file,'r') as f:
        ret = {}
        kern = {}
        for line in f.readlines():
            (label,values) = line.split(':')

            ret[label]=[int(v) for v in values.strip().split(' ') if v != ' ' and v != '']
            kern[label]=int(values.strip().replace(' ',''))

        print(kern)

        total = 1
        for (t,d) in zip(ret['Time'],ret['Distance']):
            total *= compute_combos(t,d)

        print(total)
        print(compute_combos(kern['Time'],kern['Distance']))
           

if __name__ == "__main__":



    solve()