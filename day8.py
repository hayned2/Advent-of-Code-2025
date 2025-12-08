import os
import math

# Parse input file
input = open(os.path.dirname(os.path.realpath(__file__)) + '/day8_input.txt')
lines = input.readlines()
input.close()
lines = [line.strip() for line in lines]

# Dictionary #1 - Maps a junction box to the junction number it belongs to
box_map = dict()
# Dictionary #2 - Maps a junction number to the boxes it contains
junctions = dict()
val = 0
# Start by parsing the input and putting each box into its own junction
for line in lines:
    pos = tuple([int(val) for val in line.split(',')])
    box_map[pos] = val
    junctions[val] = set([pos])
    val += 1

# Helper function to get the distance (squared distance, since we only care about relative distances)
def get_distance(box1, box2):
    return abs(((box1[0] - box2[0]) ** 2) + ((box1[1] - box2[1]) ** 2) + ((box1[2] - box2[2]) ** 2))

# Dictionary #3 - Maps a pair of junction boxes to their distances. Do this once so we don't have to keep recalculating
distances = dict()
for box1 in box_map.keys():
    for box2 in box_map.keys():
        # Don't join the same box to itself and don't duplicate box distances (A, B) and (B, A)
        if box1 == box2 or (box2, box1) in distances:
            continue
        distance = get_distance(box1, box2)
        distances[(box1, box2)] = distance
# Sort the pairs by shortest distances, now we know what order to connect the boxes in
distances = sorted(distances, key = distances.get)

# Helper function for combining junction boxes
def combine_boxes(box1, box2, box_map, junctions):
    # If they are already in the same junction, no further logic required
    if box_map[box1] == box_map[box2]:
        return box_map, junctions
    # If they are in two different junctions, combine them into one junction in Dicts #1 and #2
    new_map_value = min(box_map[box1], box_map[box2])
    old_map_value = max(box_map[box1], box_map[box2])
    for boxn in junctions[old_map_value]:
        box_map[boxn] = new_map_value
        junctions[new_map_value].add(boxn)
    # Remove the old junction, we don't need it anymore
    del junctions[old_map_value]
    return box_map, junctions

# Limit = 10 for the example, 1000 for the real input
limit = 1000
# Link together the closest boxes for Part 1
for x in range(limit):
    (box1, box2) = distances[x]
    box_map, junctions = combine_boxes(box1, box2, box_map, junctions)

# Grab the sizes of the 3 largest junctions and multiply them
sizes = sorted((len(junction) for junction in junctions.values()), reverse = True)[:3]
print("The result of the 3 largest junction sizes multiplied together is", math.prod(sizes))

# Part 2 - Keep connecting boxes until they are all on the same junction
while True:
    (box1, box2) = distances[limit]
    box_map, junctions = combine_boxes(box1, box2, box_map, junctions)
    if len(junctions) == 1:
        print("The result of multiplying the last two junction boxes' X coordinates is", box1[0] * box2[0])
        break
    limit += 1
