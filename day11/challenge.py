import numpy as np
from scipy.signal import convolve2d

from aoc.challenge_base import ChallengeBase

class Challenge(ChallengeBase):
    """
    Day 11 challenges
    """
    serial_number = 1723

    def convolve(self, kernel_size):
        """
        Convolve the grid with a kernel_size x kernel_size kernel
        """
        kernel = np.ones((kernel_size, kernel_size), dtype=np.int32)
        return convolve2d(self.grid, kernel, mode="valid")

    def challenge1(self):
        """
        Day 10 challenge 1
        """
        # Compute power levels
        self.grid = np.zeros((300,300), dtype=np.int32)
        for j in range(300):
            for i in range(300):
                x = i + 1
                y = j + 1
                rack_id = x + 10
                power = rack_id * y + self.serial_number
                power *= rack_id
                power = int(str(power)[-3]) if power > 100 else 0
                power = power - 5
                self.grid[j][i] = power

        # Find max 3x3 grid
        convolved = self.convolve(3)

        coord = np.unravel_index(np.argmax(convolved), convolved.shape)
        print(f"Max power coord: {coord[1]+1},{coord[0]+1}")

    def challenge2(self):
        """
        Day 11 challenge 2
        """
        # Convolve at every scale
        all_results = np.zeros((301, 300, 300), dtype=np.int32)
        for scale in range(1, 300):
            print(f"Scale: {scale}")
            convolved = self.convolve(scale)
            c_size = convolved.shape[0]
            all_results[scale,:c_size,:c_size] = convolved

        # Find max
        coord = np.unravel_index(np.argmax(all_results), all_results.shape)
        print(f"Challenge 2: Max power coord: {coord[2]+1},{coord[1]+1},{coord[0]}")
