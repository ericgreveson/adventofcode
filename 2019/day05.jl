include("intcode.jl")

# Part 1: run the TEST program with input 1
prog = open(f -> parse.(Int32, split(readline(f), ",")), "day05_input.txt")
println.(run_intcode!(copy(prog), [1]))

# Part 2: run the TEST program with input 5
println.(run_intcode!(copy(prog), [5]))
