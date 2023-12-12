import os 

folder = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(folder,"input.txt")

def find_all(repo,sub):
    if len(repo) == 0:
        return []
    
    loc = repo.find(sub)
    
    if loc == -1:
        return []
    
    retval = [loc]
    rets = find_all(repo[loc+1:],sub)
    return retval + [r+loc+1 for r in rets]

def get_digit_locs(str):
    return [(i,int(c)) for (i,c) in enumerate(str) if c in ['0','1','2','3','4','5','6','7','8','9']]

words = ["one","two","three","four","five","six","seven","eight","nine"]

def get_word_locs(str):
    retval = []
    for (j,word) in enumerate(words):
        locs = find_all(str,word)
        retval += [(l,j+1) for l in locs]
    return retval

def compute_value(locs):
    ascending = sorted(locs,key = lambda x:x[0])
    return 10*ascending[0][1] + ascending[-1][1]

def solve():
    total1 = 0
    total2 = 0 
    with open(input_file,'r') as f:
        for line in f.readlines():
            digit_locs = get_digit_locs(line)
            word_locs = get_word_locs(line)

            total1 += compute_value(digit_locs)
            total2 += compute_value(digit_locs+word_locs)

    print("part1:", total1)
    print("part2:", total2)

if __name__ == "__main__":
    solve()