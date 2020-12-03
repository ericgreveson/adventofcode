# Part 1
grid = open(f -> readlines(f), "day03_input.txt")
function treecount(grid, right, down)
    pos = [1, 1]
    hits = 0
    while pos[2] <= length(grid)
        row = grid[pos[2]]
        hits += row[(pos[1] - 1) % length(row) + 1] == '#' ? 1 : 0
        pos += [right, down]
    end
    hits
end
println("There are $(treecount(grid, 3, 1)) trees encountered")

# Part 2
slopes = [[1, 1], [3, 1], [5, 1], [7, 1], [1, 2]]
println("Tree product: $(prod([treecount(grid, slope...) for slope in slopes]))")