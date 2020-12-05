# Part 1 - parse passports
passes = open(f -> strip.(readlines(f)), "day05_input.txt")
rownum(pass) = parse(Int32, join([c == 'F' ? '0' : '1' for c in pass[1:7]]), base=2)
colnum(pass) = parse(Int32, join([c == 'L' ? '0' : '1' for c in pass[8:10]]), base=2)
seatids = Set(map(pass -> rownum(pass) * 8 + colnum(pass), passes))
println("Part 1: Highest seat ID is $(max(seatids...))")

# Part 2
println("Part 2: seat ID is $(first([s+1 for s in seatids if (s+1) ∉ seatids && (s+2) ∈ seatids]))")