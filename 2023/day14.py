import numpy as np

with open("day14_input.txt") as f:
    platform = np.asarray([list(line) for line in f.read().splitlines()])

def tilt_left(plat):
    """Tilt the platform left and return new platform configuration"""
    new_plat = []
    for row in plat:
        tilted = "#".join(["".join(sorted(grp, reverse=True)) for grp in "".join(row).split("#")])
        new_plat.append(list(tilted))
        
    return np.asarray(new_plat)

def load(plat):
    """Compute the north-load on the platform"""
    total_load = 0
    for row in plat.T:
        total_load += sum([len(row) - i for i, c in enumerate(row) if c == "O"])
        
    return total_load

# Transpose and shift left to make a north-tilt easier (i.e. row-wise not col-wise)
print(f"Part 1: {load(tilt_left(platform.T).T)}")

# Iterate until platform config hasn't changed since last cycle
history = []
loop_start = -1
while True:
    history.append(platform)
    # Tilt North, then West, then South, then East
    platform = tilt_left(platform.T).T
    platform = tilt_left(platform)
    platform = np.flipud(tilt_left(np.flipud(platform).T).T)
    platform = np.fliplr(tilt_left(np.fliplr(platform)))
    # Have we seen this config before?
    for i, prev_platform in enumerate(history):
        if np.all(np.equal(prev_platform, platform)):
            loop_start = i
    
    if loop_start >= 0:
        break

loop_len = len(history) - loop_start
print(f"Part 2: {load(history[loop_start + (1000000000 - loop_start) % loop_len])}")
