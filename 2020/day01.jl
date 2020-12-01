# Part 1
# Load input
expenses = open("day01_input.txt") do f
    [parse(Int32, line) for line in eachline(f)]
end

# See which pair sum to 2020 and multiply them
for (index, value1) in enumerate(expenses)
    for value2 in expenses[index+1:end]
        if value1 + value2 == 2020
            println("Product of $value1 and $value2: $(value1 * value2)")
        end
    end
end

# Part 2: which triplet satisfy these criteria?
for (index1, value1) in enumerate(expenses)
    for (index2, value2) in enumerate(expenses[index1+1:end])
        for value3 in expenses[index1+index2+1:end]
            if value1 + value2 + value3 == 2020
                println("Product of $value1, $value2 and $value3: $(value1 * value2 * value3)")
            end
        end
    end
end