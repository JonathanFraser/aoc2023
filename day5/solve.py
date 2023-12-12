import os 

folder = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(folder,"input.txt")

order = ['seed-to-soil','soil-to-fertilizer','fertilizer-to-water','water-to-light','light-to-temperature','temperature-to-humidity','humidity-to-location']

def get_location(map,m):
    mapped_ranges = [m]
    for o in order:
        ranges = map[o]
        new_ranges = []
        for m in mapped_ranges:
            new_ranges += compute_through(ranges,m)
        mapped_ranges = new_ranges

    return mapped_ranges


def split_ranges(map_range,input_range):
    (dst_start,src_start,length) = map_range 
    (start,rlength) = input_range

    if rlength <= 0:
        raise RuntimeError(f"received invalid range {input_range}")

    new_inputs = []
    new_outputs = []

    input_end = start+rlength 
    range_end = src_start+length 
    if start >= range_end:
        #input range is right of test range
        return ([input_range],[])

    if src_start >= input_end:
        #input range is to the left of test range
        return ([input_range],[])


    if input_end > range_end:
        new_inputs.append((range_end,input_end-range_end))
        rlength = range_end-start
        input_end = range_end 

    if start < src_start:
        new_inputs.append((start,src_start-start))
        rlength = input_end - src_start
        start = src_start 

    if rlength > 0:
        new_outputs.append((dst_start + (start-src_start), rlength))

    return(new_inputs,new_outputs)

def compute_through(ranges,input_range):
    input_ranges = [input_range]
    output_ranges = []
    for range in ranges:
        new_inputs = []
        for ir in input_ranges:
            (inputs,outputs) = split_ranges(range,ir)
            if outputs:
                print(f"split range {ir} into {(inputs,outputs)} by rule {range}")
            new_inputs.extend(inputs)
            output_ranges.extend(outputs)
        input_ranges = new_inputs
        
    return output_ranges+input_ranges


def solve(): 
    seeds = []
    maps = dict()
    mode = ""
    with open(input_file,'r') as f:

        for line in f.readlines():
            l = line.strip()
            if l.startswith("seeds:"):
                seeds =[int(s) for s in l[6:].strip().split(' ')]
                continue 

            if 'map' in l:
                mode = l[:-5]
                continue

            if len(l) > 0 and l[0] in ['0','1','2','3','4','5','6','7','8','9']:
                map = [int(c) for c in l.split(' ')]
                cur_map = maps.get(mode,[]) 
                cur_map += [(map[0],map[1],map[2])]
                maps[mode]=cur_map
                continue

    location_ranges = []
    for s in seeds: 
        location_ranges.extend(get_location(maps,(s,1)))

    print(min([l[0] for l in location_ranges]))

    print(seeds)
    seed_start = seeds[::2]
    seed_length = seeds[1::2]
    seed_ranges = list(zip(seed_start,seed_length))
    print(seed_ranges)
    location_ranges = []
    for r in seed_ranges:
        print(f"process: {r}")
        location_ranges.extend(get_location(maps,r))

    print(min([l[0] for l in location_ranges]))


if __name__ == "__main__":



    solve()