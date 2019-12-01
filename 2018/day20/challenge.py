import numpy as np

from aoc.challenge_base import ChallengeBase

class RoomNode:
    """
    Graph node representing a room
    """
    def __init__(self, pos):
        """
        Constructor
        pos: (y, x) coord of room in map
        """
        self.pos = pos
        self.north = None
        self.east = None
        self.south = None
        self.west = None

    def count_connections(self):
        """
        Return number of connections
        """
        return (1 if self.north else 0) + (1 if self.east else 0) + (1 if self.south else 0) + (1 if self.west else 0)

class Challenge(ChallengeBase):
    """
    Day 18 challenges
    """
    def draw_map(self, fileobj):
        """
        Draw the map to file-like object fileobj
        """
        for y in range(self.rooms.shape[0]):
            line = ""
            for x in range(self.rooms.shape[1]):
                node = self.nodes[self.rooms[y, x]]
                if (y, x) == self.start_room_pos:
                    line += "X"
                elif node.north and node.east and node.south and node.west:
                    line += "+"
                elif node.count_connections() == 3:
                    line += "3"
                elif node.count_connections() == 2:
                    line += "2"
                elif node.north:
                    line += "'"
                elif node.east:
                    line += ">"
                elif node.south:
                    line += "."
                elif node.west:
                    line += "<"
                else:
                    raise RuntimeError("Unconnected node!")

            print(line, file=fileobj)

    def get_or_create_node(self, new_pos):
        """
        Get existing node in given pos, creating it if it doesn't exist
        """
        if self.rooms[new_pos] >= 0:
            return self.nodes[self.rooms[new_pos]]

        self.rooms[new_pos] = len(self.nodes)
        self.nodes.append(RoomNode(new_pos))
        return self.nodes[-1]

    def move_to(self, current_pos, direction):
        """
        Move position, adding to map if need be
        current_pos: where to move from
        direction: direction to move
        return: new_pos
        """
        current_node = self.nodes[self.rooms[current_pos]]
        if direction == "N":
            new_pos = (current_pos[0]-1, current_pos[1])
            new_room = self.get_or_create_node(new_pos)
            current_node.north = new_room
            new_room.south = current_node
        elif direction == "E":
            new_pos = (current_pos[0], current_pos[1]+1)
            new_room = self.get_or_create_node(new_pos)
            current_node.east = new_room
            new_room.west = current_node
        elif direction == "S":
            new_pos = (current_pos[0]+1, current_pos[1])
            new_room = self.get_or_create_node(new_pos)
            current_node.south = new_room
            new_room.north = current_node
        elif direction == "W":
            new_pos = (current_pos[0], current_pos[1]-1)
            new_room = self.get_or_create_node(new_pos)
            current_node.west = new_room
            new_room.east = current_node
        
        return new_pos

    def parse_regex(self, regex, current_pos, parsing_group=False, global_char_index=0):
        """
        Parse regex recursively
        regex: the thing to parse
        current_pos: current map location
        return: the index of the last parsed character in regex
        """
        original_pos = current_pos
        index = 0
        while index < len(regex):
            c = regex[index]
            if c in ("N", "E", "S", "W"):
                current_pos = self.move_to(current_pos, c)
            elif c == "(":
                # We need to move down an option-level
                last_index = self.parse_regex(regex[index+1:],
                                                current_pos,
                                                parsing_group=True,
                                                global_char_index=global_char_index + index)

                # Jump ahead past this group
                index += last_index + 1
            elif c == ")":
                if not parsing_group:
                    raise RuntimeError(f"Character {global_char_index + index}: Not expecting )")
                
                return index
            elif c == "|":
                if not parsing_group:
                    raise RuntimeError(f"Character {global_char_index + index}: Not expecting |")

                # We have a new option group
                current_pos = original_pos
            else:
                raise RuntimeError(f"Character {global_char_index + index}: Unexpected character: {c}")

            index += 1

        return len(regex) - 1

    def crop_map(self):
        """
        Crop the map to the area with rooms
        """
        is_room = self.rooms >= 0
        min_x = is_room.shape[1]
        min_y = is_room.shape[0]
        max_x = 0
        max_y = 0
        for y in range(is_room.shape[0]):
            if np.count_nonzero(is_room[y, :]) > 0:
                if y < min_y:
                    min_y = y

                if y > max_y:
                    max_y = y

                for x in range(is_room.shape[1]):
                    if is_room[y, x]:
                        if x < min_x:
                            min_x = x

                        if x > max_x:
                            max_x = x

        self.rooms = self.rooms[min_y:max_y+1, min_x:max_x+1]
        self.start_room_pos = (self.start_room_pos[0] - min_y, self.start_room_pos[1] - min_x)
        for node in self.nodes:
            node.pos = (node.pos[0] - min_y, node.pos[1] - min_x)

    def compute_map(self):
        """
        Parse the regex and build the map of rooms and doors
        """
        self.regex = self.lines[0].strip()
        if self.regex[0] != "^" or self.regex[-1] != "$":
            raise RuntimeError("Unexpected regex")

        # Compute maximum possible distance N, E, S and W from current point
        regex_inner = self.regex[1:-1]
        direction_counts = {d: len([c for c in regex_inner if c == d]) for d in ["N", "E", "S", "W"]}
        max_width = direction_counts["E"] + direction_counts["W"] + 1
        max_height = direction_counts["N"] + direction_counts["S"] + 1

        # Allocate room node map with -1s everywhere
        self.rooms = -np.ones((max_height + 1, max_width + 1), dtype=np.int32)

        # Initialize map with starting room node
        self.start_room_pos = (direction_counts["N"], direction_counts["W"])
        self.nodes = [RoomNode(self.start_room_pos)]
        self.rooms[self.start_room_pos] = 0

        # Now parse the regex and build the map
        self.parse_regex(regex_inner, self.start_room_pos)

        # Finally, crop the map to the area with rooms only
        self.crop_map()

    def compute_node_distances(self):
        """
        Compute shortest distances from start node to all other nodes
        """
        # Implement Dijkstra algorithm (the one in scipy looks like an all-pairs algo which we don't need)
        unvisited = set(range(len(self.nodes)))
        dists = [np.iinfo(np.int32).max] * len(self.nodes)
        dists[0] = 0

        while unvisited:
            # Find the next closest unvisited node
            node_index = min(unvisited, key=lambda i: dists[i])

            # Visit it
            unvisited.remove(node_index)
            node = self.nodes[node_index]
            for adjacent_node in [node.north, node.east, node.south, node.west]:
                if adjacent_node:
                    adjacent_node_index = self.rooms[adjacent_node.pos]
                    if adjacent_node_index in unvisited:
                        possible_dist = dists[node_index] + 1
                        dists[adjacent_node_index] = min(dists[adjacent_node_index], possible_dist)

        return dists

    def challenge1(self):
        """
        Day 20 challenge 1
        """
        self.compute_map()

        with open("out.txt", "wt") as f:
            self.draw_map(f)

        # Find most distant room
        self.dists = self.compute_node_distances()
        print(f"Furthest room is {max(self.dists)} doors away")

    def challenge2(self):
        """
        Day 20 challenge 2
        """
        distant_rooms = np.count_nonzero(np.asarray(self.dists) >= 1000)
        print(f"There are {distant_rooms} rooms at least 1000 doors away")
