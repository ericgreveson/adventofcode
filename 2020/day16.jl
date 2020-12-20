module day16

# Part 1
parserange(r) = parse.(Int32, split(r, "-")) |> x -> range(first(x); stop=last(x))
parserule(rule) = match(r"(.+):\s(.+)\sor\s(.+)", rule).captures |> x -> (x[1], parserange(x[2]), parserange(x[3]))
rules, ticket, nearby = split.(strip.(split(read("day16_input.txt", String), "\n\n")), "\n")
rules = parserule.(rules)
ticket = parse.(Int32, split(last(ticket), ","))
nearby = map(x -> parse.(Int32, x), split.(nearby[2:end], ","))
valid(rule, v) = v in rule[2] || v in rule[3]
errorrate(v) = any(map(r -> valid(r, v), rules)) ? 0 : v
println("Part 1: error rate = $(sum(errorrate.(vcat(nearby...))))")

# Part 2
candidates(rule, ticket) = [i for (i, v) in enumerate(ticket) if valid(rule, v)]
decodefield(rule, tickets) = intersect(map(t -> Set(candidates(rule, t)), tickets)...)
remaining = filter(t -> sum(errorrate.(t)) == 0, nearby)
function decodefields(rules, tickets)
    fieldsets = Dict(rule[1] => decodefield(rule, tickets) for rule in rules)
    while maximum(length.(values(fieldsets))) > 1
        known = Set(only.(filter(v -> length(v) == 1, collect(values(fieldsets)))))
        fieldsets = Dict(k => length(v) == 1 ? v : setdiff(v, known) for (k, v) in fieldsets)
    end
    Dict(k => only(v) for (k, v) in fieldsets)
end
fieldindex = decodefields(rules, remaining)
deprules(rules) = filter(rule -> startswith(rule[1], "departure"), rules)
println("Part 2: result = $(prod([ticket[fieldindex[rule[1]]] for rule in deprules(rules)]))")

end