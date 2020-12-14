using Combinatorics

# Part 1
ratings = sort(parse.(Int32, readlines("day10_input.txt")))
diffs = vcat(ratings, [ratings[end]+3]) - vcat([0], ratings)
println("Part 1: product = $(count(x -> x==1, diffs) * count(x -> x==3, diffs))")

# Part 2 - note the diffs are ALL 1 or 3
function minimal(ratings)
    jolts = 0
    remaining = []
    for i in 1:(lastindex(ratings)-1)
        if jolts + 3 < ratings[i+1]
            # We need this rating, next one won't cut it
            jolts = ratings[i]
            push!(remaining, jolts)
        end
    end
    [remaining; ratings[end]]
end
remaining = minimal(ratings)
println("Part 2: arrangements = $(length(ratings) - length(remaining))")
