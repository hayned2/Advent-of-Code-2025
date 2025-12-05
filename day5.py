import os

# Parse input file
input = open(os.path.dirname(os.path.realpath(__file__)) + '/day5_input.txt')
lines = input.readlines()
input.close()
lines = [line.strip() for line in lines]

ranges = True
ranges_list = []
sum = 0
for line in lines:
    # Input Parsing First Section - Get the ranges of fresh ingredients
    if ranges:
        if '-' not in line:
            ranges_list.sort()
            ranges = False
            continue
        span = [int(val) for val in line.split("-")]
        ranges_list.append(span)
    # Input Parsing Second Section - Check if each ingredient is in a fresh range
    else:
        for span in ranges_list:
            id = int(line)
            if id >= span[0] and id <= span[1]:
                sum += 1
                break

print("The number of ingredient IDs provided that are 'fresh' is:", sum)

index = 0
while True:
    # Merge overlapping ranges (and merge adjacent ranges like 3-5, 5-10 into 3-10)
    if ranges_list[index][1] >= ranges_list[index + 1][0]:
        a = ranges_list[index][0]
        b = max(ranges_list[index][1], ranges_list[index + 1][1])
        ranges_list.pop(index)
        ranges_list[index] = [a, b]
        continue
    index += 1
    # Detect when we've combined all of the overlapping ranges
    if index == len(ranges_list) - 1:
        break

# Count the number of IDs the ranges cover
sum2 = 0
for span in ranges_list:
    sum2 += span[1] - span[0] + 1

print("The number of fresh ingredient IDs considered 'fresh' is:", sum2)