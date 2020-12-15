module Day12

# Part 1
instructions = readlines("day12_input.txt")

mutable struct Ship
    pos
    angle
end

function move!(ship::Ship, instruction)
    rules = Dict(
        'N' => (s::Ship, v) -> s.pos += [0, v],
        'S' => (s::Ship, v) -> s.pos -= [0, v],
        'E' => (s::Ship, v) -> s.pos += [v, 0],
        'W' => (s::Ship, v) -> s.pos -= [v, 0],
        'L' => (s::Ship, v) -> s.angle += v,
        'R' => (s::Ship, v) -> s.angle -= v,
        'F' => (s::Ship, v) -> s.pos += v * [round(Int, cosd(s.angle)), round(Int, sind(s.angle))]
    )
    rules[first(instruction)](ship, parse(Int32, instruction[2:end]))
end

ship = Ship([0, 0], 0)
map(i -> move!(ship, i), instructions)
println("Part 1: Manhattan dist = $(sum(abs.(ship.pos)))")

# Part 2
mutable struct Waypoint
    pos
end

function rotationmatrix(angle)
    c = round(Int, cosd(angle))
    s = round(Int, sind(angle))
    [c -s
     s c]
end

function move!(ship::Ship, waypoint::Waypoint, instruction)
    rules = Dict(
        'N' => (s::Ship, w::Waypoint, v) -> w.pos += [0, v],
        'S' => (s::Ship, w::Waypoint, v) -> w.pos -= [0, v],
        'E' => (s::Ship, w::Waypoint, v) -> w.pos += [v, 0],
        'W' => (s::Ship, w::Waypoint, v) -> w.pos -= [v, 0],
        'L' => (s::Ship, w::Waypoint, v) -> w.pos = rotationmatrix(v) * w.pos,
        'R' => (s::Ship, w::Waypoint, v) -> w.pos = rotationmatrix(-v) * w.pos,
        'F' => (s::Ship, w::Waypoint, v) -> s.pos += v * w.pos
    )
    rules[first(instruction)](ship, waypoint, parse(Int32, instruction[2:end]))
end

ship = Ship([0, 0], 0)
waypoint = Waypoint([10, 1])
map(i -> move!(ship, waypoint, i), instructions)
println("Part 2: Manhattan dist = $(sum(abs.(ship.pos)))")

end