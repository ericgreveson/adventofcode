# Part 1
layout = Array{Int8}(hcat(map(line -> 'L' .== collect(line), readlines("day11_input.txt"))...)')

function singlestep(current)
    updated = copy(current)
    region = CartesianIndices(current)
    ifirst, ilast = first(region), last(region)
    iunit = oneunit(ifirst)
    for i in region
        neighbours = [current[j] for j in max(ifirst, i - iunit):min(ilast, i + iunit) if j != i]
        if (current[i] == 1 && count(neighbours .== 2) == 0) updated[i] = 2 end
        if (current[i] == 2 && count(neighbours .== 2) >= 4) updated[i] = 1 end
    end
    updated
end

function steadystate(func, current)
    previous = zeros(size(current))
    while current != previous
        previous, current = current, func(current)
    end
    current
end

println("Part 1: occupied count = $(count(steadystate(singlestep, layout) .== 2))")

# Part 2
function singlestep2(current)
    updated = copy(current)
    region = CartesianIndices(current)
    iunit = oneunit(first(region))
    for i in region
        neighbours = []
        for direction in -iunit:iunit
            if !iszero(direction)
                j = i + direction
                while j in region
                    if current[j] != 0
                        push!(neighbours, current[j])
                        break
                    end
                    j += direction
                end
            end
        end
        if (current[i] == 1 && count(neighbours .== 2) == 0) updated[i] = 2 end
        if (current[i] == 2 && count(neighbours .== 2) >= 5) updated[i] = 1 end
    end
    updated
end

println("Part 2: occupied count = $(count(steadystate(singlestep2, layout) .== 2)) ")