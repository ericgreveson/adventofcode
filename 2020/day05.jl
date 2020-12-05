# Part 1 - parse passports
passes = open(f -> strip.(readlines(f)), "day05_input.txt")
seatids = Set(map(p -> parse(Int32, join([c ∈ ['F', 'L'] ? '0' : '1' for c in p]), base=2), passes))
println("Part 1: Highest seat ID is $(maximum(seatids))")

# Part 2
println("Part 2: seat ID is $(first([s+1 for s in seatids if (s+1) ∉ seatids && (s+2) ∈ seatids]))")