
from collections import Counter

from aoc.challenge_base import ChallengeBase

class Challenge(ChallengeBase):
    """
    Day 2 challenges
    """
    def challenge1(self):
        """
        Day 2 challenge 1
        """
        ids_with_two = 0
        ids_with_three = 0
        for id in self.lines:
            counts = set(Counter(id).values())
            if 2 in counts:
                ids_with_two += 1
            if 3 in counts:
                ids_with_three += 1

        checksum = ids_with_three * ids_with_two
        print(f"Checksum: {checksum}")

    def challenge2(self):
        """
        Day 2 challenge 2
        """
        # Remove one letter at each position from each ID and plonk them in a set
        match_possibilities = set()
        for id in self.lines:
            sub_ids = set()
            for letter_pos in range(len(id)):
                sub_ids.add(id[:letter_pos] + id[(letter_pos + 1):])
            
            matching_letters = match_possibilities.intersection(sub_ids)
            if matching_letters:
                break

            match_possibilities.update(sub_ids)

        # If the current one matches
        print(f"Matching letters: {matching_letters.pop()}")
        