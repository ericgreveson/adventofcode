from string import ascii_lowercase

from aoc.challenge_base import ChallengeBase

class Challenge(ChallengeBase):
    """
    Day 5 challenges
    """
    def react(self, polymer):
        """
        React a polymer, returning the result
        """
        reaction = True
        while reaction:
            reaction = False
            for start_pos in range(len(polymer) - 1):
                first = polymer[start_pos]
                second = polymer[start_pos+1]
                if first != second and first.lower() == second.lower():
                    # Remove the pair
                    polymer = polymer[:start_pos] + polymer[start_pos+2:]
                    reaction = True
                    break

        return polymer

    def challenge1(self):
        """
        Day 5 challenge 1
        """
        # Polymer representation is a single line
        polymer = self.lines[0].strip()

        # Start reacting!
        print(f"Start length: {len(polymer)}")
        polymer = self.react(polymer)
        print(f"Final length: {len(polymer)}")

    def challenge2(self):
        """
        Day 5 challenge 2
        """
        reacted_lengths = {}
        for char in ascii_lowercase:
            # Get the simplified polymer removing upper/lowercase versions of this letter
            polymer = self.lines[0].strip()
            polymer = polymer.replace(char, "").replace(char.upper(), "")
            
            # React it and measure the length
            polymer = self.react(polymer)
            reacted_lengths[char] = len(polymer)
            print(f"Processed letter {char}/{char.upper()}: length {len(polymer)}")

        # Find the shortest polymer
        removed_char, length = min(reacted_lengths.items(), key=lambda item: reacted_lengths[item[0]])
        print(f"Removed character: {removed_char} yields shortest polymer, length {length}")
