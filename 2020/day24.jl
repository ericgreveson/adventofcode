module day24

dirs = Dict("e" => :e, "se" => :se, "sw" => :sw, "w" => :w, "ne" => :ne, "nw" => :nw)
offsets = Dict(:e => (2, 0), :se => (1, 1), :sw => (-1, 1), :w => (-2, 0), :ne => (1, -1), :nw => (-1, -1))

function parseline(line)
    result = []
    while length(line) > 0
        for dir in keys(dirs)
            if startswith(line, dir)
                push!(result, dirs[dir])
                line = line[length(dir)+1:end]
                break
            end
        end
    end
    result
end

function indextocoord(index)
    coord = CartesianIndex(0, 0)
    for i in index
        coord += CartesianIndex(offsets[i]...)
    end
    coord
end

function fliptile!(tiles, index)
    coord = indextocoord(index)
    if coord ∈ keys(tiles)
        tiles[coord] = !tiles[coord]
    else
        tiles[coord] = true
    end
end

input = parseline.(readlines("day24_input.txt"))
tiles = Dict()
map(i -> fliptile!(tiles, i), input)
println("Part 1: black = $(count(values(tiles)))")

# Part 2
adjacent(coord) = [coord + CartesianIndex(o) for o in values(offsets)]

function runstep!(tiles)
    candidates = Set(keys(tiles))
    for (k, v) in tiles
        if v
            union!(candidates, Set(adjacent(k)))
        end
    end
    oldtiles = copy(tiles)
    for c in candidates
        nblack = count([oldtiles[n] for n in adjacent(c) if n ∈ keys(oldtiles)])
        if c ∈ keys(oldtiles) && oldtiles[c]
            if nblack == 0 || nblack > 2 tiles[c] = false end
        else
            if nblack == 2 tiles[c] = true end
        end
    end
end

[runstep!(tiles) for i in 1:100]
println("Part 2: black = $(count(values(tiles)))")

end