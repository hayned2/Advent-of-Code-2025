import os

# Parse input file
input = open(os.path.dirname(os.path.realpath(__file__)) + '/day12_input.txt')
lines = input.readlines()
input.close()
lines = [line.strip() for line in lines]

# I spent 2.5h on building a space-packing algorithm that took forever to run
# only to learn that if you just assume each present takes 8 spaces, you can 
# just compare the available space under the tree and you get the right answer
fillable_spaces = 0
for line in lines:
    if "x" not in line:
        continue
    line = line.split("x")
    width = int(line[0])
    line = line[1].split(":")
    height = int(line[0])
    presents = sum([int(val) for val in line[1].strip().split(" ")])
    space = width * height // 8
    if space >= presents:
        fillable_spaces += 1
print("The number of present configurations that are possible is", fillable_spaces)
# !%@% this problem