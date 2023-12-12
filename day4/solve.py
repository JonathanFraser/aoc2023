import os 

folder = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(folder,"input.txt")

symbols = ['$','#','%','+','=','/','-','*','@','&']
digits = ['0','1','2','3','4','5','6','7','8','9']
def solve(): 
    with open(input_file,'r') as f:
        cards = {}
        card_max = 0
        for (line_idx,line) in enumerate(f.readlines()):
            line = line.strip()
            (label,game) = line.split(':')
            (winning,yours) = game.split('|')
            yours = [int(n) for n in yours.strip().split(' ') if n != ' ' and n != '']
            winning = set([int(n) for n in winning.strip().split(' ') if n != ' ' and n != ''])
            num_common = len([i for i in yours if i in winning])
            value = 0
            if num_common > 0:
                value = 2**(num_common-1)
            game_number = int(label[5:])
            cards[game_number] = (num_common,value)
            card_max = game_number


        total = 0
        total_copies = 0
        copies = [1 for _ in range(0,card_max)]
        for c in range(0,card_max):
            game_idx = c+1
            total += cards[game_idx][1]

            current_copies = copies[c]
            total_copies += current_copies
            matches = cards[game_idx][0]
            for m in range(c+1,c+matches+1):
                if m >= card_max:
                    break
                copies[m] += current_copies

        print(total)
        print(total_copies)  





if __name__ == "__main__":
    solve()