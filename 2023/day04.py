from dataclasses import dataclass

@dataclass
class Scratchcard:
    winners: set[int]
    numbers: set[int]

scratchcards: list[Scratchcard] = []
with open("day04_input.txt") as f:
    for line in f.readlines():
        winners_str, numbers_str = line.strip().split(": ")[1].split(" | ")
        winners = {int(i) for i in winners_str.split(" ") if len(i) > 0}
        numbers = {int(i) for i in numbers_str.split(" ") if len(i) > 0}
        scratchcards.append(Scratchcard(winners, numbers))
    
# Part 1
total_points: int = 0
match_counts = [len(s.numbers.intersection(s.winners)) for s in scratchcards]
for match_count in match_counts:
    if match_count > 0:
        total_points += 2 ** (match_count - 1)
        
print(f"Part 1: {total_points}")

# Part 2
total_card_counts = [1] * len(scratchcards)
for i, match_count in enumerate(match_counts):
    this_card_count = total_card_counts[i]
    for j in range(match_count):
        if i+j+1 < len(total_card_counts):
            total_card_counts[i+j+1] += this_card_count
            
print(f"Part 2: {sum(total_card_counts)}")
