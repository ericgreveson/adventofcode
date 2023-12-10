from math import ceil, floor, prod, sqrt

races = [(49, 263), (97, 1532), (94, 1378), (94, 1851)]

def ways_to_win(time, dist):
    """Compute the number of ways to win a race"""
    # v = hold_time => d = hold_time * (race_time - hold_time)
    # win when d > record => -hold_time ^ 2 + hold_time * race_time - record > 0
    # x = (race_time -+ sqrt(race_time * race_time - 4 * record)) / 2
    q = sqrt(time * time - 4 * dist)
    upper = floor((time + q) / 2)
    lower = ceil((time - q) / 2)
    return upper - lower + 1

product = prod([ways_to_win(r[0], r[1]) for r in races])
print(f"Part 1: {product}")
print(f"Part 2: {ways_to_win(49979494, 263153213781851)}")
