from aoc.challenge_base import ChallengeBase

class Challenge(ChallengeBase):
    """
    Day 1 challenges
    """
    def challenge1(self):
        """
        Day 1 challenge 1
        """
        freq = 0
        for line in self.lines:
            freq += int(line)

        print(f"Final freq: {freq}")

    def challenge2(self):
        """
        Day 1 challenge 2
        """
        found = False
        freq = 0
        freqs_hit = {freq}
        while not found:
            for line in self.lines:
                freq += int(line)
                if freq in freqs_hit:
                    found = True
                    break
                freqs_hit.add(freq)

        print(f"First repeated freq: {freq}")
