# Load input
masses = open("day01_input.txt") do f
    [parse(Int32, line) for line in eachline(f)]
end

# Part 1
fuel_requirement = sum([Int32(floor(mass / 3)) - 2 for mass in masses])
println("Part 1: Fuel requirement: $fuel_requirement")

# Part 2
function compute_mass_recursive(fuel_mass::Int32)::Int32
    extra_fuel_mass = Int32(floor(fuel_mass / 3)) - 2
    if extra_fuel_mass <= 0
        return fuel_mass
    else
        return fuel_mass + compute_mass_recursive(extra_fuel_mass)
    end
end

fuel_requirement = sum([compute_mass_recursive(mass) - mass for mass in masses])
println("Part 2: Fuel requirement: $fuel_requirement")
