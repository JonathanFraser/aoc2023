import os 

folder = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(folder,"input.txt")

symbols = ['$','#','%','+','=','/','-','*','@','&']
digits = ['0','1','2','3','4','5','6','7','8','9']
def solve(): 
    with open(input_file,'r') as f:
        symbol_locs = set()
        numbers = []
        star_locs = dict()
        for (line_idx,line) in enumerate(f.readlines()):
            line = line.strip()
            pos = 0 
            while pos < len(line):
                if line[pos] == '.':
                    pos += 1 
                    continue 

                if line[pos] in digits:
                    str_pos = pos+1
                    while str_pos < len(line) and line[str_pos] in digits:
                        str_pos+=1

                    number = int(line[pos:str_pos])
                    neighbours = []
                    neighbours += [(line_idx-1,r) for r in range(pos,str_pos)]
                    neighbours += [(line_idx+1,r) for r in range(pos,str_pos)]
                    neighbours += [(line_idx+l,pos-1) for l in [-1,0,1]]
                    neighbours += [(line_idx+l,str_pos) for l in [-1,0,1]]
                    pos = str_pos 
                    numbers.append((number,(line_idx,pos),set(neighbours)))
                    continue 

                symbol_locs.add((line_idx,pos))
                if line[pos] == '*':
                    star_locs[(line_idx,pos)]=[]
                pos += 1
        part_total = 0
        for (number,loc, neighbours) in numbers:
            for n in neighbours:
                if n in symbol_locs:
                    part_total += number

                if n in star_locs:
                    star_locs[n] += [number]
                   

        print(part_total)

        total = 0
        for (k,v) in star_locs.items():
            if len(v) == 2:
                total += v[0]*v[1]
        print(total)





if __name__ == "__main__":
    solve()