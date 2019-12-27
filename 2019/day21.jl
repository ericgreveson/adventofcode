include("intcode.jl")

function execute_and_show(prog, script)
    result = run_intcode!(copy(prog), Int8.(collect(replace(script, "\r" => ""))))
    if result[end] <= 127
        println(string(Char.(result)...))
    else
        println("Damage: $(result[end])")
    end
end

function write_script_for_patterns(patterns, final_command)
    # Right-shift each pattern by 1, 2 and 3 steps, as we may need to jump when the pattern starts to appear
    inputs = vcat([map(x -> [repeat([true], i); x[1:end-i]], patterns) for i in 0:3]...)
    # The ground truth of whether it's safe to jump for each of these patterns is in column 4
    # The ground truth of whether it's necessary to jump
    script = ""
    return script * final_command * "\n"
end

# Part 1: write the springscript program iteratively
prog = open(f -> parse.(Int64, split(readline(f), ",")), "day21_input.txt")
# simple description: (!a || (d && (!b || (b && !c)))
script = """
NOT C J
AND B J
NOT B T
OR T J
AND D J
NOT A T
OR T J
WALK
"""
# Patterns we need to cross:
# .### -> jump on .### -> !a
# ..#. -> jump on #..# -> !b && d
# .#.. -> jump on ?#.# -> b && d && !c
execute_and_show(prog, script)

# Part 2: much bigger input sensor range
# Iteratively learn about which patterns we need to cross, auto-writing scripts as we go
function main()
    patterns = []
    loopy = 0
    while true && loopy < 10
        loopy += 1
        script = write_script_for_patterns(patterns, "RUN")
        result = run_intcode!(copy(prog), Int8.(collect(script)))
        if result[end] > 127
            println("Damage: $(result[end])")
            break
        else
            pattern = collect(replace(string(Char.(result)...)[end-13:end-5], "@" => ".")) .== '#'
            append!(patterns, pattern)
        end
    end
end
main()