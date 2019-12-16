using DataStructures
include("intcode.jl")

"""Paint the hull, putting current tile colour on input and reading output to move robot"""
function paint_hull_io(hull, input, output)
    current_pos = [0 0]
    current_angle = 0
    try
        while true
            #print("First: $(something(hull[current_pos], 0))")
            put!(input, something(hull[current_pos], 0))
            # Paint the hull the appropriate colour based on the first command
            hull[current_pos] = take!(output)
            # Turn the robot the appropriate direction based on the second command
            current_angle = (current_angle + (take!(output) == 0 ? -90 : 90)) % 360
            # Move forward one panel
            current_pos += [Int32(sind(current_angle)) -Int32(cosd(current_angle))]
        end
    catch InvalidStateException end
end

"""Run the hull-painting robot prog on the hull defined as a DefaultDict of coords to colours"""
function paint_hull(hull, prog)
    @sync begin
        input = Channel(2)
        output = Channel(2)
        @async paint_hull_io(hull, input, output)
        @async begin
            run_intcode!(copy(prog), input, output)
            close(input)
            close(output)
        end
    end
end

# Part 1: run the robot and count how many panels it paints
prog = open(f -> parse.(Int64, split(readline(f), ",")), "day11_input.txt")
hull = DefaultDict(nothing)
paint_hull(hull, prog)
println("Number of panels painted: $(length(filter(x -> !isnothing(x), collect(values(hull)))))")

# Part 2: start on a white panel and show the result
hull = DefaultDict(nothing, Dict{Any, Any}([0 0] => 1))
paint_hull(hull, prog)
x_range = (:)(extrema(first.(keys(hull)))...)
y_range = (:)(extrema(last.(keys(hull)))...)
image = zeros(Bool, length(x_range), length(y_range))
for (pos, colour) in hull image[(pos - [first(x_range) first(y_range)] + [1 1])...] = something(colour, 0) end
println.(join.(eachrow(map(x -> x ? "█" : " ", image'))))
