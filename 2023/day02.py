class Sample:
    def __init__(self, item):
        """Parse a sample from text item"""
        item_counts = item.strip().split(", ")
        self.counts = {"red": 0, "green": 0, "blue": 0}
        for count_data in item_counts:
            count, colour = count_data.split(" ")
            self.counts[colour] = int(count)

class Game:
    def __init__(self, line):
        """Parse a game from text line"""
        game_data, sample_data = line.split(": ")
        self.id = int(game_data.split(" ")[1])
        self.samples = [Sample(item) for item in sample_data.split("; ")]
        
with open("day02_input.txt") as f:
    games = [Game(line) for line in f.readlines()]
    
# Part 1
def is_game_possible(game):
    for sample in game.samples:
        if sample.counts["red"] > 12 or sample.counts["green"] > 13 or sample.counts["blue"] > 14:
            return False
        
    return True

sum_ids = sum([game.id for game in games if is_game_possible(game)])
print(f"Part 1: sum = {sum_ids}")

# Part 2
def compute_power(game):
    """Compute product of red / green / blue minima"""
    power = 1
    for colour in ["red", "green", "blue"]:
        power *= max([sample.counts[colour] for sample in game.samples])
        
    return power
    
sum_powers = sum([compute_power(game) for game in games])
print(f"Part 2: sum powers = {sum_powers}")