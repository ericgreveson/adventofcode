import numpy as np

from aoc.challenge_base import ChallengeBase

class Unit:
    """
    Goblin or elf unit
    """
    def __init__(self, x, y):
        """
        Constructor
        x, y: initial location of the unit
        """
        self.hp = 200
        self.attack = 3
        self.x = x
        self.y = y

class Goblin(Unit):
    """
    Goblin
    """
    def __init__(self, x, y):
        super().__init__(x, y)

class Elf(Unit):
    """
    Elf
    """
    def __init__(self, x, y):
        super().__init__(x, y)

class CombatEndError(RuntimeError):
    """
    Exception for when there are no more targets
    """
    def __init__(self):
        super().__init__()

class Challenge(ChallengeBase):
    """
    Day 15 challenges
    """
    def get_test_map_1(self):
        """
        Get the example map shown in the blurb
        """
        return ["#######",
                "#.G...#",
                "#...EG#",
                "#.#.#G#",
                "#..G#E#",
                "#.....#",
                "#######"]

    def get_test_map_2(self):
        """
        Get another example map shown in the blurb
        """
        return ["#######",
                "#G..#E#",
                "#E#E.E#",
                "#G.##.#",
                "#...#E#",
                "#...E.#",
                "#######"]

    def parse_raw_map(self, raw_map):
        """
        Convert input map into bool matrix (True is empty space) and unit list
        """
        base_map = np.zeros((len(raw_map), len(raw_map[0])), dtype=np.bool)
        units = []
        for y in range(base_map.shape[0]):
            for x in range(base_map.shape[1]):
                if raw_map[y][x] == ".":
                    base_map[y][x] = True
                elif raw_map[y][x] == "G":
                    base_map[y][x] = True
                    units.append(Goblin(x, y))
                elif raw_map[y][x] == "E":
                    base_map[y][x] = True
                    units.append(Elf(x, y))

        return base_map, units
        
    def adjacent_points(self, unit):
        """
        Get list of points adjacent to a unit that are not walls (may have units in though)
        """
        adj = []
        if unit.x > 0 and self.base_map[unit.y][unit.x - 1]:
            adj.append((unit.x - 1, unit.y))

        if unit.x < self.base_map.shape[1] - 1 and self.base_map[unit.y][unit.x + 1]:
            adj.append((unit.x + 1, unit.y))

        if unit.y > 0 and self.base_map[unit.y - 1][unit.x]:
            adj.append((unit.x, unit.y - 1))

        if unit.y < self.base_map.shape[0] - 1 and self.base_map[unit.y + 1][unit.x]:
            adj.append((unit.x, unit.y + 1))

        return adj

    def point_on_unit(self, x, y):
        """
        Is a point on a unit?
        """
        for u in self.units:
            if u.x == x and u.y == y:
                return True

        return False

    def adjacent_greater_equal_zero(self, dist, x, y):
        """
        Are there any points in dist adjacent to x, y that are >= 0?
        """
        if x > 0 and dist[y][x - 1] >= 0:
            return True

        if x < dist.shape[1] - 1 and dist[y][x + 1] >= 0:
            return True
            
        if y > 0 and dist[y - 1][x] >= 0:
            return True

        if y < dist.shape[0] - 1 and dist[y + 1][x] >= 0:
            return True

        return False

    def move_towards_closest(self, unit, all_adj):
        """
        Move unit towards the closest enemy-adjacent point in all_adj (tiebreak in reading order)
        """
        # Initialize a grid like the map, all -1 except for our current unit pos set to zero
        dist = -np.ones(self.base_map.shape, dtype=np.int16)
        dist[unit.y][unit.x] = 0

        # Quick lookup for adjacent point list and allowed coordinates (non-walls and non-friends)
        all_adj_lookup = {*all_adj}
        allowed_coords = np.copy(self.base_map)
        for u in self.units:
            if u is not unit and type(u) is type(unit):
                allowed_coords[u.y][u.x] = False

        # Start brute-force pathfinding. See if we can go in any 4-connected direction.
        # Record the shortest distance to this point if so
        current_dist = 0
        shortest_adj = []
        while not shortest_adj:
            current_dist += 1
            no_more_routes = True
            next_dist = dist.copy()
            for y in range(dist.shape[0]):
                for x in range(dist.shape[1]):
                    if dist[y][x] == -1 and allowed_coords[y][x] and self.adjacent_greater_equal_zero(dist, x, y):
                        next_dist[y][x] = current_dist
                        no_more_routes = False
                        if (x, y) in all_adj_lookup:
                            shortest_adj.append((x, y))

            dist = next_dist

            # Do we need to keep looking, or have we searched all possible paths now?
            if no_more_routes:
                break

        # Anywhere to go?
        if not shortest_adj:
            return

        # Tie-break with the reading-order first option in shortest_adj
        dest = sorted(shortest_adj, key=lambda p: p[1]*self.base_map.shape[1] + p[0])[0]

        # Are there multiple routes towards dest? We need to search from dest coord until hitting unit
        rev_dist = -np.ones(self.base_map.shape, dtype=np.int16)
        rev_dist[dest[1]][dest[0]] = 0
        current_dist = 0
        shortest_route_found = False
        while not shortest_route_found:
            current_dist += 1
            next_rev_dist = rev_dist.copy()
            for y in range(rev_dist.shape[0]):
                for x in range(rev_dist.shape[1]):
                    if rev_dist[y][x] == -1 and allowed_coords[y][x] and self.adjacent_greater_equal_zero(rev_dist, x, y):
                        next_rev_dist[y][x] = current_dist
                        if x == unit.x and y == unit.y:
                            # Arrived back to our current unit
                            shortest_route_found = True

            rev_dist = next_rev_dist

        # Figure out which of our unit-adjacent points can be used
        points_to_check = [(unit.x - 1, unit.y), (unit.x + 1, unit.y), (unit.x, unit.y - 1), (unit.x, unit.y + 1)]
        points_with_dists = []
        for point in points_to_check:
            if point[0] >= 0 and point[0] < rev_dist.shape[1] and point[1] >= 0 and point[1] < rev_dist.shape[0]:
                point_dist = rev_dist[point[1]][point[0]]
                if point_dist >= 0:
                    points_with_dists.append((point, point_dist))

        min_dist = min(points_with_dists, key=lambda pwd: pwd[1])[1]
        min_points = [pwd[0] for pwd in points_with_dists if pwd[1] == min_dist]

        # Tie-break with reading order
        move_coord = sorted(min_points, key=lambda p: p[1]*self.base_map.shape[1] + p[0])[0]

        # Move there!
        unit.x = move_coord[0]
        unit.y = move_coord[1]

    def run_turn(self, unit):
        """
        Run a full turn for a given unit
        """
        # Get all targets
        targets = list(filter(lambda u: type(u) is not type(unit), self.units))
        if not targets:
            # All enemy units are dead!
            raise CombatEndError()

        # Get adjacent points for all targets
        all_adj = set()
        for target in targets:
            all_adj = all_adj.union(set(filter(lambda p: not self.point_on_unit(*p), self.adjacent_points(target))))

        # Are we already in range of somebody?
        target_lookup = {(target.x, target.y): target for target in targets}
        adjacent_targets = set(self.adjacent_points(unit)).intersection(target_lookup.keys())
        if not adjacent_targets:
            # Move towards someone if possible
            self.move_towards_closest(unit, all_adj)

            # Are we next to somebody now?
            adjacent_targets = set(self.adjacent_points(unit)).intersection(target_lookup.keys())

        if adjacent_targets:
            # Find the target with lowest HP, tie-break with reading-order first point
            targets = [target_lookup[p] for p in adjacent_targets]
            min_hp = min(targets, key=lambda t: t.hp).hp
            targets = list(filter(lambda t: t.hp == min_hp, targets))
            target = sorted(targets, key=lambda t: t.y*self.base_map.shape[1] + t.x)[0]

            # Do the attack
            target.hp -= unit.attack
            if target.hp <= 0:
                # It's dead, remove it
                self.units.remove(target)

    def print_board(self):
        """
        Write board to stdout
        """
        unit_lookup = {(u.x, u.y): u for u in self.units}
        for y in range(self.base_map.shape[0]):
            out_line = ""
            row_unit_hps = []
            for x in range(self.base_map.shape[1]):
                if (x, y) in unit_lookup:
                    out_line += "E" if type(unit_lookup[(x, y)]) is Elf else "G"
                    row_unit_hps.append(unit_lookup[(x, y)].hp)
                else:
                    out_line += "." if self.base_map[y][x] else "#"
            print(f"{out_line} {row_unit_hps}")

        print("")

    def run_full_combat(self):
        """
        Run the full combat until all units of one side are dead, returning the last completed round
        """
        # Run combat rounds
        round = 0
        try:
            while True:
                round += 1
                ordered_units = sorted(self.units, key=lambda unit: unit.y*self.base_map.shape[1] + unit.x)
                for unit in ordered_units:
                    # Is this unit still alive?
                    if unit in self.units:
                        # Run this unit's turn
                        self.run_turn(unit)

                # Show the round result
                print(f"End of round {round}. Remaining total HP: {sum([unit.hp for unit in self.units])}")

        except CombatEndError:
            self.print_board()
            print(f"Combat ended after round {round - 1} was completed")
            return round - 1

    def challenge1(self):
        """
        Day 15 challenge 1
        """
        return
        # Load the base map (change this for a test map if you like)
        self.base_map, self.units = self.parse_raw_map(self.lines)

        # Run the combat
        last_round = self.run_full_combat()

        print(f"Outcome: {last_round * sum([unit.hp for unit in self.units])}")

    def challenge2(self):
        """
        Day 15 challenge 2
        """
        # Start simulations with increasing Elf attack power until they win with no loss
        for elf_attack_power in range(4, 100):
            print(f"Simulation running with elf attack power = {elf_attack_power}")

            # Back to square one
            self.base_map, self.units = self.parse_raw_map(self.lines)
            initial_elf_count = len([unit for unit in self.units if type(unit) is Elf])

            # Power up the Elves
            for unit in self.units:
                if type(unit) is Elf:
                    unit.attack = elf_attack_power

            # Run the combat
            last_round = self.run_full_combat()

            # Did all elves survive?
            remaining_elf_count = len([unit for unit in self.units if type(unit) is Elf])
            if remaining_elf_count == initial_elf_count:
                print(f"Minimum Elf attack power for all elves to survive: {elf_attack_power}")
                print(f"Outcome: {last_round * sum([unit.hp for unit in self.units])}")
                break
            else:
                print(f"Only {remaining_elf_count} Elves survived :(")
