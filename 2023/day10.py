from enum import Enum

Directions = Enum('Directions', ['NORTH', 'EAST', 'SOUTH', 'WEST'])
    
with open("day10_input.txt") as f:
    grid = f.read().splitlines()

# Find start block
start = None
for i, line in enumerate(grid):
    if "S" in line:
        start = (i, line.index("S"))
        
# Find one of the first nodes connected to start
chain = [start]
came_from = None
if grid[start[0] - 1][start[1]] in ("|", "7", "F"):
    chain.append((start[0] - 1, start[1]))
    came_from = Directions.SOUTH
elif grid[start[0] + 1][start[1]] in ("|", "L", "J"):
    chain.append((start[0] + 1, start[1]))
    came_from = Directions.NORTH
else:
    chain.append((start[0], start[1] - 1))
    came_from = Directions.EAST

# Map of (symbol, came_from) to (go_to, new_came_from)
next_lookup = {
    ("|", Directions.NORTH): (Directions.SOUTH, Directions.NORTH),
    ("|", Directions.SOUTH): (Directions.NORTH, Directions.SOUTH),
    ("-", Directions.EAST): (Directions.WEST, Directions.EAST),
    ("-", Directions.WEST): (Directions.EAST, Directions.WEST),
    ("L", Directions.NORTH): (Directions.EAST, Directions.WEST),
    ("L", Directions.EAST): (Directions.NORTH, Directions.SOUTH),
    ("J", Directions.NORTH): (Directions.WEST, Directions.EAST),
    ("J", Directions.WEST): (Directions.NORTH, Directions.SOUTH),
    ("7", Directions.SOUTH): (Directions.WEST, Directions.EAST),
    ("7", Directions.WEST): (Directions.SOUTH, Directions.NORTH),
    ("F", Directions.EAST): (Directions.SOUTH, Directions.NORTH),
    ("F", Directions.SOUTH): (Directions.EAST, Directions.WEST)
}

def move(coord, direction):
    """Return a new coordinate by moving from coord in the given direction"""
    if direction == Directions.NORTH:
        return (coord[0] - 1, coord[1])
    elif direction == Directions.SOUTH:
        return (coord[0] + 1, coord[1])
    elif direction == Directions.EAST:
        return (coord[0], coord[1] + 1)
    else:
        return (coord[0], coord[1] - 1)

# Now trace the path until we get back to start
while chain[-1] != chain[0]:
    end = chain[-1]
    direction, came_from = next_lookup[(grid[end[0]][end[1]], came_from)]
    chain.append(move(end, direction))
    
print(f"Part 1: {len(chain) // 2}")

# Replace start tile with the correct connector
def get_direction(a, b):
    """Get direction from coord a to coord b"""
    if b[0] == a[0] - 1:
        return Directions.NORTH
    elif b[0] == a[0] + 1:
        return Directions.SOUTH
    elif b[1] == a[1] - 1:
        return Directions.WEST
    elif b[1] == a[1] + 1:
        return Directions.EAST
    
d_prev = get_direction(start, chain[-2])
d_next = get_direction(start, chain[1])
new_row = list(grid[start[0]])
new_row[start[1]] = {
    (Directions.NORTH, Directions.SOUTH): "|",
    (Directions.SOUTH, Directions.NORTH): "|",
    (Directions.EAST, Directions.WEST): "-",
    (Directions.WEST, Directions.EAST): "-",
    (Directions.NORTH, Directions.EAST): "L",
    (Directions.EAST, Directions.NORTH): "L",
    (Directions.NORTH, Directions.WEST): "J",
    (Directions.WEST, Directions.NORTH): "J",
    (Directions.SOUTH, Directions.EAST): "F",
    (Directions.EAST, Directions.SOUTH): "F",
    (Directions.SOUTH, Directions.WEST): "7",
    (Directions.WEST, Directions.SOUTH): "7"
}[(d_prev, d_next)]
grid[start[0]] = ''.join(new_row)

# Now count crossings to determine inside / outside
chain_tiles = set(chain)
total_inside = 0
for i, row in enumerate(grid):
    inside_loop = False
    crossing_from_south = False
    crossing_from_north = False
    output = ""
    for j, tile in enumerate(row):
        if (i, j) in chain_tiles:
            # We may have crossed the loop
            if tile == "|":
                # Indeed we have
                inside_loop = not inside_loop
            elif tile in ("L", "J"):
                # To/from the north
                if crossing_from_north:
                    # We haven't crossed
                    crossing_from_north = False
                elif crossing_from_south:
                    # We have crossed!
                    crossing_from_south = False
                    inside_loop = not inside_loop
                else:
                    # We might cross in future
                    crossing_from_north = True
            elif tile in ("7", "F"):
                # To/from the south
                if crossing_from_south:
                    # We haven't crossed
                    crossing_from_south = False
                elif crossing_from_north:
                    # We have crossed!
                    crossing_from_north = False
                    inside_loop = not inside_loop
                else:
                    # We might cross in future
                    crossing_from_south = True

            output += "*"
        elif inside_loop:
            total_inside += 1
            
print(f"Part 2: {total_inside}")
