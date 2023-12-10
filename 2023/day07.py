from collections import Counter
from functools import cmp_to_key, partial

class Round:
    """A Round is a hand of cards together with its bid"""
    hand: str
    bid: int
    
    def __init__(self, line):
        """Construct by parsing line"""
        elements = line.split(" ")
        self.hand = elements[0]
        self.bid = int(elements[1])

rounds: list[Round] = []
with open("day07_input.txt") as f:
    for line in f.readlines():
        rounds.append(Round(line))

def hand_strength(hand: str, joker: bool) -> int:
    """Return hand strength (with or without special joker rule)"""
    counter = Counter(hand)
    
    if joker:
        # Replace J with best option
        most_common = counter.most_common(1)[0]
        if most_common[0] == "J":
            try:
                most_common = counter.most_common(2)[1]
            except IndexError:
                # All jokers! We can just replace it with aces
                most_common = ("A", 0)
            
        new_hand = hand.replace("J", most_common[0])
        counter = Counter(new_hand)
        
    if len(counter) == 1:
        # Five of a kind
        return 6
    
    if len(counter) == 2:
        if counter.most_common(1)[0][1] == 4:
            # Four of a kind
            return 5
        else:
            # Full house
            return 4
        
    if len(counter) == 3:
        if counter.most_common(1)[0][1] == 3:
            # Three of a kind
            return 3
        else:
            # Two pair
            return 2
    
    if len(counter) == 4:
        # Pair
        return 1
    
    # High card
    return 0

def card_strength(card: str, joker: bool) -> int:
    """Strength of a single card (with or without special joker rule)"""
    ordering = "J23456789TQKA" if joker else "23456789TJQKA"
    return ordering.index(card)
    
def compare_hands(r1: Round, r2: Round, joker: bool) -> int:
    """Compare two hands (with or without special joker rule)"""
    h1 = hand_strength(r1.hand, joker)
    h2 = hand_strength(r2.hand, joker)
    if h1 < h2:
        return -1
    elif h1 > h2:
        return 1
    
    # Types are the same. Use second ordering rule.
    for c1, c2 in zip(r1.hand, r2.hand):
        if c1 != c2:
            return (-1 if card_strength(c1, joker) < card_strength(c2, joker) else 1)
        
    return 0

rounds.sort(key=cmp_to_key(partial(compare_hands, joker=False)))
print(f"Part 1: {sum([r.bid * rank for rank, r in enumerate(rounds, start=1)])}")

rounds.sort(key=cmp_to_key(partial(compare_hands, joker=True)))
print(f"Part 2: {sum([r.bid * rank for rank, r in enumerate(rounds, start=1)])}")