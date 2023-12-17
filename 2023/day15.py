with open("day15_input.txt") as f:
    steps = f.read().split(",")
    
def compute_hash(s):
    current_value = 0
    for c in s:
        current_value += ord(c)
        current_value *= 17
        current_value %= 256
        
    return current_value

print(f"Part 1: {sum([compute_hash(step) for step in steps])}")

def remove_lens(box, label):
    for lens in box:
        if lens[0] == label:
            box.remove(lens)
            break
        
def replace_lens(box, label, f):
    for lens in box:
        if lens[0] == label:
            lens[1] = f
            return
        
    box.append([label, f])

boxes = [[] for _ in range(256)]
for step in steps:
    if step[-1] == "-":
        label = step[:-1]
        box_id = compute_hash(label)
        remove_lens(boxes[box_id], label)
    else:
        label, f = step.split("=")
        box_id = compute_hash(label)
        replace_lens(boxes[box_id], label, int(f))

focusing_power = 0
for i, box in enumerate(boxes):
    for j, (label, f) in enumerate(box):
        focusing_power += (i + 1) * (j + 1) * f
        
print(f"Part 2: {focusing_power}")