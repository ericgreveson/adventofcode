"""
Run an intcode program: 1 adds, 2 multiplies, 99 halts
prog: the program to run as an array of integers, will be modified in place
"""
function run_intcode!(prog)
    pc = 1
    while prog[pc] != 99
        # Remember to add 1 for Julia 1-based indices!
        arg1_index = prog[pc+1] + 1
        arg2_index = prog[pc+2] + 1
        res_index = prog[pc+3] + 1
        if prog[pc] == 1
            # 1 means add
            prog[res_index] = prog[arg1_index] + prog[arg2_index]
        elseif prog[pc] == 2
            # 2 means mul
            prog[res_index] = prog[arg1_index] * prog[arg2_index]
        end
        pc += 4
    end
end

# Part 1: load input and patch it, then say what was in first element after running
program = open(f -> parse.(Int32, split(readline(f), ',')), "day02_input.txt")
patched = copy(program)
patched[2] = 12
patched[3] = 2
run_intcode!(patched)
println("First element: $(patched[1])")

# Part 2: do a stupid grid search to find "noun" and "verb"
for noun in 0:99, verb in 0:99
    test = copy(program)
    test[2] = noun
    test[3] = verb
    run_intcode!(test)
    if test[1] == 19690720
        # This is the one!
        println("Noun=$noun, verb=$verb, 100*noun+verb=$(100*noun + verb)")
    end
end
