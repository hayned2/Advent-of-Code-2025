import os

# Parse input file
input = open(os.path.dirname(os.path.realpath(__file__)) + '/day4_input.txt')
lines = input.readlines()
input.close()
lines = [line.strip() for line in lines]

reachable = 0
part1 = True

while True:
    reachable_pos = set()
    for x in range(len(lines)):
        for y in range(len(lines[x])):
            if lines[x][y] == '.':
                continue
            neighbors = 0
            for x2 in range(x - 1, x + 2):
                for y2 in range(y - 1, y + 2):
                    if x == x2 and y == y2:
                        continue
                    if x2 < 0 or y2 < 0 or x2 >= len(lines) or y2 >= len(lines[x]):
                        continue
                    if lines[x2][y2] == '@':
                        neighbors += 1
            if neighbors < 4:
                reachable += 1
                reachable_pos.add((x, y))
    if part1:
        print("The number of reachable rolls of paper initially is", reachable)
        part1 = False
    if len(reachable_pos) > 0:
        for pos in reachable_pos:
            lines[pos[0]] = lines[pos[0]][:pos[1]] + '.' + lines[pos[0]][pos[1] + 1:]
    else:
        break
    
print("The total number of reachable rolls of paper is", reachable)