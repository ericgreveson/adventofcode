"""Decode an instruction into opcode and parameter modes and return (opcode, [0-padded modes])"""
decode_instruction(instruction::Int32) = (instruction % 100, [digits(instruction ÷ 100); [0, 0]])

"""Define all our intcode operations: each entry is op => (fn, num_params, num_results)
   and fn is a function that takes (params, pc, input, output) and returns (result, new pc)"""
ops = Dict(
    1 => ((params, pc, input, output) -> (sum(params), pc + 4), 2, 1),                                  # add
    2 => ((params, pc, input, output) -> (prod(params), pc + 4), 2, 1),                                 # mul
    3 => ((params, pc, input, output) -> (take!(input), pc + 2), 0, 1),                                 # read input
    4 => ((params, pc, input, output) -> (put!(output, params[1]), pc + 2), 1, 0),                      # write output
    5 => ((params, pc, input, output) -> (nothing, params[1] != 0 ? (params[2] + 1) : pc + 3), 2, 0),   # jump if nonzero
    6 => ((params, pc, input, output) -> (nothing, params[1] == 0 ? (params[2] + 1) : pc + 3), 2, 0),   # jump if zero
    7 => ((params, pc, input, output) -> (params[1] < params[2] ? 1 : 0, pc + 4), 2, 1),                # less than
    8 => ((params, pc, input, output) -> (params[1] == params[2] ? 1 : 0, pc + 4), 2, 1)                # equals
)

"""Run an intcode program prog, with input read from input channel, writing to output channel"""
function run_intcode!(prog, input::Channel, output::Channel)
    pc = 1
    while true
        opcode, modes = decode_instruction(prog[pc])
        if opcode == 99 break end
        op_func, num_params, num_results = ops[opcode]
        params = [modes[i] == 1 ? prog[pc + i] : prog[prog[pc + i] + 1] for i in 1:num_params]
        result, new_pc = op_func(params, pc, input, output) # op_func will consume front of input
        if num_results == 1 prog[prog[pc + num_params + 1] + 1] = result end
        pc = new_pc
    end
end

"""Simple wrapper for running prog with input array and returning output as array"""
function run_intcode!(prog, input_array::Array)
    input = Channel(1)
    output = Channel(1)
    output_array = []
    @sync begin
        @async for data in input_array put!(input, data) end
        @async try while true push!(output_array, take!(output)) end catch InvalidStateException end
        @async begin
            run_intcode!(copy(prog), input, output)
            close(input)
            close(output)
        end
    end
    return output_array
end
