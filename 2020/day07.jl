# Part 1
parseitem(item) = first(rsplit(item, " "; limit=2)) |> x -> split(x, " "; limit=2)
parsecontents(c) = c[begin:end-1] |> x -> x == "no other bags" ? [] : parseitem.(split(x, ", "))
parserule(rule) = split(rule, " bags contain ") |> r -> r[begin] => parsecontents(r[end])
rules = Dict(parserule.(readlines("day07_input.txt")))
listcontains(list, colour) = (colour ∈ list) || any(map(c -> rulecontains(rules[c], colour), list))
rulecontains(ruleset, colour) = listcontains(map(x -> last(x), ruleset), colour)
println("Part 1: $(sum(rulecontains.(values(rules), "shiny gold"))) bag colours contain ≥1 SGB")

# Part 2
bagcount(colour) = reduce(+, [parse(Int32, first(c)) * bagcount(last(c)) for c in rules[colour]]; init=1)
println("Part 2: SGB contains $(bagcount("shiny gold") - 1) bags")
