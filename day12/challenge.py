import numpy as np

from aoc.challenge_base import ChallengeBase

class Challenge(ChallengeBase):
    """
    Day 12 challenges
    """
    def parse_input(self):
        """
        Parse input data
        """
        self.initial_state = self.lines[0][len("initial state: "):].strip()
        self.rules = {}
        for line in self.lines[2:]:
            lhs, rhs = line.strip().split(" => ")
            self.rules[lhs] = rhs

    def update_generation(self, gen):
        """
        Update generation gen based on the rules
        """
        next_gen = ".."

        # Check each plant within 2-padding of edges
        for central_plant in range(2, len(gen)-2):
            next_gen += self.rules[gen[central_plant-2:central_plant+3]]

        # Update latest generation
        return next_gen + ".."

    def challenge1(self):
        """
        Day 12 challenge 1
        """
        self.parse_input()

        # We need to allocate enough space left and right - -40 to len(initial_state) + 40
        latest_gen = "."*40 + self.initial_state + "."*40
        for _ in range(20):
            latest_gen = self.update_generation(latest_gen)

        # Compute sum
        sum = 0
        for index, char in enumerate(latest_gen):
            if char == "#":
                sum += index - 40

        print(f"Sum: {sum}")

    def challenge2(self):
        """
        Day 12 challenge 2
        """
        # Let's look for a pattern - run 1000 generations, should be enough to let the states settle down
        latest_gen = "."*2000 + self.initial_state + "."*2000
        for _ in range(999):
            latest_gen = self.update_generation(latest_gen)
            
        # Let's see what happens here (it's probably a translating pattern by now)
        for i in range(8):
            latest_gen = self.update_generation(latest_gen)
            sum = 0
            for index, char in enumerate(latest_gen):
                if char == "#":
                    sum += index - 2000
            print(f"Gen {1000+i}: {sum}")

        # And looking at the result of the above, we can see score = 42061 + 42*(gen-1000)
        print(f"Gen 50000000000: {42061+42*(50000000000-1000)}")
