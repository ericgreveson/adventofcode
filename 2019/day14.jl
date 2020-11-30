using DataStructures: DefaultDict

struct Reagent
    name::String
    quantity::Int64
end

struct Reaction
    inputs::Array{Reagent}
    output::Reagent
end

function parse_reagent(s)::Reagent
    components = split(s, " ")
    return Reagent(last(components), parse(Int32, first(components)))
end

function parse_reaction(s)::Reaction
    components = split(s, " => ")
    return Reaction(parse_reagent.(split(first(components), ", ")), parse_reagent(last(components)))
end

function min_ore_required(outputs, output_name, n, leftover = DefaultDict(0))
    if output_name == "ORE" return n end

    # Use leftovers before making more
    if output_name ∈ keys(leftover)
        if leftover[output_name] >= n
            leftover[output_name] -= n
            return 0
        else
            n -= leftover[output_name]
            leftover[output_name] = 0
        end
    end

    # Produce at least n of the output, putting the rest in leftover dict
    r = outputs[output_name]
    multiplier = Int64(ceil(n / r.output.quantity))
    leftover[r.output.name] += r.output.quantity * multiplier - n
    return sum([min_ore_required(outputs, i.name, i.quantity * multiplier, leftover) for i in r.inputs])
end

"""Return the largest value x in [lower, upper] where f(x) is true, assuming f(lower) and !f(upper)"""
function binary_search(lower, upper, f)
    midpoint = (lower + upper) ÷ 2
    if midpoint == lower return lower end
    return f(midpoint) ? binary_search(midpoint, upper, f) : binary_search(lower, midpoint, f)
end

function main()
    # Part 1: read reaction spec and compute min ore requirement by walking up the tree recursively
    reactions = parse_reaction.(open(f -> readlines(f), "day14_input.txt"))
    outputs = Dict(r.output.name => r for r in reactions)
    ore = min_ore_required(outputs, "FUEL", 1)
    println("Min ore required for 1 FUEL: $ore")

    # Part 2: Fuel available with 1 trillion ore. Quick binary search?
    trillion = 1000000000000
    fuel = binary_search(trillion ÷ ore, 2trillion ÷ ore, x -> (min_ore_required(outputs, "FUEL", x) <= trillion))
    println("Fuel for 1 trillion ore: $fuel")
end
main()