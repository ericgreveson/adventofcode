import numpy as np

with open("day16_input.txt") as f:
    grid = np.asarray([list(line) for line in f.read().splitlines()])

def propagate_beam(start, direction, energised, history):
    """Fire a beam from coord in the given direction until it exits grid, marking energised"""
    next = start.copy()
    while True:
        next += direction
        if next[0] < 0 or next[1] < 0 or next[0] >= grid.shape[0] or next[1] >= grid.shape[1] \
            or (tuple(next), tuple(direction)) in history:
            return

        c = grid[tuple(next)]
        energised[tuple(next)] = 1
        history.add((tuple(next), tuple(direction)))
        if c == "-":
            if direction[0] == 0:
                pass
            else:
                propagate_beam(next.copy(), np.asarray([0, -1]), energised, history)
                propagate_beam(next.copy(), np.asarray([0, 1]), energised, history)
                return
        elif c == "|":
            if direction[1] == 0:
                pass
            else:
                propagate_beam(next.copy(), np.asarray([1, 0]), energised, history)
                propagate_beam(next.copy(), np.asarray([-1, 0]), energised, history)
                return
        elif c == "\\":
            direction = np.flip(direction)
        elif c == "/":
            direction = -np.flip(direction)
        elif c != ".":
           raise ValueError("Unknown character")

def count_tiles(start, direction):
    """Count tiles energised for a given starting edge and direction"""
    energised = np.zeros_like(grid, dtype=np.uint8)
    propagate_beam(start, direction, energised, set())
    return np.count_nonzero(energised)

print(f"Part 1: {count_tiles(np.asarray([0, -1]), np.asarray([0, 1]))}")

counts = []
for row in range(grid.shape[0]):
    counts.append(count_tiles(np.asarray([row, -1]), np.asarray([0, 1])))
    counts.append(count_tiles(np.asarray([row, grid.shape[1]]), np.asarray([0, -1])))

for col in range(grid.shape[1]):
    counts.append(count_tiles(np.asarray([-1, col]), np.asarray([1, 0])))
    counts.append(count_tiles(np.asarray([grid.shape[0], col]), np.asarray([-1, 0])))

print(f"Part 2: {max(counts)}")
