# Part 1 - parse passports
answers = split.(split(read("day06_input.txt", String), "\n\n"))
any_count(group) = length(∪(Set.(group)...))
println("Part 1: ∑(counts) = $(sum(any_count.(answers)))")

# Part 2
all_count(group) = length(∩(Set.(group)...))
println("Part 2: ∑(counts) = $(sum(all_count.(answers)))")