import numpy as np

from aoc.challenge_base import ChallengeBase

class Challenge(ChallengeBase):
    """
    Day 22 challenges
    """
    def erosion_level(self, geologic_index):
        """
        Compute erosion level from geologic index
        """
        return (self.depth + geologic_index) % 20183

    def build_erosion_map(self, map_size):
        """
        Create erosion map from rules
        map_size: the (y, x) extent of the map
        """
        # Build map of erosion indices containing mouth (0, 0) and target
        self.erosion = np.zeros(map_size, dtype=np.int32)

        # Set erosion indices per the rules
        self.erosion[0, 0] = self.erosion[-1, -1] = self.erosion_level(0)
        for y in range(self.erosion.shape[0]):
            self.erosion[y, 0] = self.erosion_level(y * 48271)

        for x in range(self.erosion.shape[1]):
            self.erosion[0, x] = self.erosion_level(x * 16807)

        for y in range(1, self.erosion.shape[0]):
            for x in range(1, self.erosion.shape[1]):
                self.erosion[y, x] = self.erosion_level(self.erosion[y, x-1] * self.erosion[y-1, x])

    def reconstruct_path(self, came_from, current):
        """
        Reconstruct path from start to current for A* search
        """
        path = [current.coord]
        while current in came_from.keys():
            current = came_from[current]
            path.append(current.coord)

        return list(reversed(path))

    def a_star_search(self):
        """
        A* search for best path to self.target from (0, 0)
        return: best node path
        """
        # Tools: 0=none, 1=torch, 2=climbing. We start with the torch.
        # If none (0) is equipped, type 0 (rocky) cannot be traversed
        # If torch (1) is equipped, type 1 (wet) cannot be traversed
        # If climbing (2) is equipped, type 2 (narrow) cannot be traversed
        class Node:
            """
            Class representing graph node
            """
            def __init__(self, coord):
                """
                Constructor
                coord: (y, x, tool) location of node
                """
                self.coord = coord
                self.neighbours = []
                self.f_score = np.iinfo(np.int32).max
                self.g_score = np.iinfo(np.int32).max

        # Build node graph from map
        # Insert special "tool change" nodes too for each grid square
        graph_nodes = []
        index_map = -1 * np.ones((self.types.shape[0], self.types.shape[1], 3), dtype=np.int32)
        for y in range(self.types.shape[0]):
            for x in range(self.types.shape[1]):
                for tool in range(3):
                    if self.types[y, x] != tool:
                        index_map[y, x, tool] = len(graph_nodes)
                        graph_nodes.append(Node((y, x, tool)))
                    
        # Link up all edges to adjacent nodes
        for y in range(self.types.shape[0]):
            for x in range(self.types.shape[1]):
                for tool in range(3):
                    if index_map[y, x, tool] >= 0:
                        central_node = graph_nodes[index_map[y, x, tool]]

                        # Allow switch to other tool
                        other_tool = ((tool + 1) % 3) if ((tool + 1) % 3) != self.types[y, x] else ((tool + 2) % 3)
                        central_node.neighbours.append(graph_nodes[index_map[y, x, other_tool]])

                        # Allow movement to neighbours allowed by current tool
                        if y > 0 and self.types[y-1, x] != tool:
                            central_node.neighbours.append(graph_nodes[index_map[y-1, x, tool]])
                        if x > 0 and self.types[y, x-1] != tool:
                            central_node.neighbours.append(graph_nodes[index_map[y, x-1, tool]])
                        if y < index_map.shape[0] - 1 and self.types[y+1, x] != tool:
                            central_node.neighbours.append(graph_nodes[index_map[y+1, x, tool]])
                        if x < index_map.shape[1] - 1 and self.types[y, x+1] != tool:
                            central_node.neighbours.append(graph_nodes[index_map[y, x+1, tool]])

        # Now we need to find a shortest route. A* algorithm is probably a good first choice...
        # We will need a priority queue of nodes to visit
        open_nodes = {graph_nodes[0]}
        closed_nodes = set()
        came_from = dict()

        # Known cost of start to node: infinity everywhere except start where it's 0
        graph_nodes[0].g_score = 0
        # Current best paths: heuristic for start node only at this point
        graph_nodes[0].f_score = self.target[0] + self.target[1]

        while open_nodes:
            # Visit the min of open nodes
            curr = min(open_nodes, key=lambda n: n.f_score)
            if curr.coord == (self.target[0], self.target[1], 1):
                return self.reconstruct_path(came_from, curr)

            # Move the current node from open to closed
            open_nodes.remove(curr)
            closed_nodes.add(curr)

            # See where we can go from the current node
            for neigh in curr.neighbours:
                # Skip closed nodes
                if neigh in closed_nodes:
                    continue

                # Compute cost to move to neighbour
                tentative_g_score = curr.g_score
                tentative_g_score += abs(neigh.coord[0] - curr.coord[0]) + abs(neigh.coord[1] - curr.coord[1])
                tentative_g_score += 7 if neigh.coord[2] != curr.coord[2] else 0

                # Open up if it's a new undiscovered node, otherwise check if the score is better
                if neigh not in open_nodes:
                    open_nodes.add(neigh)
                elif tentative_g_score >= neigh.g_score:
                    continue  

                # Best path so far, record it
                came_from[neigh] = curr
                neigh.g_score = tentative_g_score

                # Cost estimate for remainder of path can simply be dy + dx (underestimate is better
                # than overestimate as we want an admissible heuristic)
                heuristic_score = abs(neigh.coord[0] - self.target[0]) + abs(neigh.coord[1] - self.target[1])
                # If we don't have the torch equipped, we will need to pay to do that too at some point
                if neigh.coord[2] != 1:
                    heuristic_score += 7

                neigh.f_score = neigh.g_score + heuristic_score

        raise RuntimeError("Failed to find anything")

    def challenge1(self):
        """
        Day 22 challenge 1
        """
        self.depth = 5913
        self.target = (701, 8) # y, x for numpy ease of use
        self.build_erosion_map((self.target[0] + 1, self.target[1] + 1))

        # Compute risk index
        risk_wet = np.count_nonzero(self.erosion % 3 == 1)
        risk_narrow = 2 * np.count_nonzero(self.erosion % 3 == 2)
        print(f"Total risk: {risk_wet + risk_narrow}")

    def challenge2(self):
        """
        Day 22 challenge 2
        """
        # Build a bigger map as we might have to go past the target for best results
        self.build_erosion_map((self.target[0] + 150, self.target[1] + 70))

        # Replace with a (0, 1, 2)-keyed type map
        self.types = self.erosion.copy()
        self.types[self.erosion % 3 == 0] = 0
        self.types[self.erosion % 3 == 1] = 1
        self.types[self.erosion % 3 == 2] = 2

        # Find best path through the cave
        best_path = self.a_star_search()
        
        # Evaluate total time for the path
        total_time = 0
        for index, current_node in enumerate(best_path[:-1]):
            # Is the next node a tool change node or a movement node?
            if best_path[index + 1] != current_node[2]:
                total_time += 7
            else:
                total_time += 1

        print(f"Best path time: {total_time}")