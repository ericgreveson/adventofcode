module AdventOfCode

using Combinatorics
mutable struct Moon pos; vel end

gravity!(m1::Moon, m2::Moon) = (dv = (m1.pos .< m2.pos) - (m1.pos .> m2.pos); m1.vel += dv; m2.vel -= dv)
gravity!(moons) = map(ms -> gravity!(ms...), combinations(moons, 2))
velocity!(m::Moon) = m.pos += m.vel
energy(m::Moon) = sum(abs.(m.pos)) * sum(abs.(m.vel))

# Part 1: compute total energy after 1000 simulation steps
jupiter_moons = [
    Moon([-7 -8 9], [0 0 0]),
    Moon([-12 -3 -4], [0 0 0]),
    Moon([6 -17 -9], [0 0 0]),
    Moon([4 -10 -6], [0 0 0])
]
for step in 1:1000
    gravity!(jupiter_moons)
    velocity!.(jupiter_moons)
end
println("Total energy: $(sum(energy.(jupiter_moons)))")

# Part 2: find how long it takes before first repeated step
end