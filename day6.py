import math
import os

# Parse input file
input = open(os.path.dirname(os.path.realpath(__file__)) + '/day6_input.txt')
lines = input.readlines()
input.close()
lines[-1] += "\n"

# Grab the operations on the bottom line
signs = lines[-1].split()

# Initialize products and sums for each operation
mults = [1] * len(lines[0].split())
sums = [0] * len(lines[0].split())
total = 0
for line in lines[:-1]:
    line = line.split()
    # As we go through each number, add or multiply it to its corresponding value
    for x in range(len(line)):
        value = int(line[x])
        if signs[x] == "*":
            mults[x] *= value
        else:
            sums[x] += value

# Tally our results. Make sure we don't count products that we initialized to 1
total = sum([mult for mult in mults if mult > 1]) + sum(sums)
print("The grand total of the normal arithmetic problem answers is:", total)

# Time for part two
width = len(lines[0])
height = len(lines) - 1
operation_index = 0
total2 = 0
values = []
for y in range(0, width):
    value = ""
    """
    Read from top-left going down each column
    123
     45  -- Gets read as "1  ", "24 ", "356"
      6
    """
    for x in range(0, height):
        value += lines[x][y]
    # Once we hit a blank column (or the last column), perform the operation
    if value.isspace() or y == width + 1:
        if signs[operation_index] == "*":
            total2 += math.prod(values)
        else:
            total2 += sum(values)
        # Reset our tracked values and increment which operation we're doing next
        values = []
        operation_index += 1
    else:
        values.append(int(value))
print("The grand total of the cephalopod arithmetic problem answers is:", total2)