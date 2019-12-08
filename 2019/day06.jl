module AdventOfCode

mutable struct Node
    name::String
    children::Array{Node}
    parent::Union{Nothing, Node}
end

depth(node::Node) = isnothing(node.parent) ? 0 : (depth(node.parent) + 1)
ancestors(node::Node) = isnothing(node.parent) ? [] : [node.parent; ancestors(node.parent)]

"""Return Dict(name => Node) from list of [parent, child] pairs"""
function build_tree(orbits)
    nodes = Dict()
    for (orbitee, orbiter) in orbits
        orbiter_node = get!(nodes, orbiter, Node(orbiter, [], nothing))
        orbitee_node = get!(nodes, orbitee, Node(orbitee, [], nothing))
        orbiter_node.parent = orbitee_node
        push!(orbitee_node.children, orbiter_node)
    end
    return nodes
end

# Part 1 - build orbit tree and compute depth of each node
orbits = open(f -> split.(readlines(f), ")"), "day06_input.txt")
nodes = build_tree(orbits)
println("Total direct/indirect orbits: $(sum(depth.(values(nodes))))")

# Part 2 - minimum orbital transfers from YOU to SAN
you_nodes = ancestors(nodes["YOU"])
santa_nodes = ancestors(nodes["SAN"])
non_common_nodes = symdiff(you_nodes, santa_nodes)
print("Transfers: $(length(non_common_nodes))")

end