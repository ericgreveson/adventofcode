using LightGraphs

"""Build a graph with locked doors not included. Return graph, nodes, nodemap, keynodes, doornodes, entrance"""
function build_graph(plan)
    nodes = [coord for coord in CartesianIndices(plan) if plan[coord] != '#' && plan[coord] ∉ 'A':'Z']
    nodemap = Dict(coord => i for (i, coord) in enumerate(nodes))
    graph = SimpleGraph(length(nodes))
    keynodes = []
    doornodes = Dict(lowercase(plan[coord]) => coord for coord in CartesianIndices(plan) if plan[coord] ∈ 'A':'Z')
    entrance = nothing
    for (i, coord) in enumerate(nodes)
        # Skip walls
        if plan[coord] == '#' continue end
        # Everything else is walkable, although we'll need keys to access the door nodes
        if plan[coord] == '@'
            entrance = i
        elseif plan[coord] != '.'
            push!(keynodes, i)
        end
        # Add east and south edges (other nodes will add north and west for us)
        for offset in [CartesianIndex(0, 1), CartesianIndex(1, 0)]
            if (coord + offset) ∈ keys(nodemap) add_edge!(graph, i, nodemap[coord + offset]) end
        end
    end
    return graph, nodes, nodemap, keynodes, doornodes, entrance
end

"""Collect all keys in the plan recursively, returning the shortest distance to collect them"""
function collect_keys(plan, current_coord=nothing, cached_solutions=Dict())
    # We need to exhaustively search all key pickups that are currently possible
    graph, nodes, nodemap, keynodes, doornodes, entrance = build_graph(plan)
    # Have we finished?
    if length(keynodes) == 0 return 0 end
    # Are we just starting?
    if isnothing(current_coord) current_coord = nodes[entrance] end
    # Do we have an easy answer?
    search_state = (current_coord, Set(map(x -> nodes[x], keynodes)))
    if search_state in keys(cached_solutions) return cached_solutions[search_state] end
    possible_paths = []
    collected = []
    for ki in keynodes
        state = yen_k_shortest_paths(graph, nodemap[current_coord], ki)
        if length(state.dists) > 0
            push!(possible_paths, state.paths[1])
            push!(collected, plan[nodes[ki]])
        end
    end

    # For each potential path, unlock all doors on it, then recursively search for the next move
    path_lengths = []
    for path in possible_paths
        collected_keys = keynodes ∩ path
        # Skip any paths with more than one key on - the path to the first key will do just fine
        if length(collected_keys) > 1 continue end
        new_plan = copy(plan)
        new_plan[map(ki -> nodes[ki], collected_keys)] = repeat(['.'], length(collected_keys))
        unlocked_door_coords = [doornodes[plan[nodes[ki]]] for ki in collected_keys if plan[nodes[ki]] ∈ keys(doornodes)]
        new_plan[unlocked_door_coords] = repeat(['.'], length(unlocked_door_coords))
        push!(path_lengths, length(path) - 1 + collect_keys(new_plan, nodes[last(path)], cached_solutions))
    end
    # Cache this solution in case we have another path ending at the same place in future
    cached_solutions[search_state] = minimum(path_lengths)
    println("Cached solutions: $(length(cached_solutions))")
    return minimum(path_lengths)
end

function main()
    # Part 1: build graph of corridors, keys and doors, then solve for shortest path to get all keys
    # Sounds a bit travelling salesperson-y.
    plan = hcat(open(f -> collect.(readlines(f)), "day18_input.txt")...)
    shortest_dist = collect_keys(plan)
    println("Shortest distance: $shortest_dist")

    # Part 2: this time there are 4 vaults with robots, one moving at a time.
end
main()