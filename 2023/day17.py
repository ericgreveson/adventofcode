import numpy as np

from functools import partial

with open("day17_input.txt") as f:
    city = np.asarray([[int(c) for c in line] for line in f.read().splitlines()])

def neighbours(current, min_len, max_len):
    """Return set of neighbouring nodes of current. Don't return a neighbour
    going back from where we've come, or with path length in same dir > max_len.
    Also don't return a neighbour involving a turn if path length < min_len"""
    nbs = []
    if current[0] > 0 and current[2] <= 0 and current[2] > -max_len \
        and (min_len == 0 or current[3] == 0 or abs(current[3]) >= min_len):
        nbs.append((current[0] - 1, current[1], current[2] - 1, 0))
        
    if current[0] < city.shape[0] - 1 and current[2] >= 0 and current[2] < max_len \
        and (min_len == 0 or current[3] == 0 or abs(current[3]) >= min_len):
        nbs.append((current[0] + 1, current[1], current[2] + 1, 0))
        
    if current[1] > 0 and current[3] <= 0 and current[3] > -max_len \
        and (min_len == 0 or current[2] == 0 or abs(current[2]) >= min_len):
        nbs.append((current[0], current[1] - 1, 0, current[3] - 1))
        
    if current[1] < city.shape[1] - 1 and current[3] >= 0 and current[3] < max_len \
        and (min_len == 0 or current[2] == 0 or abs(current[2]) >= min_len):
        nbs.append((current[0], current[1] + 1, 0, current[3] + 1))
        
    return nbs

def dijkstra(grid, min_len=0, max_len=3):
    """Dijkstra's algorithm to find min path through grid"""
    # Coords are (row, col, path_length_rows, path_length_cols)
    visited = set()
    unvisited = {(0, 0, 0, 0)} # top left
    distances = {(0, 0, 0, 0): 0}
    while unvisited:
        coord = min([(distances[c], c) for c in unvisited], key=lambda x: x[0])[1]
        # Look at each neighbour of current coord
        cur_dist = distances[coord]
        for n in neighbours(coord, min_len, max_len):
            if n not in visited:
                unvisited.add(n)
                distances[n] = min(distances.get(n, np.inf), cur_dist + grid[(n[0], n[1])])
    
        visited.add(coord)
        unvisited.remove(coord)
    
    last = (grid.shape[0] - 1, grid.shape[1] - 1)
    return min([d for c, d in distances.items() if c[0] == last[0] and c[1] == last[1] and
                max(abs(c[2]), abs(c[3])) >= min_len])

print(f"Part 1: {dijkstra(city)}")
print(f"Part 2: {dijkstra(city, min_len=4, max_len=10)}")
