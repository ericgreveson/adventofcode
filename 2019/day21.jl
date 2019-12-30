include("intcode.jl")

function execute_and_show(prog, script)
    result = run_intcode!(copy(prog), Int8.(collect(replace(script, "\r" => ""))))
    if result[end] <= 127
        println(string(Char.(result)...))
    else
        println("Damage: $(result[end])")
    end
end

# Part 1: write the springscript program iteratively
prog = open(f -> parse.(Int64, split(readline(f), ",")), "day21_input.txt")
# simple description: (!a || (d && (!b || (b && !c)))
script = """NOT C J
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
#execute_and_show(prog, script)

# Part 2: much bigger input sensor range
# Again iteratively learn about which patterns we need to cross, writing scripts as we go
#
# ABCDEFGHI
# 011111111 -> jump on 011111111 -> !a
# 001011111 -> jump on 100101111 -> !b && d
# 010011111 -> jump on 110100111 -> b && !c && d && h
# 010100010 -> jump on 010100010 -> !a
#              DO NOT jump on 1101010000 -> modified rule for third option above
# 010001001 -> jump on 110100010 -> modified rule for third option above again
#
# simple description: (!a || (d && (!b || (b && !c && g)))
script = """NOT C J
AND B J
AND H J
NOT B T
OR T J
AND D J
NOT A T
OR T J
RUN
"""
execute_and_show(prog, script)