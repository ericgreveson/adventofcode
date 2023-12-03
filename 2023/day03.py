import re

with open("day03_input.txt") as f:
    lines = [line.strip() for line in f.readlines()]

# Part 1
def is_symbol_adjacent(lines, i, start, end):
    """Is the span of chars (start, end) on line i adjacent to a symbol?"""
    search_lines = [lines[i]]
    if i > 0:
        search_lines.append(lines[i-1])
    if i < len(lines) - 1:
        search_lines.append(lines[i+1])
        
    for line in search_lines:
        search_start = max(0, start-1)
        search_end = min(len(line), end+1)
        for char in line[search_start:search_end]:
            if not (char == "." or char.isdigit()):
                return True
            
    return False
        
part_re = re.compile("\d+")
sum_parts = 0
for i, line in enumerate(lines):
    # Check each match to see if it's a part number
    for match in part_re.finditer(line):
        if is_symbol_adjacent(lines, i, match.start(), match.end()):
            sum_parts += int(match[0])
            
print(f"Part 1: {sum_parts}")

# Part 2
def find_adjacent_parts(lines, x, y):
    """Find all adjacent part numbers to the char at line x, column y"""
    parts = []
    search_lines = [lines[i]]
    if i > 0:
        search_lines.append(lines[i-1])
    if i < len(lines) - 1:
        search_lines.append(lines[i+1])
        
    for line in search_lines:
        for match in part_re.finditer(line):
            if not (y > match.end() or y < match.start()-1):
                parts.append(int(match[0]))
                
    return parts
    
sum_gear_ratios = 0
for i, line in enumerate(lines):
    # Look for gears
    for j, char in enumerate(line):
        if char == "*":
            parts = find_adjacent_parts(lines, i, j)
            if len(parts) == 2:
                sum_gear_ratios += parts[0]*parts[1]
                
print(f"Part 2: {sum_gear_ratios}")
