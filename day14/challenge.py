from aoc.challenge_base import ChallengeBase

class Challenge(ChallengeBase):
    """
    Day 14 challenges
    """
    puzzle_input = 894501

    def generate_recipes_from_latest(self):
        """
        Create recipes from current score summing rule
        """
        total = self.scoreboard[self.indices[0]] + self.scoreboard[self.indices[1]]

        # Add each digit (if it exists) to the scoreboard
        if total > 9:
            self.scoreboard.append(total // 10)
        
        self.scoreboard.append(total % 10)

    def update_indices(self):
        """
        Update elves' current recipes according to score plus one wraparound rule
        """
        for i in [0, 1]:
            self.indices[i] = (self.indices[i] + self.scoreboard[self.indices[i]] + 1) % len(self.scoreboard)

    def make_six_digit(self, seq):
        """
        Make a six digit number from a sequence of six digits
        """
        return seq[0]*100000 + seq[1]*10000 + seq[2]*1000 + seq[3]*100 + seq[4]*10 + seq[5]

    def challenge1(self):
        """
        Day 14 challenge 1
        """
        # Initial scoreboard and elf current recipe indices
        self.scoreboard = [3, 7]
        self.indices = [0, 1]

        # Generate new recipes
        while len(self.scoreboard) < self.puzzle_input + 10:
            self.generate_recipes_from_latest()
            self.update_indices()

        print(f"Scoreboard next 10: {self.scoreboard[self.puzzle_input:]}")

    def challenge2(self):
        """
        Day 14 challenge 2
        """
        # Generate a whole load more in the sequence (hacky guess at enough data)
        while len(self.scoreboard) < 30000000:
            self.generate_recipes_from_latest()
            self.update_indices()

        # Hopefully now the sequence is in our scoreboard...
        for i in range(len(self.scoreboard) - 10):
            if self.make_six_digit(self.scoreboard[i:i+6]) == self.puzzle_input:
                print(f"Number of recipes to left: {i}")
                break
