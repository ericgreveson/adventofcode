using Combinatorics

# Part 1
data = parse.(Int64, readlines("day09_input.txt"))
valid = [d ∈ Set(sum.(combinations(data[i-25:i-1], 2))) for (i, d) in enumerate(data) if i > 25]
target = data[argmin(valid)+25]
println("Part 1: first invalid = $target")

# Part 2
function find_weakness(data, target)
    for start in 1:lastindex(data)
        total = data[start]
        for finish in (start+1):lastindex(data)
            total += data[finish]
            if total == target return minimum(data[start:finish]) + maximum(data[start:finish]) end
            if total > target break end
        end
    end
end
println("Part 2: weakness = $(find_weakness(data, target))")