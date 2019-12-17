module AdventOfCode

using Combinatorics
mutable struct Moon pos; vel end

gravity!(m1::Moon, m2::Moon) = (dv = (m1.pos .< m2.pos) - (m1.pos .> m2.pos); m1.vel += dv; m2.vel -= dv)
gravity!(moons) = map(ms -> gravity!(ms...), combinations(moons, 2))
velocity!(m::Moon) = m.pos += m.vel
energy(m::Moon) = sum(abs.(m.pos)) * sum(abs.(m.vel))

# Part 1: compute total energy after 1000 simulation steps
initial_moons() = [
    Moon([-7 -8 9], [0 0 0]),
    Moon([-12 -3 -4], [0 0 0]),
    Moon([6 -17 -9], [0 0 0]),
    Moon([4 -10 -6], [0 0 0])
]
jupiter_moons = initial_moons()
for step in 1:1000
    gravity!(jupiter_moons)
    velocity!.(jupiter_moons)
end
println("Total energy: $(sum(energy.(jupiter_moons)))")

# Part 2: find how long it takes before first repeated step
# Approach: x, y and z dimension equations are independent, maybe each one has a shorter period?
dim_history = [Dict() Dict() Dict()]
cycle_ends = Array{Any}([nothing nothing nothing])
jupiter_moons = initial_moons()
for step in 0:10000000
    gravity!(jupiter_moons)
    velocity!.(jupiter_moons)
    for dim in 1:3
        dim_state = map(m -> (m.pos[dim], m.vel[dim]), jupiter_moons)
        if isnothing(cycle_ends[dim])
            if dim_state ∈ keys(dim_history[dim])
                cycle_ends[dim] = (dim_history[dim][dim_state], step)
            else
                dim_history[dim][dim_state] = step
            end
        end
    end
    if !any(isnothing.(cycle_ends)) break end
end

if all(0 .== first.(cycle_ends))
    period = lcm(last.(cycle_ends)...)
    println("Loop start/end: $cycle_ends, repeat period: $period")
else
    println("Ugh, the maths is harder, I have to think more to implement this")
end

end