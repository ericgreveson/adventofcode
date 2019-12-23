include("intcode.jl")

# Part 1: compute sum of x*y for all intersections
prog = open(f -> parse.(Int64, split(readline(f), ",")), "day17_input.txt")
image = split(string(Char.(run_intcode!(copy(prog), []))...))
scaffold = hcat([[val == '#' for (c, val) in enumerate(collect(line))] for (r, line) in enumerate(image)]...)'
directions = CartesianIndex.([(0, 0), (-1, 0), (0, 1), (1, 0), (0, -1)])
isect = map(x -> all([(d + x) ∈ CartesianIndices(scaffold) && scaffold[d + x] for d in directions]), CartesianIndices(scaffold))
isect_coords = [x for x in CartesianIndices(isect) if isect[x]]
println("Sum of intersection coord products: $(sum([(c[1]-1) * (c[2]-1) for c in isect_coords]))")

# Part 2: control the vacuum robot! Dump the image to screen and manually figure out a program
println.(image)
# Ok, from inspection, uncompressed we need:
# [L,4,L,4,L,6,R,10,L,6,L,4,L,4,L,6,R,10,L,6,L,12,L,6,R,10,L,6,R,8,R,10,L,6,R,8,R,10,L,6,
# L,4,L,4,L,6,R,10,L,6,R,8,R,10,L,6,L,12,L,6,R,10,L,6,R,8,R,10,L,6,L,12,L,6,R,10,L,6]
# Looking at patterns, we can get this into 20 bytes in 3 subroutines like:
A = "L,4,L,4,L,6,R,10,L,6\n"
B = "L,12,L,6,R,10,L,6\n"
C = "R,8,R,10,L,6\n"
main_routine = "A,A,B,C,C,A,C,B,C,B\n"
prog[1] = 2
output = run_intcode!(copy(prog), Int8.(collect("$(main_routine)$(A)$(B)$(C)n\n")))
println("Dust: $(last(output))")
