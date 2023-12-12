import os 

folder = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(folder,"input.txt")

colors = ['red','blue','green']
def process_line(line):
    (prefix,game_data) = line.split(':')
    game_number = int(prefix[5:])
    round_strs = game_data.split(';')
    rounds = []
    for r in round_strs:
        draw_strs = r.split(',')
        round = {}
        for d in draw_strs:
            dstr = d.strip()
            for c in colors:
                if dstr.endswith(c):
                    round[c] = int(dstr[:-len(c)].strip())
        rounds.append(round)
        
    return (game_number,rounds)

def isRoundConsistent(target,test):
    retval = True 
    for c in colors:
        retval = retval and (target.get(c,0) >= test.get(c,0))
    return retval 

def minRound(minset,round):
    for c in colors:
        minset[c] = max(minset.get(c,0),round.get(c,0))
    return minset

def getGamePower(rounds):
    minset = {}
    for r in rounds:
        minset = minRound(minset,r)

    value = 1
    for c in colors:
        value *= minset.get(c,0)
    return value 

def isGameConsistent(target,rounds):
    retval = True 
    for r in rounds:
        retval = retval and (isRoundConsistent(target,r))
    return retval 

def solve(): 
    with open(input_file,'r') as f:
        target = {
            'red':12,
            'green':13,
            'blue':14,
        }

        matching_game_sum=0
        power_sum = 0
        for line in f.readlines():
            (game_idx,rounds) = process_line(line)
            if isGameConsistent(target,rounds):
                matching_game_sum += game_idx
            power_sum += getGamePower(rounds)


        print("part1:",matching_game_sum)
        print("part2:",power_sum)


if __name__ == "__main__":
    solve()