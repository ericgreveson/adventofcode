from enum import Enum
import numpy as np
from PIL import Image

from aoc.challenge_base import ChallengeBase

class MapTile(Enum):
    """
    Values for map tiles
    """
    SAND = 0
    CLAY = 1
    FLOWING_WATER = 2
    STILL_WATER = 3

class Challenge(ChallengeBase):
    """
    Day 16 challenges
    """
    def parse_input(self):
        """
        Parse input lines
        """
        # First, parse the clay ranges
        vert_ranges = []
        horz_ranges = []
        for line in self.lines:
            # Get the basic tokens
            first, second = line.strip().split(", ")
            first_axis, first_dist = first.split("=")
            second_axis, second_range = second.split("=")
            second_start, second_end = second_range.split("..")
            if first_axis == second_axis:
                raise RuntimeError("Expecting two different axes!")

            # Record as (first_axis_pos, range_start, range_end) tuple
            range_tuple = (int(first_dist), int(second_start), int(second_end))
            if first_axis == "x":
                vert_ranges.append(range_tuple)
            elif first_axis == "y":
                horz_ranges.append(range_tuple)
            else:
                raise RuntimeError("Expecting x or y axis")

        # Now use these to build our cross-section map. We want to clip to X and Y range given.
        self.min_x = min([r[0] for r in vert_ranges] + [r[1] for r in horz_ranges])
        self.min_y = min([r[0] for r in horz_ranges] + [r[1] for r in vert_ranges])

        # Build map as 2d array with 0 as sand
        # A real genius would RLE encode the whole thing for super efficiency, but for an idiot like me,
        # that seems like the water filling algorithms would become a bit complicated...
        max_x = max([r[0] for r in vert_ranges] + [r[2] for r in horz_ranges])
        max_y = max([r[0] for r in horz_ranges] + [r[2] for r in vert_ranges])

        # Could leave an extra top row as all sand, as we may need to flow water along it.
        # But we don't need to as the puzzle input kindly leaves some extra little nubbins
        # within and above the top container so it's not an issue in practice
        # However we do need a padding column in X before and after to allow waterfalls off the edge!
        self.map = np.zeros((max_y - self.min_y + 1, max_x - self.min_x + 1 + 2), dtype=np.uint8)

        # Draw the clay
        for x, y_start, y_end in vert_ranges:
            self.map[(y_start - self.min_y):(y_end - self.min_y + 1), x - self.min_x + 1] = MapTile.CLAY.value

        for y, x_start, x_end in horz_ranges:
            self.map[(y - self.min_y), (x_start - self.min_x + 1):(x_end - self.min_x + 2)] = MapTile.CLAY.value

        # Normalize the water source X location too, then set the first visible tile under it to water
        self.flowing_water = [(0, 500 - self.min_x + 1)]
        self.still_water = []
        self.map[self.flowing_water[0]] = MapTile.FLOWING_WATER.value

    def flow_sideways(self, coord, new_flowing_water):
        """
        Flow water sideways
        coord: the coordinate to attempt to fill (to side of existing flowing water)
        new_flowing_water: list to add any new filled coords to
        return: True if more flowing can happen, False if it's time to stop
        """
        if self.map[coord] == MapTile.CLAY.value:
            # Bounded on this side
            return False

        if self.map[coord] != MapTile.FLOWING_WATER.value:
            # Not already flowing
            self.map[coord] = MapTile.FLOWING_WATER.value
            new_flowing_water.append(coord)

        if self.map[coord[0] + 1, coord[1]] not in (MapTile.CLAY.value, MapTile.STILL_WATER.value):
            # Fallen off the end of this level
            return False

        return True

    def check_bounded_water(self, coord):
        """
        Check for a bounded water volume, starting from flowing water
        coord: the starting flowing water coord to look left and right from
        return: bounded, min_x, max_x where bounded is True if this can be converted to still
        """
        min_x = coord[1]
        max_x = coord[1]
        bounded_left = False
        for x in range(coord[1] - 1, -1, -1):
            tile_type = self.map[coord[0], x]
            if tile_type == MapTile.CLAY.value:
                bounded_left = True
                min_x = x + 1
                break
            elif tile_type not in (MapTile.FLOWING_WATER.value, MapTile.STILL_WATER.value):
                break
            
            # Also, if the tile underneath isn't clay or still water, we are not bounded
            if self.map[coord[0] + 1, x] not in (MapTile.CLAY.value, MapTile.STILL_WATER.value):
                break

        bounded_right = False
        for x in range(coord[1] + 1, self.map.shape[1]):
            tile_type = self.map[coord[0], x]
            if tile_type == MapTile.CLAY.value:
                bounded_right = True
                max_x = x - 1
                break
            elif tile_type not in (MapTile.FLOWING_WATER.value, MapTile.STILL_WATER.value):
                break

            # Also, if the tile underneath isn't clay or still water, we are not bounded
            if self.map[coord[0] + 1, x] not in (MapTile.CLAY.value, MapTile.STILL_WATER.value):
                break

        return (bounded_left and bounded_right), min_x, max_x                            

    def challenge1(self):
        """
        Day 16 challenge 1
        """
        self.parse_input()

        # Start the water flowing (as 2). When no new tiles are filled, we're done
        did_something = True
        try:
            while did_something:
                did_something = False

                # Iteratively propagate the water! First, continue any downward flow
                # This is simply those tiles with flowing water above that are also sand
                new_flowing_water = []
                for coord in self.flowing_water:
                    coord_below = (coord[0] + 1, coord[1])
                    if coord_below[0] < self.map.shape[0] and self.map[coord_below] == MapTile.SAND.value:
                        self.map[coord_below] = MapTile.FLOWING_WATER.value
                        new_flowing_water.append(coord_below)
                        did_something = True
                
                # Add any new flowing water
                self.flowing_water += new_flowing_water

                # Now do any sideways filling
                # This is simply those tiles beside flowing water above clay or water which are also above clay or water
                new_flowing_water = []
                fw_indices_to_remove = set()
                for fw_index, coord in enumerate(self.flowing_water):
                    coord_below = (coord[0] + 1, coord[1])
                    if coord_below[0] < self.map.shape[0] and self.map[coord_below] in (MapTile.CLAY.value, MapTile.STILL_WATER.value):
                        # Propagate left
                        current_new_flowing_water = []
                        for x in range(coord[1] - 1, -1, -1):
                            if not self.flow_sideways((coord[0], x), current_new_flowing_water):
                                break

                        # Propagate right
                        for x in range(coord[1] + 1, self.map.shape[1]):
                            if not self.flow_sideways((coord[0], x), current_new_flowing_water):
                                break

                        # Do we need to convert this line to still water?
                        is_bounded, min_x, max_x = self.check_bounded_water(coord)
                        if is_bounded:
                            # Convert the line to still water
                            for x in range(min_x, max_x + 1):
                                self.map[coord[0], x] = MapTile.STILL_WATER.value
                                
                            self.still_water += current_new_flowing_water
                            fw_indices_to_remove.add(fw_index)
                            did_something = True
                        elif current_new_flowing_water:
                            # Add to our new flowing water list
                            new_flowing_water += current_new_flowing_water
                            did_something = True

                cropped_flowing_water = []
                for fw_index, coord in enumerate(self.flowing_water):
                    if fw_index not in fw_indices_to_remove:
                        if coord[0] < self.map.shape[0] - 1:
                            coord_below = (coord[0] + 1, coord[1])
                            coord_left = (coord[0], coord[1] - 1)
                            coord_right = (coord[0], coord[1] + 1)

                            # Remove flowing water from our "to-check" list if it has clay or still water below
                            # and has water either side. This is merely a speed optimization.
                            if (self.map[coord_below] in (MapTile.CLAY.value, MapTile.STILL_WATER.value)
                                and self.map[coord_left] == MapTile.FLOWING_WATER.value
                                and self.map[coord_right] == MapTile.FLOWING_WATER.value):
                                continue

                        cropped_flowing_water.append(coord)

                self.flowing_water = cropped_flowing_water

                # Add any new flowing water
                self.flowing_water += new_flowing_water
                print(f"Last flowing coord: {self.flowing_water[-1]}")
                
        except RuntimeError as ex:
            print(ex)

        # Debugging output
        im = Image.fromarray(self.map * 255 // 3, mode="L")
        im.save("out.png")

        # Count total water tiles (after first)
        water_tile_count = np.count_nonzero(self.map > 1)
        print(f"Water tile count: {water_tile_count}")

    def challenge2(self):
        """
        Day 16 challenge 2
        """
        # Count total water tiles (after first)
        water_tile_count = np.count_nonzero(self.map > 2)
        print(f"Still water tile count: {water_tile_count}")
