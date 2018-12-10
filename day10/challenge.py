from aoc.challenge_base import ChallengeBase

class MovingPoint:
    """
    Moving point
    """
    def __init__(self, pos, velocity):
        """
        Create a moving point
        pos: initial position (x, y)
        velocity (vx, vy)
        """
        self.pos = pos
        self.velocity = velocity

    def update_pos(self):
        """
        Update the position for 1 time step
        """
        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]

class Challenge(ChallengeBase):
    """
    Day 10 challenges
    """
    def parse_input(self):
        """
        Parse input points
        """
        self.points = []
        for line in self.lines:
            parts = line.split("=<")
            pos = parts[1].split(">")[0].split(",")
            v = parts[2].split(">")[0].split(",")
            self.points.append(MovingPoint([int(pos[0]), int(pos[1])], [int(v[0]), int(v[1])]))

    def challenge1(self):
        """
        Day 10 challenge 1
        """
        self.parse_input()

        # Strategy: find step with smallest board
        board_sizes = []
        for i in range(20000):
            # Compute board size at each step
            xs, ys = zip(*[(point.pos[0], point.pos[1]) for point in self.points])
            dx = max(xs) - min(xs)
            dy = max(ys) - min(ys)
            board_area = dx*dy
            board_sizes.append((i, board_area))

            # Move all points
            for point in self.points:
                point.update_pos()

        # Now find the smallest board
        self.smallest_board = min(board_sizes, key=lambda item: item[1])
        
        # And run the simulation again to find the message
        self.parse_input()
        for i in range(self.smallest_board[0]):
            # Move all points
            for point in self.points:
                point.update_pos()

        # Figure out upper-left corner pos
        xs, ys = zip(*[(point.pos[0], point.pos[1]) for point in self.points])
        min_x = min(xs)
        min_y = min(ys)
        max_x = max(xs)
        max_y = max(ys)
        
        # Print the resulting board, using some list()/join magic to work around immutable strings
        print(f"Board {self.smallest_board[0]}:")
        lines = [list(" " * (max_x - min_x + 1)) for i in range(max_y - min_y + 1)]
        for point in self.points:
            lines[point.pos[1] - min_y][point.pos[0] - min_x] = "#"

        for line in lines:
            print("".join(line))

    def challenge2(self):
        """
        Day 10 challenge 2
        """
        print(f"Waiting time was {self.smallest_board[0]} seconds")
