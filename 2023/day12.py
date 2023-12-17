import functools
import re

record_groups = []
with open("day12_input.txt") as f:
    for line in f.read().splitlines():
        record, groups = line.split(" ")
        record_groups.append((record, [int(x) for x in groups.split(",")]))
        
def is_ok(record, groups):
    """Is a particular arrangement acceptable according to the groups?"""
    runs = record.split(".")
    
@functools.cache
def num_arrangements(record, groups):
    """Compute the number of arrangements of springs for a record"""
    valid_re = re.compile("[\.\?]*" + "[\.\?]+".join([f"[#\?]{{{g}}}" for g in groups]) + "[\.\?]*")
    if not valid_re.fullmatch(record):
        return 0
    
    # It might match
    if "?" not in record:
        return 1
    
    # Replace first ? each way and recurse
    return num_arrangements(record.replace("?", ".", 1), groups) + \
        num_arrangements(record.replace("?", "#", 1), groups)

print(f"Part 1: {sum([num_arrangements(r, g) for r, g in record_groups])}")

record_groups = [("?".join([r]*5), g*5) for r, g in record_groups]
print(f"{record_groups[0]}")
print(f"Part 2: {sum([num_arrangements(r, g) for r, g in record_groups])}")
