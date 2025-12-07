import math
import os

# Parse input file
input = open(os.path.dirname(os.path.realpath(__file__)) + '/day7_input.txt')
lines = input.readlines()
input.close()
lines = [line.strip() for line in lines]

# Find where the starting beam comes from
S = lines[0].find("S")

# As we go down level by level, track the number of overlapping beams in each column, starting with 1 beam in the middle
beams = dict()
beams[S] = 1

# Counter for part 1
splits = 0

# Skip the first 2 lines (The first line only has the S and the second line is blank)
for x in range(2, len(lines)):

    # Building a new dictionary for each level
    new_beams = dict()
    columns = beams.keys()

    # For each beam we are tracking, check if it hit a splitter or not
    for col in columns:

        # If we hit a splitter with 5 beams, for example, then 5 go left and 5 go right
        if lines[x][col] == "^":
            splits += 1
            if col - 1 not in new_beams:
                new_beams[col - 1] = 0
            if col + 1 not in new_beams:
                new_beams[col + 1] = 0
            # It's possible more than 1 set of beams join together in the same column, so add them together
            new_beams[col - 1] += beams[col]
            new_beams[col + 1] += beams[col]

        # If we didn't hit a splitter, just move the beams down to the next level
        else:
            if col not in new_beams:
                new_beams[col] = 0
            new_beams[col] += beams[col]
    beams = new_beams

print("The number of times the beams were split is", splits)
print("The number of timelines the particle would end up on is", sum(beams.values()))