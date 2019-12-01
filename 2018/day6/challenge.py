import numpy as np

from aoc.challenge_base import ChallengeBase

class Challenge(ChallengeBase):
    """
    Day 6 challenges
    """
    def parse_input(self):
        points = []
        for line in self.lines:
            x, y = line.strip().split(", ")
            points.append((int(x), int(y)))

        xs, ys = zip(*points)
        min_x = min(xs)
        min_y = min(ys)
        max_x = max(xs)
        max_y = max(ys)

        # Shift points so min values are at zero
        xs = np.asarray(xs) - min_x
        ys = np.asarray(ys) - min_y
        self.points = list(zip(xs, ys))

    def challenge1(self):
        """
        Day 6 challenge 1
        """
        self.parse_input()

        # Figure out Manhattan distance to each grid point
        xs, ys = zip(*self.points)
        grid_shape = (len(self.points), max(ys) + 1, max(xs) + 1)
        grid = np.zeros(grid_shape, np.int16)
        for i, point in enumerate(self.points):
            for y in range(grid_shape[1]):
                for x in range(grid_shape[2]):
                    grid[i, y, x] = abs(point[0] - x) + abs(point[1] - y)

        # For each grid point, assign the nearest point if unique
        index_grid = np.argmin(grid, axis=0)
        reverse_index_grid = np.argmin(np.flip(grid, axis=0), axis=0)
        second_index_grid = len(self.points) - reverse_index_grid - 1
        non_unique_points = index_grid != second_index_grid
        index_grid[non_unique_points] = -1

        # Find edge points and remove these indices
        edge_indices = set()
        for x in range(grid_shape[2]):
            edge_indices.add(index_grid[0, x])
            edge_indices.add(index_grid[-1, x])

        for y in range(grid_shape[1]):
            edge_indices.add(index_grid[y, 0])
            edge_indices.add(index_grid[y, -1])

        for i in edge_indices:
            index_grid[index_grid == i] = -1

        # Now count the unique, non-edge points
        counts = np.asarray([np.count_nonzero(index_grid == i) for i in range(len(self.points))])
        print(f"Max count: {max(counts)} for point index {np.argmax(counts)}")

    def challenge2(self):
        """
        Day 6 challenge 2
        """
        xs, ys = zip(*self.points)
        grid_shape = (max(ys) + 1, max(xs) + 1)
        grid = np.zeros(grid_shape, np.int32)
        for y in range(grid_shape[0]):
            for x in range(grid_shape[1]):
                total = 0
                for i, point in enumerate(self.points):
                    total += abs(point[0] - x) + abs(point[1] - y)
                grid[y, x] = total

        valid_region = grid[grid < 10000]
        print(f"Valid region size: {np.count_nonzero(valid_region)}")
