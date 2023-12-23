import numpy as np

with open("day18_input.txt") as f:
    instructions = [line.split(" ") for line in f.read().splitlines()]
    
directions = {
    "R": (0, 1),
    "L": (0, -1),
    "D": (1, 0),
    "U": (-1, 0)
}

current = (0, 0)
coords = [current]
for direction, dist, _ in instructions:
    vector = directions[direction]
    for i in range(int(dist)):
        current = (current[0] + vector[0], current[1] + vector[1])
        coords.append(current)
        
# Now rasterize edge
min_c = np.asarray((min(c[0] for c in coords), min(c[1] for c in coords)))
max_c = np.asarray((max(c[0] for c in coords), max(c[1] for c in coords)))
grid = np.zeros((max_c - min_c + (1, 1)), dtype=np.uint8)
for c in coords:
    grid[tuple(np.asarray(c) - min_c)] = 1

# And fill the exterior
def set_top_edge_if_zero(arr, val):
    """Set the top edge of arr to val if zero"""
    for i in range(arr.shape[1]):
        if arr[0, i] == 0:
            arr[0, i] = val
        
def set_all_edges_if_zero(arr, val):
    """Set all edges of arr to val if zero"""
    set_top_edge_if_zero(arr, val)
    set_top_edge_if_zero(np.flipud(arr), val)
    set_top_edge_if_zero(arr.T, val)
    set_top_edge_if_zero(np.flipud(arr.T), val)

def match_fill_forward_pass(arr, val):
    """Fill in any 0 adjacent to val (left or above of it) with val"""
    for i in range(1, arr.shape[0] - 1):
        for j in range(1, arr.shape[1] - 1):
            if arr[i, j] == 0 and (arr[i, j-1] == val or arr[i-1, j] == val):
                arr[i, j] = val

def fill_exterior(arr, outside_val):
    """Fill exterior of arr outside the boundary (zeroes attached to edge) with outside_val
    Return count of elements that are not outside"""
    set_all_edges_if_zero(arr, outside_val)

    # Do a forward (top-bottom, left-right) pass first, then a reverse pass, until no change
    last_count = 0
    while True:
        match_fill_forward_pass(arr, outside_val)
        match_fill_forward_pass(np.flipud(np.fliplr(arr)), outside_val)
        count = np.count_nonzero(arr != outside_val)
        if last_count == count:
            break
    
        last_count = count
    
    return last_count

print(f"Part 1: {fill_exterior(grid, 255)}")

current = (0, 0)
coords = [current]
for _, _, color in instructions:
    dist = int(color[2:7], 16)
    vector = directions[{"0": "R", "1": "D", "2": "L", "3": "U"}[color[7]]]
    current = (current[0] + vector[0] * dist, current[1] + vector[1] * dist)
    coords.append(current)

# Adjust so lowest coord is at (0, 0) and reframe as unique grid coords
# Each grid "square" could be 1 wide or high if it's trench, otherwise much bigger
min_c = np.asarray((min(c[0] for c in coords), min(c[1] for c in coords)))
coords = [(c[0] - min_c[0], c[1] - min_c[1]) for c in coords]
unique_x = sorted({c[0] for c in coords}.union({c[0] + 1 for c in coords}))
unique_y = sorted({c[1] for c in coords}.union({c[1] + 1 for c in coords}))
x_map = {x: i for i, x in enumerate(unique_x)}
y_map = {y: j for j, y in enumerate(unique_y)}
x_sizes = [unique_x[i+1] - unique_x[i] for i in range(len(unique_x) - 1)]
y_sizes = [unique_y[i+1] - unique_y[i] for i in range(len(unique_y) - 1)]

# Rasterize edge against this new grid with variable-area pixels
grid = np.zeros((max(x_map.values()) + 1, max(y_map.values()) + 1), dtype=np.uint8)
prev_x, prev_y = x_map[coords[0][0]], y_map[coords[0][1]]
grid[prev_x, prev_y] = 1
for c in coords[1:]:
    x, y = x_map[c[0]], y_map[c[1]]
    vx, vy = x - prev_x, y - prev_y
    vector_len = max(abs(vx), abs(vy))
    uvx, uvy = vx // vector_len, vy // vector_len
    for i in range(vector_len):
        grid[prev_x + i * uvx, prev_y + i * uvy] = 1
        
    prev_x, prev_y = x, y

fill_exterior(grid, 255)

# Now count the non-outside elements, multiplying each by its area
total_size = 0
for ind in np.ndindex((grid.shape[0] - 1, grid.shape[1] - 1)):
    if grid[ind] != 255:
        total_size += x_sizes[ind[0]] * y_sizes[ind[1]]

print(f"Part 2: {total_size}")
