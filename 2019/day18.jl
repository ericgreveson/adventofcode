using LightGraphs

"""Get a set of all remaining keys in plans"""
remaining_keys(plans) = Set(vcat([[c for c in plan if c ∈ 'a':'z'] for plan in plans]...))

"""Get a dictionary of keychar => doorcoord for doors in plan"""
doorcoords(plan) = Dict(lowercase(plan[coord]) => coord for coord in CartesianIndices(plan) if plan[coord] ∈ 'A':'Z')

"""Build a graph with locked doors not included. Return graph, nodes, nodemap, keynodes, doornodes"""
function build_graph(plan)
    nodes = [coord for coord in CartesianIndices(plan) if plan[coord] != '#' && plan[coord] ∉ 'A':'Z']
    nodemap = Dict(coord => i for (i, coord) in enumerate(nodes))
    graph = SimpleGraph(length(nodes))
    keynodes = []
    doornodes = Dict(lowercase(plan[coord]) => coord for coord in CartesianIndices(plan) if plan[coord] ∈ 'A':'Z')
    for (i, coord) in enumerate(nodes)
        # Skip walls
        if plan[coord] == '#' continue end
        # Everything else is walkable, although we'll need keys to access the door nodes
        if plan[coord] != '@' && plan[coord] != '.'
            push!(keynodes, i)
        end
        # Add east and south edges (other nodes will add north and west for us)
        for offset in [CartesianIndex(0, 1), CartesianIndex(1, 0)]
            if (coord + offset) ∈ keys(nodemap) add_edge!(graph, i, nodemap[coord + offset]) end
        end
    end
    return graph, nodes, nodemap, keynodes, doornodes
end

"""Collect all keys in the plans recursively, returning the shortest distance to collect them"""
function collect_keys(plans, current_coords, cached_solutions=Dict())
    # Do we have an easy cached answer?
    search_state = (current_coords, remaining_keys(plans))
    if search_state in keys(cached_solutions) return cached_solutions[search_state] end
    # Have we actually collected all the keys?
    if isempty(last(search_state)) return 0 end

    path_lengths = []
    for (p, (plan, current_coord)) in enumerate(zip(plans, current_coords))
        # We need to exhaustively search all key pickups that are currently possible
        graph, nodes, nodemap, keynodes, doornodes = build_graph(plan)
        # Have we finished this plan?
        if length(keynodes) == 0 continue end
        possible_paths = []
        collected = []
        ds = dijkstra_shortest_paths(graph, nodemap[current_coord])
        for ki in keynodes
            if ds.pathcounts[ki] > 0
                path = enumerate_paths(ds, ki)
                # Skip any paths with more than one key on - the path to the first key will do just fine
                if length(keynodes ∩ path) > 1 continue end
                push!(possible_paths, path)
                push!(collected, plan[nodes[ki]])
            end
        end

        # For each potential path with a single key, unlock the corresponding door, then recursively search for the next move
        for path in possible_paths
            collected_key_coord = nodes[last(path)]
            # Clone list of all plans, then replace this one with a copy after moving along this path
            new_plans = copy(plans)
            new_plan = copy(plan)
            new_plans[p] = new_plan
            new_plan[collected_key_coord] = '.'
            # Figure out which plan the door was in and remove it
            for (op, otherplan) in enumerate(plans)
                dc = doorcoords(otherplan)
                if plan[collected_key_coord] ∈ keys(dc)
                    if op != p
                        # We have not yet copied this plan - clone it
                        new_plans[op] = copy(otherplan)
                    end
                    new_plans[op][dc[plan[collected_key_coord]]] = '.'
                    break
                end
            end
            new_coords = copy(current_coords)
            new_coords[p] = collected_key_coord
            push!(path_lengths, length(path) - 1 + collect_keys(new_plans, new_coords, cached_solutions))
        end
    end

    # Cache this solution in case we have another path ending at the same place in future
    cached_solutions[search_state] = minimum(path_lengths)
    if length(cached_solutions) % 100 == 0 println("Cached solutions: $(length(cached_solutions))") end
    return minimum(path_lengths)
end

function main()
    # Part 1: build graph of corridors, keys and doors, then solve for shortest path to get all keys
    # Sounds a bit travelling salesperson-y.
    plan = hcat(open(f -> collect.(readlines(f)), "day18_input.txt")...)
    shortest_dist = collect_keys([plan], [indexin('@', plan)[1]])
    println("Part 1: Shortest distance: $shortest_dist")

    # Part 2: this time there are 4 vaults with robots, one moving at a time. Patch and split the map.
    centre = (size(plan) .+ 1) .÷ 2
    replacement = ['@' '#' '@'; '#' '#' '#'; '@' '#' '@']
    plan[(centre[1]-1):(centre[1]+1), (centre[2]-1):(centre[2]+1)] = replacement
    subplans = [
        plan[1:(centre[1]-1), 1:(centre[2]-1)],
        plan[1:(centre[1]-1), (centre[2]+1):end],
        plan[(centre[1]+1):end, 1:(centre[2]-1)],
        plan[(centre[1]+1):end, (centre[2]+1):end]
    ]
    
    shortest_dist = collect_keys(subplans, [indexin('@', plan)[1] for plan in subplans])
    println("Part 2: Shortest distance: $shortest_dist")
end
main()