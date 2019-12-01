import numpy as np

from aoc.challenge_base import ChallengeBase

class CrashError(RuntimeError):
    """
    Exception type for one or more cart crashes
    """
    def __init__(self, cart_pairs):
        """
        Constructor from list of cart pairs that collided
        """
        self.cart_pairs = cart_pairs

class Cart:
    """
    Cart representation
    """
    def __init__(self, x, y, direction):
        """
        Constructor
        x, y: initial coordinate
        direction: initial direction ('^', 'v', '>' or '<')
        """
        self.x = x
        self.y = y
        self.direction = direction
        self.turn_count = 0

    def turn_left(self):
        """
        Change orientation by making a left turn
        """
        if self.direction == "^":
            self.direction = "<"
        elif self.direction == "v":
            self.direction = ">"
        elif self.direction == "<":
            self.direction = "v"
        elif self.direction == ">":
            self.direction = "^"

    def turn_right(self):
        """
        Change orientation by making a left turn
        """
        if self.direction == "^":
            self.direction = ">"
        elif self.direction == "v":
            self.direction = "<"
        elif self.direction == "<":
            self.direction = "^"
        elif self.direction == ">":
            self.direction = "v"
        
    def move(self, base_map):
        """
        Move according to current direction and re-orient based on the given map
        """
        if self.direction == "^":
            self.y -= 1
        elif self.direction == "v":
            self.y += 1
        elif self.direction == "<":
            self.x -= 1
        elif self.direction == ">":
            self.x += 1

        # Work out new cart direction if it is going round a corner
        map_char = base_map[self.y][self.x]
        if map_char == "/":
            if self.direction == "^" or self.direction == "v":
                self.turn_right()
            else:
                self.turn_left()
        elif map_char == "\\":
            if self.direction == "^" or self.direction == "v":
                self.turn_left()
            else:
                self.turn_right()
        elif map_char == "+":
            # Intersection! We turn based on our internal counter
            if self.turn_count % 3 == 0:
                self.turn_left()
            elif self.turn_count % 3 == 2:
                self.turn_right()

            self.turn_count += 1

class Challenge(ChallengeBase):
    """
    Day 13 challenges
    """
    def get_map_removing_carts(self):
        """
        Get the underlying map without the carts on
        return (map, carts)
        where map is the ASCII line-list for the map
        and carts is the (x, y, direction) for each cart
        """
        new_map = []
        carts = []
        for y, line in enumerate(self.lines):
            new_line = []
            for x, char in enumerate(line):
                if char == "^" or char == "v":
                    new_line.append("|")
                    carts.append(Cart(x, y, char))
                elif char == ">" or char == "<":
                    new_line.append("-")
                    carts.append(Cart(x, y, char))
                else:
                    new_line.append(char)

            new_map.append("".join(new_line))

        return new_map, carts

    def run_tick(self, base_map, carts):
        """
        Run a single tick of the tracks, updating all carts in-place
        Raise CrashError if carts overlap
        """
        sorted_carts = sorted(carts, key=lambda cart: cart.y * 1000 + cart.x)
        marked_crashes = []
        for cart_index, cart in enumerate(sorted_carts):
            # Move cart in appropriate direction
            cart.move(base_map)
            
            # Is there a crash?
            for other_cart in sorted_carts[:cart_index] + sorted_carts[cart_index+1:]:
                if other_cart.x == cart.x and other_cart.y == cart.y:
                    # Record it but finish the tick anyway (needed for challenge 2)
                    marked_crashes.append((cart, other_cart))

        if marked_crashes:
            raise CrashError(marked_crashes)

    def challenge1(self):
        """
        Day 13 challenge 1
        """
        # Let's just use the text input pretty much as is! Probably won't be too slow
        base_map, carts = self.get_map_removing_carts()
        try:
            while True:
                self.run_tick(base_map, carts)

        except CrashError as ex:
            # Both crashed carts are at the same place, we only care about the first crashed pair
            print(f"Crash at {ex.cart_pairs[0][0].x}, {ex.cart_pairs[0][0].y}")

    def challenge2(self):
        """
        Day 13 challenge 2
        """
        base_map, carts = self.get_map_removing_carts()
        while len(carts) > 1:
            try:
                self.run_tick(base_map, carts)
            except CrashError as ex:
                # This time, just remove all crashed carts
                crashed_carts = [p[0] for p in ex.cart_pairs] + [p[1] for p in ex.cart_pairs]
                carts = list(filter(lambda cart: cart not in crashed_carts, carts))
                
        print(f"Last cart at {carts[0].x}, {carts[0].y}")

