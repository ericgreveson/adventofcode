using Combinatorics

# Part 1
ratings = sort(parse.(Int32, readlines("day10_input.txt")))
diffs = vcat(ratings, [ratings[end]+3]) - vcat([0], ratings)
println("Part 1: product = $(count(x -> x==1, diffs) * count(x -> x==3, diffs))")

# Part 2
valid(chain) = maximum([chain; chain[end]+3] - [chain[1]-3; chain]) <= 3
innercombinations(chain) = combinations(chain[2:(lastindex(chain)-1)])
swapguts(chain, inner) = [first(chain); inner; last(chain)]
arrangements(chain) = count([[valid(swapguts(chain, c)) for c in innercombinations(chain)]; valid(swapguts(chain, []))])
function subchains(chain)
    results = []
    current = [first(chain)]
    for i in 2:lastindex(chain)
        if last(current) + 3 == chain[i]
            push!(results, current)
            current = []
        end
        push!(current, chain[i])
    end
    push!(results, current)
    results
end
println("Part 2: arrangements = $(prod(arrangements.(subchains([0; ratings; ratings[end]+3]))))")
