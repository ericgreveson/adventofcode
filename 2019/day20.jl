using LightGraphs

forward_directions = CartesianIndex.([(1, 0), (0, 1)])
directions = [forward_directions; -forward_directions]

"""Find a label adjacent to a corridor at coord, return nothing if there is none"""
function find_adjacent_label(plan, coord)
    for dir in directions
        if plan[coord + dir] ∈ 'A':'Z'
            label = string(plan[coord + dir], plan[coord + 2dir])
            if dir ∉ forward_directions label = reverse(label) end
            return label
        end
    end
    return nothing
end

"""Build a (non recursive) graph from the plan ASCII art matrix passed in"""
function parse_plan(plan)
    # Build graph of connected corridors and portals
    nodes = [coord for coord in CartesianIndices(plan) if plan[coord] == '.']
    nodemap = Dict(coord => i for (i, coord) in enumerate(nodes))
    graph = SimpleGraph(length(nodes))
    labels = Dict(coord => find_adjacent_label(plan, coord) for coord in nodes)
    # Add edges between corridors
    for (i, coord) in enumerate(nodes)
        for dir in forward_directions
            if (coord + dir) ∈ keys(nodemap) add_edge!(graph, i, nodemap[coord + dir]) end
        end
    end
    # Add edges between portals
    labelmap = Dict()
    portals_first = Dict(labels[coord] => coord for coord in nodes if !isnothing(labels[coord]))
    portals_second = Dict(labels[coord] => coord for coord in reverse(nodes) if !isnothing(labels[coord]))
    for (label, coord) in portals_first
        second_coord = portals_second[label]
        if second_coord != coord
            add_edge!(graph, nodemap[coord], nodemap[second_coord])
            labelmap[label] = (coord, second_coord)
        else
            labelmap[label] = coord
        end
    end
    return graph, nodes, nodemap, labelmap
end

"""Build a recursive graph from the plan ASCII art matrix passed in, with levels layers of recursion"""
function parse_plan_recursive(plan, levels)
    # Build graph of connected corridors and portals
    nodes = [coord for coord in CartesianIndices(plan) if plan[coord] == '.']
    nodemap = Dict(coord => i for (i, coord) in enumerate(nodes))
    labels = Dict(coord => find_adjacent_label(plan, coord) for coord in nodes)
    npl = length(nodes)
    graph = SimpleGraph(npl * levels)
    # Add edges between corridors
    for level in 0:(levels-1)
        for (i, coord) in enumerate(nodes)
            for dir in forward_directions
                if (coord + dir) ∈ keys(nodemap) add_edge!(graph, npl * level + i, npl * level + nodemap[coord + dir]) end
            end
        end
    end
    # Add edges between portals from level n to level n+1
    outer_x = extrema(map(x -> x[1], nodes))
    outer_y = extrema(map(x -> x[2], nodes))
    outer = Dict(label => coord for (coord, label) in labels if coord[1] ∈ outer_x || coord[2] ∈ outer_y && !isnothing(label))
    inner = Dict(label => coord for (coord, label) in labels if coord[1] ∉ outer_x && coord[2] ∉ outer_y && !isnothing(label))
    for level in 0:(levels-2)
        for label in keys(inner)
            add_edge!(graph, npl * level + nodemap[inner[label]], npl * (level + 1) + nodemap[outer[label]])
        end
    end
    return graph, nodes, nodemap, outer
end

# Part 1: shortest path through maze
plan = hcat(open(f -> collect.(readlines(f)), "day20_input.txt")...)
graph, nodes, nodemap, labelmap = parse_plan(plan)
shortest_path = yen_k_shortest_paths(graph, nodemap[labelmap["AA"]], nodemap[labelmap["ZZ"]]).dists[1]
println("Part 1: Shortest path: $(shortest_path) steps")

# Part 2: build recursive maze, although just pretend and use a fixed number of levels (bit brute forcey but whatevs)
plan = hcat(open(f -> collect.(readlines(f)), "day20_input.txt")...)
graph, nodes, nodemap, labelmap = parse_plan_recursive(plan, 40)
shortest_path = yen_k_shortest_paths(graph, nodemap[labelmap["AA"]], nodemap[labelmap["ZZ"]]).dists[1]
println("Part 2: Shortest path: $(shortest_path) steps")