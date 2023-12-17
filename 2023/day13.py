import numpy as np

patterns = []

with open("day13_input.txt") as f:
    pattern = []
    for line in f.read().splitlines():
        if line == "":
            patterns.append(np.asarray(pattern))
            pattern = []
        else:
            pattern.append([c == "#" for c in line])
            
    patterns.append(np.asarray(pattern))
    
def has_reflection(pattern, reflection_row):
    """Return True if pattern has vertical symmetry about line reflection_row"""
    for row in range(0, reflection_row):
        mirror_row = reflection_row + (reflection_row - row - 1)
        if mirror_row < pattern.shape[0] and list(pattern[row]) != list(pattern[mirror_row]):
            return False

    return True

def find_row_sym(pattern, ignore_sym_row):
    """Find a vert reflection in pattern, returning num rows above line or None
    Ignore a symmetry row ignore_sym_row if given"""
    for reflection_row in range(1, pattern.shape[0]):
        if reflection_row != ignore_sym_row and has_reflection(pattern, reflection_row):
            return reflection_row
        
    return None

def find_sym(pattern, ignore_sym=None):
    """Find a reflection in pattern, vertical or horizontal, return (r, 0) or (0, c)
    if vert or horz symmetry, respectively. Ignore symmetry ignore_sym if given."""
    s = find_row_sym(pattern, ignore_sym[0] if ignore_sym else None)
    if s:
        return (s, 0)
    else:
        s = find_row_sym(pattern.T, ignore_sym[1] if ignore_sym else None)
        if s:
            return (0, s)
        
    return None
            
syms = [find_sym(p) for p in patterns]
print(f"Part 1: {sum([r*100 + c for r, c in syms])}")

new_syms = []
for pattern, sym in zip(patterns, syms):
    # Find a different symmetry by perturbing each element
    found = False
    for it in np.ndindex(pattern.shape):
        pattern[it] = not pattern[it]
        new_sym = find_sym(pattern, ignore_sym=sym)            
        if new_sym:
            new_syms.append(new_sym)
            found = True
            break
        
        pattern[it] = not pattern[it]

print(f"Part 2: {sum([r*100 + c for r, c in new_syms])}")
