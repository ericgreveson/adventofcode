# Part 1
program = map(i -> [i[1], parse(Int32, i[2])], split.(readlines("day08_input.txt")))

# Execute an instruction in prog, returning next instruction index and acc
function exec_inst(prog, instr, acc)
    instruction = prog[instr]
    handlers = Dict(
        "acc" => (instr, acc, arg) -> (instr + 1, acc + arg),
        "jmp" => (instr, acc, arg) -> (instr + arg, acc),
        "nop" => (instr, acc, arg) -> (instr + 1, acc)
    )
    handlers[instruction[1]](instr, acc, instruction[2])
end

# Execute instructions in prog until an instruction is executed twice
# If loop detected, return acc, false
# If about to exec 1 past the instruction array, return acc, true
function exec_until_loop(prog, acc=0)
    next_instr = 1
    executed = Set()
    while next_instr ∉ executed
        push!(executed, next_instr)
        next_instr, acc = exec_inst(prog, next_instr, acc)
        if next_instr == length(prog) + 1 return acc, true end
    end
    acc, false
end

println("Part 1: accumulator=$(first(exec_until_loop(program)))")

# Part 2
# Patch each instruction in the program (swapping jmp <-> nop) until it exits normally
function try_patches(prog)
    for i in 1:length(prog)
        patched = deepcopy(prog)
        patched[i][1] = patched[i][1] |> x -> (x == "jmp" ? "nop" : (x == "nop" ? "jmp" : x))
        acc, good = exec_until_loop(patched)
        if good return acc end
    end
end

println("Part 2: accumulator=$(try_patches(program))")
