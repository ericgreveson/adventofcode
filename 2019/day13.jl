include("intcode.jl")

# Part 1: count number of blocks drawn
prog = open(f -> parse.(Int64, split(readline(f), ",")), "day13_input.txt")
command_triples = reshape(run_intcode!(copy(prog), []), 3, :)'
drawn_tiles = Dict((row[1], row[2]) => row[3] for row in eachrow(command_triples))
println("Number of blocks: $(length(filter(isequal(2), collect(values(drawn_tiles)))))")

# Part 2: fake the payment and play the game!