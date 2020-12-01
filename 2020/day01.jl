using Combinatorics

# Part 1
# Load input
expenses = open("day01_input.txt") do f
    [parse(Int32, line) for line in eachline(f)]
end

# See which pair sum to 2020 and multiply them
for (value1, value2) in combinations(expenses, 2)
    if value1 + value2 == 2020
        println("Product of $value1 and $value2: $(value1 * value2)")
    end
end

# Part 2: which triplet satisfy these criteria?
for values in combinations(expenses, 3)
    if sum(values) == 2020
        println("Product of $values: $(prod(values))")
    end
end