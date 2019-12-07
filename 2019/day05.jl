"""Decode an instruction into opcode and parameter modes and return (opcode, [0-padded modes])"""
decode_instruction(instruction::Int32) = (instruction % 100, [digits(instruction ÷ 100); [0, 0]])

"""Define all our intcode operations: each entry is op => (fn, num_params, num_outputs)
   and fn is a function that takes (params, pc, input) and returns (output, new pc)"""
ops = Dict(
    1 => ((params, pc, input) -> (sum(params), pc + 4), 2, 1),                                  # add
    2 => ((params, pc, input) -> (prod(params), pc + 4), 2, 1),                                 # mul
    3 => ((params, pc, input) -> (input, pc + 2), 0, 1),                                        # read input
    4 => ((params, pc, input) -> (println(params[1]), pc + 2), 1, 0),                           # write output
    5 => ((params, pc, input) -> (nothing, params[1] != 0 ? (params[2] + 1) : pc + 3), 2, 0),   # jump if nonzero
    6 => ((params, pc, input) -> (nothing, params[1] == 0 ? (params[2] + 1) : pc + 3), 2, 0),   # jump if zero
    7 => ((params, pc, input) -> (params[1] < params[2] ? 1 : 0, pc + 4), 2, 1),                # less than
    8 => ((params, pc, input) -> (params[1] == params[2] ? 1 : 0, pc + 4), 2, 1)                # equals
)

"""Run an intcode program"""
function run_intcode!(prog, input)
    pc = 1
    while true
        opcode, modes = decode_instruction(prog[pc])
        if opcode == 99 break end
        op_func, num_params, num_outputs = ops[opcode]
        params = [modes[i] == 1 ? prog[pc + i] : prog[prog[pc + i] + 1] for i in 1:num_params]
        output, new_pc = op_func(params, pc, input)
        if num_outputs == 1 prog[prog[pc + num_params + 1] + 1] = output end
        pc = new_pc
    end
end

# Part 1: run the TEST program with input 1
prog = open(f -> parse.(Int32, split(readline(f), ",")), "day05_input.txt")
run_intcode!(copy(prog), 1)

# Part 2: run the TEST program with input 5
run_intcode!(copy(prog), 5)
