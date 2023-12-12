import os 
import numpy as np 
folder = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(folder,"input.txt")

def next_value(arr):
    if np.all(arr == 0):
        return (0,0)
    (deltaf,deltal) = next_value(np.diff(arr))
    return (arr[0]-deltaf,arr[-1]+deltal) 

def solve(): 

    with open(input_file,'r') as f:
        l=0
        s=0
        for link in f.readlines():
            array = [int(l.strip()) for l in link.strip().split(' ')]
            (nf,nl) =next_value(array)
            s+=nf
            l+=nl
        
        print(l)
        print(s)
        

if __name__ == "__main__":
    solve()