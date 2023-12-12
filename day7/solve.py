import os 
folder = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(folder,"input.txt")

basic_symbols = "23456789TJQKA"
joker_symbols = "J23456789TQKA"

def order_value(hand:str,joker_rules=False):
    if hand == "":
        return 0
    if joker_rules:
        value = joker_symbols.find(hand[-1])
    else:
        value = basic_symbols.find(hand[-1])
    return order_value(hand[:-1],joker_rules=joker_rules)*13+value


typ = ["H","1P","2P","3K","FH","4K","5K"]

def classify_hand(hand,joker_rules=False):
    joker_count = 0 
    if joker_rules:
        hand = hand.replace('J','')
        joker_count = 5 - len(hand)

    accum = {}
    for h in hand:
        accum[h] = accum.get(h,0)+1
    
    set_count = {}
    for v in accum.values():
        set_count[v] = set_count.get(v,0)+1

    if set_count.get(5,0) == 1:
        return 7 #five of a kind
    
    if set_count.get(4,0) ==1:
        if joker_count:
            return 7
        return 6 # four of a kind
    
    if set_count.get(3,0) == 1 and set_count.get(2,0) ==1:
        return 5 #full house
    
    if set_count.get(3,0) == 1:
        if joker_count==1:
            return 6
        if joker_count==2:
            return 7
        return 4 # three of a kind
    
    if set_count.get(2,0) == 2:
        if joker_count:
            return 5
        return 3 # two pair 
    
    if set_count.get(2,0) == 1:
        if joker_count ==1:
            return 4
        if joker_count ==2:
            return 6
        if joker_count == 3:
            return 7
        return 2 # one pair
    
    if joker_count ==1:
        return 2
    
    if joker_count ==2:
        return 4
    
    if joker_count == 3:
        return 6
    
    if joker_count == 4:
        return 7
    
    if joker_count == 5:
        return 7
    
    return 1  #high card

def value_hand(hand,joker_rules=False):
    return (classify_hand(hand,joker_rules=joker_rules),order_value(hand,joker_rules=joker_rules))

def solve(): 
    lines=0
    with open(input_file,'r') as f:
        hands = []
        for line in f.readlines():
            lines+=1
            (cards,bid) = line.strip().split(' ')
            hands.append((cards.strip(),int(bid)))

    sorted_hands = sorted(hands,key=lambda x: value_hand(x[0]))
    total = 0
    for (i,sorted_hands) in enumerate(sorted_hands):
        total += (i+1) * sorted_hands[1]
    print(total)
    sorted_hands = sorted(hands,key=lambda x: value_hand(x[0],joker_rules=True))
    for s in sorted_hands:
        hand = s[0]
        if 'J' in hand:
            print(hand, typ[classify_hand(hand,joker_rules=True)-1])
    total = 0
    for (i,sorted_hands) in enumerate(sorted_hands):
        total += (i+1) * sorted_hands[1]
    print(total)

if __name__ == "__main__":
    solve()