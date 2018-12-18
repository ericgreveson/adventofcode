import numpy as np

from aoc.challenge_base import ChallengeBase

class Challenge(ChallengeBase):
    """
    Day 18 challenges
    """
    def parse_input(self):
        """
        Parse input lines
        """
        # Pad acre edges by 1 so we can quickly look up things without worrying about edge effects
        self.acres = np.zeros((52, 52), dtype=np.int8)

        # 1 for open, 2 for tree, 3 for lumberyard
        acre_types = {".": 1, "|": 2, "#": 3}
        for y, line in enumerate(self.lines):
            for x, char in enumerate(line.strip()):
                self.acres[y + 1, x + 1] = acre_types[char]

    def run_time_step(self):
        """
        Run a single time step, updating the map
        """
        next_map = np.copy(self.acres)

        for y in range(self.acres.shape[0] - 2):
            for x in range(self.acres.shape[1] - 2):
                local_patch = self.acres[y:y+3, x:x+3]
                central_point = self.acres[y+1, x+1]
                if central_point == 1:
                    # Open ground. Becomes trees if >= 3 adjacent trees.
                    if np.count_nonzero(local_patch == 2) >= 3:
                        next_map[y+1, x+1] = 2
                elif central_point == 2:
                    # Trees. Becomes lumberyard if >= 3 adjacent lumberyards.
                    if np.count_nonzero(local_patch == 3) >= 3:
                        next_map[y+1, x+1] = 3
                else:
                    # Lumberyard. Becomes open unless adjacent to >= 1 lumberyard and >= 1 tree.
                    if np.count_nonzero(local_patch == 2) == 0 or np.count_nonzero(local_patch == 3) <= 1:
                        next_map[y+1, x+1] = 1

        # Do the time tick!
        self.acres = next_map

    def challenge1(self):
        """
        Day 18 challenge 1
        """
        self.parse_input()

        # Start the magical acre-evolution
        for _ in range(10):
            self.run_time_step()

        # Print the final resource value
        resource_value = np.count_nonzero(self.acres == 2) * np.count_nonzero(self.acres == 3)
        print(f"Final resource value: {resource_value}")

    def challenge2(self):
        """
        Day 18 challenge 2
        """
        self.parse_input()

        # This time, record resource values at each time point
        with open("out.txt", "wt") as f:
            for minute in range(1000):
                self.run_time_step()
                resource_value = np.count_nonzero(self.acres == 2) * np.count_nonzero(self.acres == 3)
                print(f"{minute},{resource_value}", file=f)
        
        # Looking at this, we have a repeating pattern:
        # 970,205900
        # 971,208080
        # 972,207000
        # 973,202842
        # ...
        # 996,202650
        # 997,205545
        # then back to the start. I.e. period of 28 and we know the values in there.
        
        # (1000000000 - 970) % 28 == 2
        # so answer is 208080
        print("Resource value after 1000000000 time steps: 208080")
