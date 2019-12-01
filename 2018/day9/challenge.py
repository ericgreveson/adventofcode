from aoc.challenge_base import ChallengeBase

class MarbleCircleNode:
    """
    Node in doubly-linked list for marble circle
    """
    def __init__(self, value, cw, ccw):
        """
        Create a marble node.
        value: marble value
        cw: clockwise marble
        ccw: counter-clockwise marble
        """
        self.value = value
        self.cw = cw
        self.ccw = ccw

class MarbleCircle:
    """
    Class representing circle of marbles
    """
    def __init__(self):
        """
        Constructor. Initialize with the zero marble.
        """
        # Treat as doubly-linked list
        self.current_marble = MarbleCircleNode(0, None, None)
        self.current_marble.cw = self.current_marble.ccw = self.current_marble

    def add_marble_two_clockwise(self, marble):
        """
        Add a marble to the circle, between the marbles 1 and 2 further clockwise from current
        """
        # Find the node where we'll insert this marble clockwise of
        ccw_node = self.current_marble.cw
            
        # Expand the circle and re-link
        new_node = MarbleCircleNode(marble, ccw_node.cw, ccw_node)
        ccw_node.cw = new_node
        new_node.cw.ccw = new_node

        # Update index
        self.current_marble = new_node

    def remove_seven_counter_clockwise(self):
        """
        Remove the marble seven counter-clockwise from current and return it
        Also set the current index to the marble clockwise from the removed one
        """
        node_to_remove = self.current_marble
        for _ in range(7):
            node_to_remove = node_to_remove.ccw
        
        # Unlink this node
        node_to_remove.ccw.cw = node_to_remove.cw
        node_to_remove.cw.ccw = node_to_remove.ccw
        self.current_marble = node_to_remove.cw
        return node_to_remove.value

def run_marble_game(num_players, last_marble_value):
    """
    Simulate the marble game for the given parameters
    Return an array of final player scores
    """
    player_scores = [0] * num_players
    marble_circle = MarbleCircle()
    for marble in range(1, last_marble_value + 1):
        if marble % 23 != 0:
            marble_circle.add_marble_two_clockwise(marble)
        else:
            removed_marble = marble_circle.remove_seven_counter_clockwise()
            player_scores[marble % num_players] += removed_marble + marble

    return player_scores

class Challenge(ChallengeBase):
    """
    Day 9 challenges
    """
    num_players = 439
    last_marble_value = 71307

    def challenge1(self):
        """
        Day 9 challenge 1
        """
        # Simulate the game!
        player_scores = run_marble_game(self.num_players, self.last_marble_value)
        high_score = max(player_scores)
        print(f"High score for {self.num_players} / {self.last_marble_value}: {high_score}")

    def challenge2(self):
        """
        Day 1 challenge 2
        """
        # Simulate the game!
        player_scores = run_marble_game(self.num_players, self.last_marble_value * 100)
        high_score = max(player_scores)
        print(f"High score for {self.num_players} / {self.last_marble_value * 100}: {high_score}")
