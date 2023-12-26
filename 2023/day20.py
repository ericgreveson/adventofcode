from collections import deque

class Pulse:
    def __init__(self, src, dest, is_high):
        self.src = src
        self.dest = dest
        self.is_high = is_high
        
class Broadcaster:
    def __init__(self, dests):
        self.name = "broadcaster"
        self.dests = dests
        
    def handle(self, pulse, pulse_queue):
        for dest in self.dests:
            pulse_queue.append(Pulse(self.name, dest, pulse.is_high))

class FlipFlop:
    def __init__(self, name, dests):
        self.name = name
        self.dests = dests
        self.state = False
        
    def handle(self, pulse, pulse_queue):
        if not pulse.is_high:
            self.state = not self.state
            for dest in self.dests:
                pulse_queue.append(Pulse(self.name, dest, self.state))
        
class Conjunction:
    def __init__(self, name, dests):
        self.name = name
        self.dests = dests
        
    def setup(self, inputs):
        self.state = {input: False for input in inputs}
        
    def handle(self, pulse, pulse_queue):
        self.state[pulse.src] = pulse.is_high
        result = not all(self.state.values())
        for dest in self.dests:
            pulse_queue.append(Pulse(self.name, dest, result))

def create_module(line):
    module_id, destinations = line.split(" -> ")
    dests = destinations.split(", ")
    if module_id == "broadcaster":
        return Broadcaster(dests)
    elif module_id[0] == "%":
        return FlipFlop(module_id[1:], dests)
    elif module_id[0] == "&":
        return Conjunction(module_id[1:], dests)
    else:
        raise ValueError()

def push_button(modules):
    pulse_queue = deque([Pulse("button", "broadcaster", False)])
    low_pulses, high_pulses = 0, 0
    while pulse_queue:
        pulse = pulse_queue.popleft()
        try:
            modules[pulse.dest].handle(pulse, pulse_queue)
        except KeyError:
            pass
        
        if pulse.is_high:
            high_pulses += 1
        else:
            low_pulses += 1
            
    return low_pulses, high_pulses

modules = {}
with open("day20_input.txt") as f:
    for line in f.read().splitlines():
        module = create_module(line)
        modules[module.name] = module

# Set up all the Conjunction states    
for conj in filter(lambda x: type(x) is Conjunction, modules.values()):
    conj.setup([m.name for m in modules.values() if conj.name in m.dests])

total_low_pulses = 0
total_high_pulses = 0
for _ in range(1000):
    low_pulses, high_pulses = push_button(modules)
    total_low_pulses += low_pulses
    total_high_pulses += high_pulses
    
print(f"Part 1: {total_low_pulses * total_high_pulses}")
