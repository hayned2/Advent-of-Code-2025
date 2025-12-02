import os
import textwrap

# Parse input file
input = open(os.path.dirname(os.path.realpath(__file__)) + '/day2_input.txt')
lines = input.readlines()
input.close()
lines = [line.strip() for line in lines]

lines = lines[0]
sum = 0
sum2 = 0

# This is definitely not optimized, but it returns within like a minute or two, so...
def invalid_id(id):
    id = str(id)
    # Odd-length IDs can't be made of two equal halves
    if len(id) % 2 == 1:
        return False
    else:
        # Does the first half match the second half?
        value = id[0:len(id) // 2] == id[len(id) // 2:]
        return value
    
def invalid_id2(id):
    id = str(id)
    for x in range(1, len(id)):
        # Only check groups that the ID can be split into. "1212" can be split into 1 and 2 (1-2-1-2 and 12-12) but not 3
        if len(id) % x != 0:
            continue
        # Handy library I found that splits a string into equal groups. So textwrap.wrap("abcdefg", 2) = ["ab", "cd", "ef", "g"]
        listy = textwrap.wrap(id, x)
        # Turn the list into a set to remove duplicates
        setty = set(listy)
        # If the set only contains 1 unique value, then it's an invalid ID
        if len(setty) == 1:
            return True
    return False
        
for line in lines.split(','):
    ids = line.split("-")
    start = int(ids[0])
    end = int(ids[1])
    # There is definitely a way to do this without iterating through every number, but eh...
    for x in range(start, end + 1):
        if invalid_id(x):
            sum += x
        if invalid_id2(x):
            sum2 += x

print("The sum of the invalid IDs that are comprised of 2 equal parts is", sum)
print("The sum of the invalid IDs that are comprised of N equal parts is", sum2)