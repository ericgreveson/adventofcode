import numpy as np

with open("day21_input.txt") as f:
    plots = np.asarray([[{".": 0, "#": 1, "S": 2}[c] for c in l] for l in f.read().splitlines()])
    
directions = [np.asarray(x) for x in [(0, 1), (0, -1), (1, 0), (-1, 0)]]

def in_map(curr_plots, idx):
    return not (idx[0] < 0 or idx[0] >= curr_plots.shape[0] or
                idx[1] < 0 or idx[1] >= curr_plots.shape[1])
    
def take_step(curr_plots):
    next_plots = np.copy(curr_plots)
    next_plots[next_plots == 2] = 0
    for idx in np.ndindex(curr_plots.shape):
        if curr_plots[idx] == 2:
            for direction in directions:
                neighbour = tuple(idx + direction)
                if in_map(next_plots, neighbour) and next_plots[neighbour] == 0:
                    next_plots[neighbour] = 2
                    
    return next_plots

curr_plots = np.copy(plots)
for _ in range(64):
    curr_plots = take_step(curr_plots)
    
print(f"Part 1: {np.count_nonzero(curr_plots == 2)}")