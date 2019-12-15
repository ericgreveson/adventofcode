# Part 1: run BOOST program in diagnostic mode
include("intcode.jl")
prog = open(f -> parse.(Int64, split(readline(f), ",")), "day09_input.txt")
println.(run_intcode!(copy(prog), [1]))

# Part 2: run BOOST program in boost mode
println.(run_intcode!(copy(prog), [2]))
