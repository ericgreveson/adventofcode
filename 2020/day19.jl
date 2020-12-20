module day19

using Combinatorics

function parserule(r)
    id, spec = split(r, ": ")
    id = parse(Int32, id)
    if spec[1] == '"'
        return id => (:matchchar, spec[2])
    else
        subrules = map(x -> parse.(Int32, split(x, " ")), split(spec, " | "))
        return id => (:matchrules, subrules)
    end
end

# Try to match string s[offset:end] with a specific sub-option sequential rule list, return set of remainder offsets
function matchoption(rules, subrules, s; offset)
    offsets = Set(offset)
    for subrule in subrules
        matchsets = [match(rules, subrule, s; offset=o) for o in offsets if o <= lastindex(s)]
        if isempty(matchsets) return Set() end
        offsets = union(matchsets...)
    end
    offsets
end

# Try to match string s[offset:end] with rule ruleidx, return a set of possible remainder offsets
function match(rules, ruleidx, s; offset=1)
    if offset > lastindex(s) return Set() end
    ruletype, data = rules[ruleidx]
    if ruletype == :matchrules
        return union([matchoption(rules, ruleoption, s; offset) for ruleoption in data]...)
    elseif ruletype == :matchchar
        return s[offset] == data ? Set(offset + 1) : Set()
    end
end

rules, messages = split(read("day19_input.txt", String), "\n\n")
rules = Dict(parserule.(split(rules, "\n")))
messages = split(strip(messages), "\n")
println("Part 1: valid = $(count(map(m -> (lastindex(m) + 1) ∈ match(rules, 0, m), messages)))")

# Part 2
for r in ["8: 42 | 42 8", "11: 42 31 | 42 11 31"]
    parsed = parserule(r)
    rules[first(parsed)] = last(parsed)
end
println("Part 2: valid = $(count(map(m -> (lastindex(m) + 1) ∈ match(rules, 0, m), messages)))")

end