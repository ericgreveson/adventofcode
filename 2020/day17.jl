module day17

data = Array{Bool}(hcat(map(line -> map(c -> c == '#', collect(line)), readlines("day17_input.txt"))...)')
steps = 6

# Part 1
function simulate(current)
    next = copy(current)
    region = CartesianIndices(current)
    ifirst, ilast = first(region), last(region)
    iunit = oneunit(ifirst)
    for i in region
        neighbours = [current[j] for j in max(ifirst, i - iunit):min(ilast, i + iunit) if j != i]
        if (current[i] && count(neighbours) ∉ [2, 3]) next[i] = false end
        if (!current[i] && count(neighbours) == 3) next[i] = true end
    end
    next
end

function runall(dim)
    grid = zeros(Bool, map(+, (size(data)..., fill(1, dim-2)...), tuple(fill(steps*2, dim)...)))
    s = steps + 1
    e = s + first(size(data)) - 1
    grid[s:e, s:e, fill(s:s, dim-2)...] = data
    for i in 1:steps
        grid = simulate(grid)
    end
    grid
end
println("Part 1: active count = $(sum(runall(3)))")

# Part 2
println("Part 2: active count = $(sum(runall(4)))")

end