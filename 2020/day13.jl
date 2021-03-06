# Part 1
data = readlines("day13_input.txt")
earliest = parse(Int64, first(data))
ids = [parse(Int64, id) for id in split(last(data), ",") if id != "x"]
waitingtimes = [ceil(Int, earliest / id) * id - earliest for id in ids]
println("Part 1: answer = $(ids[argmin(waitingtimes)] * minimum(waitingtimes))")

# Part 2 - each id, delta pair fulfils equation t + delta_i = N * id_i
# i.e. (t + delta_i) (mod id_i) = 0
function findt(deltas)
    t = first(deltas)[2]
    modulo = first(deltas)[1]
    for (id, delta) in deltas[2:end]
        while (t + delta) % id != 0 t += modulo end
        modulo = lcm(modulo, id)
    end
    t
end

deltas = [(parse(Int64, id), i-1) for (i, id) in enumerate(split(last(data), ",")) if id != "x"]
println("Part 2: $(findt(deltas))")