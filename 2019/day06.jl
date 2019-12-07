module AdventOfCode

mutable struct Node
    name::String
    children::Array{Node}
    parent::Union{Nothing, Node}
end

"""Build a tree from a list of [parent, child] pairs, assuming there is exactly one root node"""
function build_tree(orbits)
    nodes = Dict()
    for (orbitee, orbiter) in orbits
        orbiter_node = get!(nodes, orbiter, Node(orbiter, [], nothing))
        orbitee_node = get!(nodes, orbitee, Node(orbitee, [], nothing))
        orbiter_node.parent = orbitee_node
        push!(orbitee_node.children, orbiter_node)
    end
    return first(filter(n -> isnothing(n.parent), collect(values(nodes))))
end

# Part 1 - build orbit tree and compute depth of each node
orbits = open(f -> split.(readlines(f), ")"), "day06_input.txt")
tree = build_tree(orbits)
total_orbits(node::Node, depth=0) = depth + sum([total_orbits.(node.children, depth + 1); 0])
println("Total direct/indirect orbits: $(total_orbits(tree))")

# Part 2 - minimum orbital transfers from YOU to SAN
function get_ancestors(node::Node, name, ancestors=[])
    new_ancestors = [ancestors; node]
    if node.name == name return new_ancestors end
    for child in node.children
        child_result = get_ancestors(child, name, new_ancestors)
        if !isnothing(child_result) return child_result end
    end
    return nothing
end

you_nodes = get_ancestors(tree, "YOU")
santa_nodes = get_ancestors(tree, "SAN")
non_common_nodes = symdiff(reverse(you_nodes), santa_nodes)
print("Transfers: $(length(non_common_nodes) - 2)")

end