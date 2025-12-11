import os


# Parse input file
input = open(os.path.dirname(os.path.realpath(__file__)) + '/day11_input.txt')
lines = input.readlines()
input.close()
lines = [line.strip() for line in lines]

# Parse the input into a dictionary of the form 'device: [output1, output2, ...]'
mapping = dict()
mapping["out"] = []
for line in lines:
    line = line.split(":")
    device = line[0]
    outputs = line[1].strip().split()
    mapping[device] = outputs

""" My naive solution. Runs fast enough for part 1, not for part 2
total_paths = 0
paths = [["you"]]
while len(paths) > 0:
    path = paths.pop()
    for output in mapping[path[-1]]:
        if output == 'out':
            total_paths += 1
            continue
        new_path = list(path)
        new_path.append(output)
        paths.append(tuple(new_path))
print(total_paths)
"""

# Time for some memoization -- if we've called this function for the same source/destination combo, shortcut it
memo = dict()
def count_paths(source, destination):

    # We've reached our destination!
    if source == destination:
        return 1
    
    # We've seen this combo before, we know the answer already
    elif (source, destination) in memo:
        return memo[(source, destination)]
    
    # Time to keep branching to each reachable machine from our source
    total = 0
    for next in mapping[source]:
        total += count_paths(next, destination)

    # Make sure to update our memo before returning the total
    memo[(source, destination)] = total
    return total

# Part 1 - From 'you' to 'out'
you_to_out = count_paths("you", "out")
print("The number of paths from 'you' to 'out' is", you_to_out)

# Part 2 - From 'svr' to 'out' that goes through 'fft' and 'dac' (in any order)
# Take the number of paths from 'svr' to 'fft', then from 'fft' to 'dac', then from 'dac' to 'out'
# Multiply those path counts together to get the total answer
svr_to_fft = count_paths("svr", "fft")
fft_to_dac = count_paths("fft", "dac")
dac_to_out = count_paths("dac", "out")

# I noticed while examining the data that there are 0 paths from 'dac' to 'fft', but I am going
# to calculate these paths anyway. But the value of dac_to_fft = 0 for my input file.
svr_to_dac = count_paths("svr", "dac")
dac_to_fft = count_paths("dac", "fft")
fft_to_out = count_paths("fft", "out")

# Add the two different acceptable path counts from 'svr' to 'out' (even if the latter is 0)
total_paths = (svr_to_fft * fft_to_dac * dac_to_out) + (svr_to_dac * dac_to_fft * fft_to_out)

print("The number of paths from 'svr' to 'out' that go through 'fft' and 'dac' is", total_paths)

print("And just to prove it to you...")
print("The number of paths from 'fft' to 'dac' is", fft_to_dac)
print("The number of paths from 'dac' to 'fft' is", dac_to_fft)
