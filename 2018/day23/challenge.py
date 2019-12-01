import itertools
import numpy as np
import re

from aoc.challenge_base import ChallengeBase

class Nanobot:
    """
    Nanobot with coords and range
    """
    def __init__(self, coord, r):
        """
        Constructor
        coord: (x, y, z) position
        r: signal range
        """
        self.coord = coord
        self.r = r

def manhattan_dist(c1, c2):
    """
    Compute Manhattan distance between two coordinates
    """
    return abs(c1[0] - c2[0]) + abs(c1[1] - c2[1]) + abs(c1[2] - c2[2])

class OctreeNode:
    """
    Node in an octree
    """
    def __init__(self, mins, maxs):
        """
        Constructor
        mins: [x, y, z] lower bound
        maxs: [x, y, z] (inclusive) upper-bound
        """
        self.mins = mins
        self.maxs = maxs
        self.children = []

    def in_node(self, coord):
        """
        Return True if coord is in this node
        """
        for axis in range(3):
            if coord[axis] < self.mins[axis] or coord[axis] > self.maxs[axis]:
                return False

        return True

    def nanobot_in_range_of_whole_node(self, nanobot):
        """
        Return True if nanobot is in range of all eight corners
        """
        for corner in itertools.product(*zip(self.mins, self.maxs)):
            if manhattan_dist(nanobot.coord, corner) > nanobot.r:
                return False

        return True

    def in_range_if_outside(self, nanobot):
        """
        Return True if nanobot is in range, assuming it's outside
        """
        nearest_point_on_cube = []
        for axis in range(3):
            c = nanobot.coord[axis]
            if c < self.mins[axis]:
                nearest_point_on_cube.append(self.mins[axis])
            elif c > self.maxs[axis]:
                nearest_point_on_cube.append(self.maxs[axis])
            else:
                nearest_point_on_cube.append(c)

        return manhattan_dist(nearest_point_on_cube, nanobot.coord) <= nanobot.r

class SearchResult:
    """
    Recursive node search result
    """
    def __init__(self, mins, maxs, count):
        """
        Constructor
        mins, maxs: extent of the area with the given count
        count: number of nanobots in range of the given area
        """
        self.mins = mins
        self.maxs = maxs
        self.count = count

class Challenge(ChallengeBase):
    """
    Day 23 challenges
    """
    def parse_input(self):
        """
        Parse input lines
        """
        line_re = re.compile("pos=<(-?\d+),(-?\d+),(-?\d+)>, r=(\d+)")
        self.nanobots = []
        for line in self.lines:
            m = line_re.match(line)
            self.nanobots.append(Nanobot((int(m.group(1)), int(m.group(2)), int(m.group(3))), int(m.group(4))))

    def search_coord_with_max_nanobots(self, mins, maxs, fully_in_range, maybe_partially_in_range, best_count=0):
        """
        Recursively search for cube with max nanobots in range
        mins: minimum (x, y, z) for the cube
        maxs: maximum (x, y, z) for the cube
        fully_in_range: list of nanobots known to be fully in range of the cube
        maybe_partially_in_range: list of nanobots that may be partially in range of the cube
        best_count: The best count so far, to allow us to skip nodes without potential to equal or better it
        return: list of SearchResult for this node
        """
        # Figure out how many of maybe_partially_in_range are actually in range of this whole cube
        # or if they're completely out of range
        cube = OctreeNode(mins, maxs)
        new_fully_in_range = fully_in_range.copy()
        new_partially_in_range = []
        for nanobot in maybe_partially_in_range:
            if cube.nanobot_in_range_of_whole_node(nanobot):
                new_fully_in_range.append(nanobot)
            elif cube.in_node(nanobot.coord) or cube.in_range_if_outside(nanobot):
                new_partially_in_range.append(nanobot)

        # If we're not potentially at least as good as best_count, no results worth returning
        if len(new_fully_in_range) + len(new_partially_in_range) < best_count:
            return []

        # If none are partially in range, we know the answer for this node!
        if not new_partially_in_range:
            return [SearchResult(mins, maxs, len(new_fully_in_range))]

        # If this node is only 0 or 1 units long in each direction, we can't subdivide
        big_enough = False
        for axis in range(3):
            if maxs[axis] - mins[axis] > 1:
                big_enough = True

        all_results = []
        if not big_enough:
            # Manually test all 8 corners (ignoring duplicate corners, if any)
            points_tested = set()
            for corner in itertools.product(*zip(mins, maxs)):
                if corner not in points_tested:
                    points_tested.add(corner)
                    new_best_count = len(new_fully_in_range) + len([nanobot for nanobot in new_partially_in_range
                                                                    if manhattan_dist(nanobot.coord, corner) <= nanobot.r])
                    if new_best_count >= best_count:
                        best_count = new_best_count
                        all_results += [SearchResult(corner, corner, new_best_count)]
                    
        else:
            # Otherwise, divide into 8 subcubes and recursively search
            midpoint = []
            for axis in range(3):
                midpoint.append((mins[axis] + maxs[axis]) // 2)

            axis_coords = list(zip(mins, midpoint, maxs))
            for corner_index in itertools.product(*zip([0, 0, 0], [1, 1, 1])):
                subcube_mins = []
                subcube_maxs = []
                for axis in range(3):
                    subcube_mins.append(axis_coords[axis][corner_index[axis]])
                    subcube_maxs.append(axis_coords[axis][corner_index[axis] + 1])

                results = self.search_coord_with_max_nanobots(subcube_mins,
                                                              subcube_maxs,
                                                              new_fully_in_range,
                                                              new_partially_in_range,
                                                              best_count)
                
                # Result counts should all be the same
                if results and results[0].count >= best_count:
                    all_results += results

        # Keep the result(s) with the highest count
        return [result for result in all_results if result.count == best_count]

    def challenge1(self):
        """
        Day 23 challenge 1
        """
        self.parse_input()

        # Find strongest nanobot
        strongest = max(self.nanobots, key=lambda n: n.r)

        # Find all in range of this
        num_in_range = 0
        for nanobot in self.nanobots:
            if manhattan_dist(nanobot.coord, strongest.coord) <= strongest.r:
                num_in_range += 1

        print(f"{num_in_range} nanobots are in range of strongest")

    def challenge2(self):
        """
        Day 23 challenge 2
        """
        # Let's try an octree-type approach
        # For each grid cube we should be able to find whether a nanobot:
        # 1) is not in range (is outside grid cube and not in range of nearest face)
        # 2) is in range of whole cube (all 8 corners are in range)
        # 3) is in range of part of the cube (i.e. not 1 or 2)
        # Root node: figure out extent of whole space
        mins = []
        maxs = []
        for axis in range(3):
            mins.append(min(self.nanobots, key=lambda n: n.coord[axis]).coord[axis])
            maxs.append(max(self.nanobots, key=lambda n: n.coord[axis]).coord[axis])

        for count in range(len(self.nanobots), 0, -1):
            results = self.search_coord_with_max_nanobots(mins, maxs, [], self.nanobots, count)
            if results and results[0].count >= count:
                break

        print(f"Found {len(results)} octree search results with {results[0].count} nanobots in range.")

        # Find result coord closest to origin
        closest_dist = np.iinfo(np.int32).max
        best_coord = None
        for result in results:
            for corner in itertools.product(*zip(result.mins, result.maxs)):
                d = manhattan_dist(corner, (0, 0, 0))
                if d < closest_dist:
                    closest_dist = d
                    best_coord = corner

        print(f"Best coord: {best_coord} (dist={manhattan_dist(best_coord, (0, 0, 0))})")
        