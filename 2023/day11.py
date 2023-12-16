from itertools import combinations
import numpy as np

with open("day11_input.txt") as f:
    image = np.asarray([[c == "#" for c in line] for line in f.read().splitlines()])

def expand_rows(image):
    """Duplicate blank rows in the image"""
    new_rows = []
    for row in image:
        new_rows.append(row)
        if not any(row):
            # Duplicate it
            new_rows.append(row)
    
    return np.asarray(new_rows)

expanded_image = expand_rows(image)
expanded_image = expand_rows(expanded_image.T).T

locations = np.argwhere(expanded_image)
distances = [np.sum(np.abs(a - b)) for a, b in combinations(locations, 2)]

print(f"Part 1: {sum(distances)}")

locations = np.argwhere(image)
blank_rows = set(range(image.shape[0])).difference(set(locations[:, 0]))
blank_cols = set(range(image.shape[1])).difference(set(locations[:, 1]))
distances = []
for a, b in combinations(locations, 2):
    dist_vec = np.abs(a - b)
    min_row, min_col = min(a[0], b[0]), min(a[1], b[1])
    rows = set(range(min_row, min_row + dist_vec[0]))
    cols = set(range(min_col, min_col + dist_vec[1]))
    distance = np.sum(dist_vec)
    distance += 999999*(len(rows.intersection(blank_rows)) + len(cols.intersection(blank_cols)))
    distances.append(distance)
    
print(f"Part 2: {sum(distances)}")
