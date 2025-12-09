import os

# Parse input file
input = open(os.path.dirname(os.path.realpath(__file__)) + '/day9_input.txt')
lines = input.readlines()
input.close()
lines = [line.strip() for line in lines]

# Parse the input into a list of points that are tuples with integers
tiles = []
for line in lines:
    tile = line.split(",")
    tile = [int(val) for val in tile]
    tile = tuple(tile)
    tiles.append(tile)

# Calculate the areas of every bounding box between the points and save them
areas = dict()
for x in range(len(tiles)):
    for y in range(x + 1, len(tiles)):
        area = (abs(tiles[x][0] - tiles[y][0]) + 1) * (abs(tiles[x][1] - tiles[y][1]) + 1)
        areas[(tiles[x], tiles[y])] = area
areas_sorted = sorted(areas, key = areas.get, reverse = True)
print("The largest area of any rectangle we can make with these points is", areas[areas_sorted[0]])

# Create two dictionaries: for each row and each column, we want to know where the edges are
row_edges = dict()
col_edges = dict()

for n in range(len(tiles)):
    tile = tiles[n]
    # Modulo logic to link the last tile to the first tile
    next_tile = tiles[(n + 1) % len(tiles)]

    # Same x value, calculate the edge along the y-axis
    if tile[0] == next_tile[0]:
        x = tile[0]
        y1 = min(tile[1], next_tile[1])
        y2 = max(tile[1], next_tile[1])
        for y in range(y1 + 1, y2):
            if y not in row_edges:
                row_edges[y] = []
            if x not in col_edges:
                col_edges[x] = []
            row_edges[y].append(x)
            col_edges[x].append(y)

    # Same y value, calculate the edge along the x-axis
    else:
        y = tile[1]
        x1 = min(tile[0], next_tile[0])
        x2 = max(tile[0], next_tile[0])
        for x in range(x1 + 1, x2):
            if y not in row_edges:
                row_edges[y] = []
            if x not in col_edges:
                col_edges[x] = []
            row_edges[y].append(x)
            col_edges[x].append(y)

# Sort the edges in both dictionaries so we can check for edge-intersections
for edges in row_edges.values():
    edges.sort()
for edges in col_edges.values():
    edges.sort()

# Given a horizontal row from points x1 to x2, check if there are any edges between x1 and x2
def row_crosses_edge(y, x1, x2):
    for x in row_edges[y]:
        if x1 <= x <= x2:
            return True
    return False

# Given a vertical column from points y1 to y2, check if there are any edges between y1 and y2
def column_crosses_edge(x, y1, y2):
    for y in col_edges[x]:
        if y1 <= y <= y2:
            return True
    return False

# Given a point, check if it's inside the polygon
# To do this, we pick a point in the middle of the bounding box, and project a line out from it
# Arbitrarily, we are projecting towards x --> 0, since the direction doesn't matter
# We count how many times that line crosses an edge
# If it's an even number of crossings, we are outside the polygon. Odd means we are inside.
def point_inside_polygon(point):
    count = 0
    for edge in row_edges[point[1]]:
        if edge <= point[0]:
            count += 1
        else:
            break
    return (count % 2) == 1

# Starting with the largest-area bounding box, check if it's valid
rank = 0
for area in areas_sorted:
    rank += 1
    tile = area[0]
    tile2 = area[1]
    x1 = min(tile[0], tile2[0]) + 1
    x2 = max(tile[0], tile2[0]) - 1
    y1 = min(tile[1], tile2[1]) + 1
    y2 = max(tile[1], tile2[1]) - 1

    # Can't calculate an interior bounding box of a single-line, and it'll never be the biggest box anyway so skip it
    if x1 > x2 or y1 > y2:
        continue

    # Make sure none of the edges of the bounding box cross an edge
    if row_crosses_edge(y1, x1, x2):
        continue
    if row_crosses_edge(y2, x1, x2):
        continue
    if column_crosses_edge(x1, y1, y2):
        continue
    if column_crosses_edge(x2, y1, y2):
        continue

    # At this point the box is either entirely inside or entirely outside the polygon
    # Grab a point in the center of the box and make sure it's inside the polygon
    midpoint = ((x1 + x2) // 2, (y1 + y2) // 2)
    if not point_inside_polygon(midpoint):
        continue

    # We found a valid bounding box!
    print("The largest area of any rectangle we can make solely on the red and green tiles is", areas[area])
    print("This is the", str(rank) + "th largest bounding box!")
    break