include("intcode.jl")

# Part 1: count number of blocks drawn
prog = open(f -> parse.(Int64, split(readline(f), ",")), "day13_input.txt")
command_triples = reshape(run_intcode!(copy(prog), []), 3, :)'
drawn_tiles = Dict((row[1], row[2]) => row[3] for row in eachrow(command_triples))
println("Number of blocks: $(length(filter(isequal(2), collect(values(drawn_tiles)))))")

# Part 2: fake the payment and play the game!
function render(tiles)
    cols = maximum(first.(keys(tiles))) + 1
    rows = maximum(last.(keys(tiles))) + 1
    screen = zeros(Int32, rows, cols)
    for (coord, val) in tiles
        screen[last(coord) + 1, first(coord) + 1] = val
    end
    return [join(getindex.(Ref(Dict(0 => ' ', 1 => 'X', 2 => '█', 3 => '-', 4 => 'o')), row)) for row in eachrow(screen)]
end

prog[1] = 2
input = Channel(1)
output = Channel(30000)
drawn_tiles = Dict((0, 0) => 0)
@async begin
    run_intcode!(copy(prog), input, output)
    close(input)
    close(output)
end

# Screen renderer / input bot
try
    ball_x = 0
    paddle_x = 0
    score = 0
    while true
        put!(input, cmp(ball_x, paddle_x))
        yield()
        while isready(output)
            cmd = copy([take!(output) for i in 1:3])
            if cmd[1] == -1 && cmd[2] == 0
                score = cmd[3]
            else
                drawn_tiles[(cmd[1], cmd[2])] = cmd[3]
                if cmd[3] == 3
                    paddle_x = cmd[1]
                end
                if cmd[3] == 4 ball_x = cmd[1] end
            end
        end
        println.(["Score: $score, BX: $ball_x, PX: $paddle_x"; render(drawn_tiles); ""])
    end
catch InvalidStateException
end