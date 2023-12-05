from dataclasses import dataclass
    
@dataclass
class Range:
    """Simple range of values determined by start and length"""
    start: int
    length: int
    
    def end(self):
        """Return one-past-the-end of the range"""
        return self.start + self.length
    
@dataclass
class SrcDstRange:
    """Range mapping from src_start and dst_start for range_len values"""
    src_start: int
    dst_start: int
    range_len: int
    
    def apply(self, value: int):
        """If range includes value, apply the map. If not, return None"""
        if value >= self.src_start and value < self.src_start + self.range_len:
            return self.dst_start + (value - self.src_start)
        else:
            return None
        
    def apply_range(self, value_range: Range):
        """Apply mapping to passed range, returning (mapped_range, [remaining_ranges])
        if (part of) range overlaps, or (None, None) if no overlap"""
        self_end = self.src_start + self.range_len
        if value_range.end() < self.src_start or value_range.start > self_end:
            return None, None
        
        # There is some overlap...
        remaining_ranges: list[Range] = []
        if value_range.start < self.src_start:
            remaining_ranges.append(Range(value_range.start, self.src_start - value_range.start))
            
        if value_range.end() > self_end:
            remaining_ranges.append(Range(self_end, value_range.end() - self_end))
            
        overlap_src_start = max(value_range.start, self.src_start)
        overlap_src_end = min(value_range.end(), self_end)
        overlap_dst_start = self.dst_start + (overlap_src_start - self.src_start)
        return Range(overlap_dst_start, overlap_src_end - overlap_src_start), remaining_ranges        
    
@dataclass
class SrcDstRangeMap:
    """Map of ranges from src to dst categories"""
    src: str
    dst: str
    ranges: list[SrcDstRange]
    
    def apply(self, value: int):
        """Lookup the appropriate range, if no range matches, return same value"""
        for range in self.ranges:
            result = range.apply(value)
            if result:
                return result
        
        return value
    
    def apply_range(self, value_range: Range):
        """Lookup all values in value_range, returning a list of ranges"""
        result_ranges: list[Range] = []
        ranges_to_process: list[Range] = [value_range]
        for range in self.ranges:
            new_ranges_to_process: list[Range] = []
            for range_to_process in ranges_to_process:
                mapped_range, remaining_ranges = range.apply_range(range_to_process)
                if mapped_range:
                    result_ranges.append(mapped_range)
                    new_ranges_to_process += remaining_ranges
                else:
                    new_ranges_to_process.append(range_to_process)
                    
            ranges_to_process = new_ranges_to_process
            
        return result_ranges + ranges_to_process

seeds: list[int] = []
maps: dict[str, SrcDstRangeMap] = {}

# Read input
with open("day05_input.txt") as f:
    seeds = [int(s) for s in f.readline().split(": ")[1].strip().split(" ")]
    f.readline()
    map_blocks = []
    map_block = []
    for line in f.read().splitlines():
        if line == "":
            # End of a map block
            map_blocks.append(map_block)
            map_block = []
        else:
            map_block.append(line)
            
    map_blocks.append(map_block)
    
    for map_block in map_blocks:
        src, dst = map_block[0].split(" ")[0].split("-to-")
        ranges = []
        for line in map_block[1:]:
            # note ordering! dst first in input file
            dst_start, src_start, range_len = (int(v) for v in line.split(" "))
            ranges.append(SrcDstRange(src_start, dst_start, range_len))
            
        maps[src] = SrcDstRangeMap(src, dst, ranges)

# Part 1    
def find_location(seed: int):
    """Apply all the maps and return final value when we hit location as dst"""
    current_map = maps["seed"]
    value = seed
    while True:
        value = current_map.apply(value)
        if current_map.dst == "location":
            return value
        
        current_map = maps[current_map.dst]    

locations = [find_location(seed) for seed in seeds]
print(f"Part 1: {min(locations)}")

# Part 2
def find_location_ranges(seed_range: Range):
    """Apply all the maps to the seed range and return a list of location ranges"""
    current_map = maps["seed"]
    value_ranges = [seed_range]
    while True:
        dst_ranges: list[Range] = []
        for src_range in value_ranges:
            dst_ranges += current_map.apply_range(src_range)
            
        value_ranges = dst_ranges
            
        if current_map.dst == "location":
            return value_ranges

        current_map = maps[current_map.dst]
                                    
seed_ranges = [Range(seeds[i*2], seeds[i*2+1]) for i in range(len(seeds) // 2)]
min_location = min(locations)
for seed_range in seed_ranges:
    location_ranges = find_location_ranges(seed_range)
    min_location = min(min_location, min([lr.start for lr in location_ranges]))

print(f"Part 2: {min_location}")
