using DataStructures

"""Intcode machine state"""
mutable struct IntcodeState
    pc::Int64
    input::Channel
    output::Channel
    relative_base::Int64
end

"""Decode an instruction into opcode and parameter modes and return (opcode, [0-padded modes])"""
decode_instruction(instruction) = (instruction % 100, [digits(instruction ÷ 100); [0, 0]])

"""Define all our intcode operations: each entry is op => (fn, num_params, num_results)
   and fn is a function that takes (params, state) and returns result"""
ops = Dict(
    1 => ((p, state::IntcodeState) -> (state.pc += 4; sum(p)), 2, 1),                                       # add
    2 => ((p, state::IntcodeState) -> (state.pc += 4; prod(p)), 2, 1),                                      # mul
    3 => ((p, state::IntcodeState) -> (state.pc += 2; take!(state.input)), 0, 1),                           # read input
    4 => ((p, state::IntcodeState) -> (state.pc += 2; put!(state.output, p[1])), 1, 0),                     # write output
    5 => ((p, state::IntcodeState) -> (state.pc = p[1] != 0 ? (p[2] + 1) : state.pc + 3; nothing), 2, 0),   # jump if nonzero
    6 => ((p, state::IntcodeState) -> (state.pc = p[1] == 0 ? (p[2] + 1) : state.pc + 3; nothing), 2, 0),   # jump if zero
    7 => ((p, state::IntcodeState) -> (state.pc += 4; p[1] < p[2] ? 1 : 0), 2, 1),                          # less than
    8 => ((p, state::IntcodeState) -> (state.pc += 4; p[1] == p[2] ? 1 : 0), 2, 1),                         # equals
    9 => ((p, state::IntcodeState) -> (state.pc += 2; state.relative_base += p[1]), 1, 0),                  # adjust relative base
    99 => ((p, state::IntcodeState) -> (state.pc += 1), 0, 0)                                               # exit
)

"""Read a param using the appropriate mode"""
function read_param(prog, state, mode, i)
    if mode == 0
        # Position mode: take the argument and read the according (1-indexed) address
        prog[prog[state.pc + i] + 1]
    elseif mode == 1
        # Immediate mode: take the argument as is
        prog[state.pc + i]
    elseif mode == 2
        # Relative mode: position mode plus the relative base (already 1-indexed)
        prog[prog[state.pc + i] + state.relative_base]
    end
end

"""Write a result using the appropriate mode and previous program counter"""
function write_result(prog, state, mode, i, result)
    if mode == 0
        # Position mode: store in the appropriate 1-indexed address
        prog[prog[i] + 1] = result
    elseif mode == 2
        # Relative mode: position mode plus the relative base
        prog[prog[i] + state.relative_base] = result
    end
end

"""Run an intcode program prog, with input read from input channel, writing to output channel"""
function run_intcode!(prog, input::Channel, output::Channel)
    # "Large memory" support: turn prog into a defaultdict so we can write to any old "address"
    dprog = DefaultDict(0, Dict(i => val for (i, val) in enumerate(prog)))
    state = IntcodeState(1, input, output, 1)
    while true
        opcode, modes = decode_instruction(dprog[state.pc])
        if opcode == 99 break end
        op_func, num_params, num_results = ops[opcode]
        params = [read_param(dprog, state, modes[i], i) for i in 1:num_params]
        old_pc = state.pc
        result = op_func(params, state)
        if num_results == 1 write_result(dprog, state, modes[num_params + 1], old_pc + num_params + 1, result) end
    end
end

"""Simple wrapper for running prog with input array and returning output as array"""
function run_intcode!(prog, input_array::Array)::Array
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

"""Give a human-friendly disassembly of the program"""
function disassemble(prog)::Array{String,1}
    pc = 1
    asm = Dict(
        1 => "ADD  ",
        2 => "MUL  ",
        3 => "READ ",
        4 => "WRITE",
        5 => "JMPNZ",
        6 => "JMPZ ",
        7 => "LESS ",
        8 => "EQUAL",
        9 => "ADJRB",
        99 => "EXIT "
    )

    disassembled = Array{String,1}()
    data_segment = false
    while pc <= length(prog)
        opcode, modes = decode_instruction(prog[pc])
        num_params, num_results = 0, 0
        if opcode ∈ keys(ops)
            op_func, num_params, num_results = ops[opcode]
        else
            data_segment = true
        end
        
        if data_segment
            push!(disassembled, "DATA($opcode)")
            pc += 1
            continue
        end

        cmd = "$(asm[opcode])"
        for i in 1:num_params
            param = prog[pc + i]
            if modes[i] == 0
                cmd *= " LOAD($param)"
            elseif modes[i] == 1
                cmd *= " $param"
            elseif modes[i] == 2
                cmd *= " LOADREL($param)"
            end
        end
        for i in 1:num_results
            param = prog[pc + i + num_params]
            if modes[i] == 0
                cmd *= " STORE($param)"
            elseif modes[i] == 2
                cmd *= " STOREREL($param)"
            end
        end
        push!(disassembled, cmd)
        pc += num_params + num_results + 1
    end
    return disassembled
end