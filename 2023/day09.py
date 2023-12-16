histories = []
with open("day09_input.txt") as f:
    for line in f.readlines():
        histories.append([int(v) for v in line.split(" ")])

def predict_next(history):
    """Get next value by repeated differencing"""
    diffs = [history[i+1] - history[i] for i in range(len(history) - 1)]
    if all([v == 0 for v in diffs]):
        return history[-1]
    else:    
        return history[-1] + predict_next(diffs)

print(f"Part 1: {sum([predict_next(history) for history in histories])}")

def predict_previous(history):
    """Get previous value by repeated differencing"""
    diffs = [history[i+1] - history[i] for i in range(len(history) - 1)]
    if all([v == 0 for v in diffs]):
        return history[0]
    else:    
        return history[0] - predict_previous(diffs)

print(f"Part 2: {sum([predict_previous(history) for history in histories])}")
