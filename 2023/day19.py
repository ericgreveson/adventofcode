from math import prod

class PropRanges:
    def __init__(self, x, m, a, s):
        self.x = x
        self.m = m
        self.a = a
        self.s = s
        
    def copy_replace(self, prop, r):
        props = {"x": self.x, "m": self.m, "a": self.a, "s": self.s}
        props[prop] = r
        return PropRanges(props["x"], props["m"], props["a"], props["s"])
        
    def combinations(self):
        return prod((pr[1] - pr[0] + 1) for pr in [self.x, self.m, self.a, self.s])
        
class Filter:
    def __init__(self, dest):
        self.dest = dest

class GreaterThan(Filter):
    def __init__(self, cond, dest):
        self._prop, val = cond.split(">")
        super().__init__(dest)
        self._val = int(val)
        
    def test(self, part):
        return part[self._prop] > self._val
    
    def split_ranges(self, prop_ranges):
        r = getattr(prop_ranges, self._prop)
        r0_pass, r1_pass = r[0] > self._val, r[1] > self._val
        if r0_pass and r1_pass:
            return (prop_ranges, None)
        elif (not r0_pass) and (not r1_pass):
            return (None, prop_ranges)
        else:
            return (prop_ranges.copy_replace(self._prop, (self._val + 1, r[1])),
                    prop_ranges.copy_replace(self._prop, (r[0], self._val)))
    
class LessThan(Filter):
    def __init__(self, cond, dest):
        self._prop, val = cond.split("<")
        super().__init__(dest)
        self._val = int(val)
        
    def test(self, part):
        return part[self._prop] < self._val
    
    def split_ranges(self, prop_ranges):
        r = getattr(prop_ranges, self._prop)
        r0_pass, r1_pass = r[0] < self._val, r[1] < self._val
        if r0_pass and r1_pass:
            return (prop_ranges, None)
        elif (not r0_pass) and (not r1_pass):
            return (None, prop_ranges)
        else:
            return (prop_ranges.copy_replace(self._prop, (r[0], self._val - 1)),
                    prop_ranges.copy_replace(self._prop, (self._val, r[1])))

class Always(Filter):
    def __init__(self, dest):
        super().__init__(dest)
        
    def test(self, _):
        return True
    
    def split_ranges(self, prop_ranges):
        return (prop_ranges, None)

def make_rule(text):
    if ":" not in text:
        return Always(text)
    
    cond, dest = text.split(":")
    if ">" in cond:
        return GreaterThan(cond, dest)
    elif "<" in cond:
        return LessThan(cond, dest)

class Workflow:
    def __init__(self, line):
        self.id, rest = line.split("{")
        self.rules = [make_rule(s) for s in rest[:-1].split(",")]

workflows = {}
parts = []
with open("day19_input.txt") as f:
    lines = f.read().splitlines()
    done_workflows = False
    for line in lines:
        if line == "":
            done_workflows = True
            continue
        
        if not done_workflows:
            workflow = Workflow(line)
            workflows[workflow.id] = workflow
        else:
            parts.append({prop[0]: int(prop[2:]) for prop in line[1:-1].split(",")})

def apply_workflows(part):
    wfid = "in"
    while wfid not in ["A", "R"]:
        wf = workflows[wfid]
        for rule in wf.rules:
            if rule.test(part):
                wfid = rule.dest
                break

    return wfid

accepted = [part for part in parts if apply_workflows(part) == "A"]
print(f"Part 1: {sum(sum(val for val in part.values()) for part in accepted)}")

def count_combinations(workflow_id, prop_ranges):
    wf = workflows[workflow_id]
    total_combinations = 0
    for rule in wf.rules:
        pass_range, fail_range = rule.split_ranges(prop_ranges)
        if pass_range:
            if rule.dest == "A":
                total_combinations += pass_range.combinations()
            elif rule.dest != "R":
                total_combinations += count_combinations(rule.dest, pass_range)
        
        if not fail_range:
            return total_combinations
        
        prop_ranges = fail_range
                
pr = PropRanges((1, 4000), (1, 4000), (1, 4000), (1, 4000))
print(f"Part 2: {count_combinations('in', pr)}")
