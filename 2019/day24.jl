# Part 1: evolve until we get a repeated state, then report its "biodiversity"
dirs = CartesianIndex.([(0, -1), (1, 0), (0, 1), (-1, 0)])
biodiversity(plan) = sum([2^(i-1) for (i, v) in enumerate(plan) if v])
adjacent(plan, coord) = [try plan[coord + dir] catch BoundsError; false end for dir in dirs]

"""Evolve the plan state, returning new state. adjacency_func should return array of adjacent values"""
function evolve(plan, adjacency_func)
    new_plan = copy(plan)
    for coord in CartesianIndices(plan)
        adjacent_count = sum(adjacency_func(plan, coord))
        if plan[coord] && adjacent_count != 1
            new_plan[coord] = false
        elseif !plan[coord] && adjacent_count ∈ 1:2
            new_plan[coord] = true
        end
    end
    return new_plan
end

"""Find first repeated state, returning its biodiversity"""
function find_first_repeat(plan)
    states = Set()
    while true
        bd = biodiversity(plan)
        if bd ∈ states return bd end
        push!(states, bd)
        plan = evolve(plan, adjacent)
    end
end

plan = hcat(open(f -> collect.(readlines(f)), "day24_input.txt")...) .== '#'
println("Biodiversity of first repeated state: $(find_first_repeat(plan))")

# Part 2: recursive bugs. Count total bugs after n=200 evolutions. Our plan is 3D this time
# Third dimension of the plan is 2n+1 long, 1:n are "outer", n+1 is initial, n+2:end are "inner"
function adjacent_3d(plan_3d, coord)
    adj = []
    sx, sy, sz = size(plan_3d)
    mx, my = (sx+1)÷2, (sy+1)÷2
    # Centre squares are meaningless now
    if (coord[1], coord[2]) == (mx, my) return [false] end
    for dir in dirs
        x, y, z = (coord + CartesianIndex((dir[1], dir[2], 0))).I
        try
            if x == 0 # Past left edge, go "out" a level
                push!(adj, plan_3d[CartesianIndex((mx-1, my, z-1))])
            elseif x == sx+1 # Past right edge, go "out" a level
                push!(adj, plan_3d[CartesianIndex((mx+1, my, z-1))])
            elseif y == 0 # Past top edge, go "out" a level
                push!(adj, plan_3d[CartesianIndex((mx, my-1, z-1))])
            elseif y == sy+1 # Past bottom edge, go "out" a level
                push!(adj, plan_3d[CartesianIndex((mx, my+1, z-1))])
            elseif x == mx && y == my # Centre square, go "in" a level, find sx/sy adjacent squares
                if coord[1] == mx-1 # Left edge of inner level
                    append!(adj, plan_3d[CartesianIndices((1, 1:sy, z+1))])
                elseif coord[1] == mx+1 # Right edge of inner level
                    append!(adj, plan_3d[CartesianIndices((sx, 1:sy, z+1))])
                elseif coord[2] == my-1 # Top edge of inner level
                    append!(adj, plan_3d[CartesianIndices((1:sx, 1, z+1))])
                elseif coord[2] == my+1 # Bottom edge of inner level
                    append!(adj, plan_3d[CartesianIndices((1:sx, sy, z+1))])
                end
            else # our old fashioned simple case
                push!(adj, plan_3d[CartesianIndex((x, y, z))])
            end
        catch BoundsError
            push!(adj, false)
        end
    end
    return adj
end

n = 200
plan_3d = zeros(Bool, size(plan)..., 2n+1)
plan_3d[:, :, n+1] = plan
evolved = foldl((x, y) -> evolve(x, adjacent_3d), 1:n, init=plan_3d)
println("Total bugs after $n evolutions: $(sum(evolved))")