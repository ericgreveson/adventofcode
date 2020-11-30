include("intcode.jl")
using Images: save, Gray
using LightGraphs

function render(plan, file)
    mincol, maxcol = extrema(first.(keys(plan)))
    minrow, maxrow = extrema(last.(keys(plan)))
    screen = zeros(Int32, maxrow - minrow + 1, maxcol - mincol + 1)
    for (coord, val) in plan
        screen[last(coord) - minrow + 1, first(coord) - mincol + 1] = val + 1
    end
    save(file, Gray.(screen / 4))
end

"""Explore the map to get a plan. Return the plan when all tiles are explored."""
function explore(input, output)
    # Plan: 0 means known space, 1 means wall, 2 means oxygen system, 3 (internal only) means fully explored
    pos = [0 0]
    plan = Dict(pos => 0)
    # Directions North, South, West, East correspond to commands 1 to 4
    cardinal_directions = [[0 -1], [0 1], [-1 0], [1 0]]
    oxygen_system_pos = nothing

    while true
        moved = false
        for (cmd, vec) in enumerate(cardinal_directions)
            # Have we already taken a look at this one? If so, skip it
            new_pos = pos + vec
            if new_pos ∈ keys(plan) continue end
        
            # Can we move in this direction?
            put!(input, cmd)
            result = take!(output)
            if result == 0
                # It's a wall, mark it as such
                plan[new_pos] = 1
            elseif result ∈ [1, 2]
                # We have moved to a previously unknown space, or the oxygen system space
                plan[new_pos] = 0
                pos = new_pos
                moved = true
                if result == 2 oxygen_system_pos = new_pos end
                break
            end
        end

        if !moved
            # We've looked at all directions from here now. Mark it as complete and move elsewhere
            plan[pos] = 3
            for (cmd, vec) in enumerate(cardinal_directions)
                if plan[pos + vec] == 0
                    moved = true
                    put!(input, cmd)
                    take!(output)
                    pos += vec
                    break
                end
            end
        end

        if !moved break end
    end

    plan[oxygen_system_pos] = 2
    return Dict(k => plan[k] == 3 ? 0 : plan[k] for k in keys(plan))
end

"""Create graph from plan, returning graph, index of start node, and index of the oxygen system node"""
function make_graph(plan)
    space_nodes = [k for k in keys(plan) if plan[k] ∈ [0, 2]]
    index_lookup = Dict(k => i for (i, k) in enumerate(space_nodes))
    graph = SimpleGraph(length(space_nodes))
    start_node = -1
    oxygen_system_node = -1
    for (i, k) in enumerate(space_nodes)
        # Each node can add its E and S neighbours if they exist (N and W will be added by another node)
        for neighbour in [k + [1 0], k + [0 1]]
            if neighbour ∈ keys(index_lookup) add_edge!(graph, i, index_lookup[neighbour]) end
        end
        if k == [0 0] start_node = i end
        if plan[k] == 2 oxygen_system_node = i end
    end
    return graph, start_node, oxygen_system_node
end

function main()
    # Part 1: find the oxygen system and its min-path distance from start point
    prog = open(f -> parse.(Int64, split(readline(f), ",")), "day15_input.txt")
    input = Channel(1)
    output = Channel(1)
    @async run_intcode!(copy(prog), input, output)
    plan = explore(input, output)
    render(plan, "day15_result.png")
    graph, start_node, oxygen_system_node = make_graph(plan)
    dijkstra_state = dijkstra_shortest_paths(graph, oxygen_system_node)
    println("Shortest path length: $(dijkstra_state.dists[start_node])")

    # Part 2: max distance from oxygen system
    println("Time for oxygen to fill all spaces: $(maximum(dijkstra_state.dists))")
end
main()