from dataclasses import dataclass
from math import lcm

node_map = dict()
directions = ""

with open("day08_input.txt") as f:
    directions = f.readline().strip()
    f.readline()
    for line in f.readlines():
        node_map[line[:3]] = (line[7:10], line[12:15])

current_node = "AAA"
iter = 0
while current_node != "ZZZ":
    options = node_map[current_node]
    current_node = options[0] if directions[iter % len(directions)] == "L" else options[1]
    iter += 1
    
print(f"Part 1: {iter}")

# Part 2: Compute deltas to Z's and offset / period for each path loop
@dataclass
class Loop:
    """Definition of a loop in the graph"""
    offset: int # Steps to reach first node of the loop
    period: int # Loop period from first node of the loop
    delta: int  # Steps to "Z" node within the loop
    
start_nodes = [k for k in node_map.keys() if k[-1] == "A"]
loops = []

for start_node in start_nodes:
    current_node = start_node
    chain = []
    iter = 0
    while True:
        d_index = iter % len(directions)
        chain.append((current_node, d_index))
        options = node_map[current_node]
        current_node = options[0] if directions[d_index] == "L" else options[1]
        iter += 1
        d_index = iter % len(directions)
        if (current_node, d_index) in chain:
            # We've found a loop!
            offset = chain.index((current_node, d_index))
            loop_chain = [c[0] for c in chain[offset:]]
            period = len(loop_chain)
            for delta, node in enumerate(loop_chain):
                if node[-1] == "Z":
                    loops.append(Loop(offset, period, delta))

            break

# Z hit for iter i, loop j when delta_j = (i - offset_j) % period_j
# Property of all loops is that offset_j + delta_j == period_j, so we can use lcm
print(f"Part 2: {lcm(*[loop.period for loop in loops])}")