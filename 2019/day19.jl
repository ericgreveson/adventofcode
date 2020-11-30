include("intcode.jl")

# Part 1: run the intcode program on all points in the 50x50 starting grid and count 1's
prog = open(f -> parse.(Int64, split(readline(f), ",")), "day19_input.txt")
result = map(x -> run_intcode!(copy(prog), [x[1], x[2]])[1], CartesianIndices((0:49, 0:49)))
println("Number of on pixels: $(sum(result))")

# Part 2: find top left coord of part of beam covering 100x100 area. Estimate first and last y as fn of x
approx_start_factor = 38/50
approx_end_factor = 49/50
test_point(prog, x, y) = run_intcode!(copy(prog), [x, y])[1]
function find_exact_start_end(prog, x)
    ys = Int32(floor(x * approx_start_factor)) - 1
    while test_point(prog, x, ys) == 0 ys += 1 end
    ye = Int32(ceil(x * approx_end_factor)) + 1
    while test_point(prog, x, ye) == 0 ye -= 1 end
    return ys, ye
end
# Look for the first coordinate which can fit a 100x100 square in
for x in 700:1200
    ys1, ye1 = find_exact_start_end(prog, x)
    ys2, ye2 = find_exact_start_end(prog, x + 99)
    if ye1 - ys2 >= 99
        println("First coord for square: ($x, $ys2). Code: $(x * 10000 + ys2)")
        break
    end
end