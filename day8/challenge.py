from aoc.challenge_base import ChallengeBase

class TreeNode:
    """
    Representation of tree node
    """
    def __init__(self, child_nodes, metadata):
        """
        Create a node
        child_nodes: list of TreeNode children
        metadata: list of metadata
        """
        self.child_nodes = child_nodes
        self.metadata = metadata
        
def build_subtree(data):
    """
    Parse a node of the tree recursively
    Return (TreeNode, remaining data)
    """
    child_node_count, metadata_count = data[0], data[1]
    data = data[2:]
    child_nodes = []
    for _ in range(child_node_count):
        child_node, data = build_subtree(data)
        child_nodes.append(child_node)

    metadata = data[:metadata_count]
    return TreeNode(child_nodes, metadata), data[metadata_count:]

def sum_metadata(node):
    """
    Walk the tree and sum the metadata
    """
    running_total = 0
    for child_node in node.child_nodes:
        running_total += sum_metadata(child_node)

    return running_total + sum(node.metadata)

def compute_value(node):
    """
    Walk the tree and compute the node value
    """
    # If it's a leaf, value is just the metadata sum
    if not node.child_nodes:
        return sum(node.metadata)

    # Otherwise, add value for each 1-indexed child node from metadata
    child_node_values = [compute_value(child_node) for child_node in node.child_nodes]
    value = 0
    for child_index in node.metadata:
        try:
            value += child_node_values[child_index - 1]
        except IndexError:
            pass

    return value

class Challenge(ChallengeBase):
    """
    Day 8 challenges
    """
    def parse_input(self):
        """
        Build tree from input
        """
        raw_data = [int(i) for i in self.lines[0].strip().split(" ")]
        self.tree, _ = build_subtree(raw_data)

    def challenge1(self):
        """
        Day 8 challenge 1
        """
        self.parse_input()

        total = sum_metadata(self.tree)
        print(f"Total metadata sum: {total}")

    def challenge2(self):
        """
        Day 8 challenge 2
        """
        value = compute_value(self.tree)
        print(f"Root node value: {value}")
