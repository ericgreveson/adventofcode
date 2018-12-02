from abc import ABC, abstractmethod

class ChallengeBase(ABC):
    """
    Base class for Advent of Code challenges
    """
    def load_input(self, input_file):
        """
        input_file: Input file to load
        """
        with open(input_file, "rt") as f:
            self.lines = f.readlines()

    @abstractmethod
    def challenge1(self):
        """
        Run the first challenge of the day
        """
        pass

    @abstractmethod
    def challenge2(self):
        """
        Run the second challenge of the day
        """
        pass
