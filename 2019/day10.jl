function visible_asteroids_at_coord(grid, coord)
    # Search outwards in "shells" from coord
    remaining = copy(grid)
    for r in 1:maximum(size(grid))
        shell = map(x -> coord + x, setdiff(CartesianIndices((-r:r, -r:r)), CartesianIndices((-(r-1):(r-1), -(r-1):(r-1)))))
        for i in filter(x -> x ∈ CartesianIndices(remaining) && remaining[x], shell)
            # We can see this asteroid. Find the minimum integer direction vector.
            delta = CartesianIndex(tuple((x -> x .÷ gcd(x))(collect((i - coord).I))...))
            # Delete all occluded locations by stepping along the direction vector
            occluded = i + delta
            while occluded ∈ CartesianIndices(grid)
                remaining[occluded] = false
                occluded += delta
            end
        end
    end
    # Remember to remove the asteroid we're sitting on
    remaining[coord] = false
    return remaining
end

# Part 1: read asteroid map as bool matrix and find out which one can detect most asteroids
grid = hcat(map(line -> '#' .== collect(line), open(f -> readlines(f), "day10_input.txt"))...)'
visible_counts = map(x -> grid[x] ? count(visible_asteroids_at_coord(grid, x)) : 0, CartesianIndices(grid))
println("Max detected asteroids: $(maximum(visible_counts))")

# Part 2: get coord of best station, then work out which is the 200th asteroid to be vaporized
# We actually have >200 detected, so we need less than one rotation. Sort detected by angle.
coord = argmax(visible_counts)
detected = visible_asteroids_at_coord(grid, coord)
item = sort(map(x -> (π - atan(reverse((x - coord).I)...), x), filter(x -> detected[x], CartesianIndices(detected))))[200]
println("200th to be vaporized: $item, checksum: $((item[2][2] - 1) * 100 + item[2][1] - 1))")