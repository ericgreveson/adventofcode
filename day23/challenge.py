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
        pass
