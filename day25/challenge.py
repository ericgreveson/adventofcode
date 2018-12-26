from aoc.challenge_base import ChallengeBase

def manhattan_dist_4d(p1, p2):
    """
    Compute manhattan distance between 4D points p1 and p2
    """
    dist = 0
    for axis in range(4):
        dist += abs(p2[axis] - p1[axis])

    return dist

class Challenge(ChallengeBase):
    """
    Day 25 challenges
    """
    def parse_input(self):
        """
        Parse input points
        """
        self.points = []
        for line in self.lines:
            self.points.append([int(p) for p in line.strip().split(",")])

    def merge_constellations(self, c1_index, c2_index):
        """
        Merge constellation with ID c2_index into c1_index, removing c2
        """
        # Move points to first constellation
        second_constellation = self.constellations[c2_index]
        self.constellations[c1_index] += second_constellation

        # Update the point to constellation map
        for point_index in second_constellation:
            self.point_to_constellation[point_index] = c1_index

        # Remove the second constellation
        del self.constellations[c2_index]

    def build_constellations(self):
        """
        Build constellations from points
        """
        # Find which points are within range of other points
        # Record the point's constellation index in an array, and keep a list of constellations
        self.constellations = dict()
        self.point_to_constellation = [-1] * len(self.points)
        next_constellation_id = 0
        for point_index, point in enumerate(self.points):
            # Test its distance against all other points so far
            close_points = [other_point_index for other_point_index in range(point_index)
                            if manhattan_dist_4d(point, self.points[other_point_index]) <= 3]
            
            if not close_points:
                # Add new constellation for this point
                self.point_to_constellation[point_index] = next_constellation_id
                self.constellations[next_constellation_id] = [point_index]
                next_constellation_id += 1
            else:
                # Add to first existing constellation
                constellation_indices = sorted([self.point_to_constellation[p] for p in close_points])
                first_constellation_index = constellation_indices[0]
                self.point_to_constellation[point_index] = first_constellation_index
                self.constellations[first_constellation_index].append(point_index)

                # Merge any other constellations matching this point into the first one
                for constellation_index in constellation_indices[1:]:
                    if constellation_index != first_constellation_index and constellation_index in self.constellations:
                        self.merge_constellations(first_constellation_index, constellation_index)

    def challenge1(self):
        """
        Day 25 challenge 1
        """
        self.parse_input()
        self.build_constellations()

        print(f"There are {len(self.constellations)} constellations")

    def challenge2(self):
        """
        Day 25 challenge 2
        """
        pass
