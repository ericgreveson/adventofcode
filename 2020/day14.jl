# Part 1
program = readlines("day14_input.txt")
getval(line) = last(split(line, " = "))
getmemloc(line) = parse(Int64, first(split(line, " = "))[5:end-1])
applymask(mask, val) = parse(Int64, join([m == 'X' ? v : m for (m, v) in zip(mask, bitstring(val)[end-35:end])]), base=2)

function run(prog)
    mask = repeat("0", 36)
    mem = Dict()
    for line in prog
        if startswith(line, "mask")
            mask = getval(line)
        else
            mem[getmemloc(line)] = applymask(mask, parse(Int64, getval(line)))
        end
    end
    mem
end
println("Part 1: sum = $(sum(values(run(program))))")

# Part 2
function masklocs(mask, loc)
    idx = 1
    locformat = ""
    for (m, v) in zip(mask, bitstring(loc)[end-35:end])
        if m == 'X'
            locformat *= "[$idx]"
            idx += 1
        elseif m == '1'
            locformat *= '1'
        else
            locformat *= v
        end
    end

    if idx == 1 return [parse(Int64, locformat, base=2)] end
    xcount = idx - 1

    locs = []
    for i in 0:2^xcount-1
        replaced = locformat
        for (j, x) in enumerate(collect(bitstring(i)[end-(xcount-1):end]))
            replaced = replace(replaced, "[$j]" => "$x")
        end
        push!(locs, replaced)
    end
    locs
end

function run2(prog)
    mask = repeat("0", 36)
    mem = Dict()
    for line in prog
        if startswith(line, "mask")
            mask = getval(line)
        else
            loc = getmemloc(line)
            for ml in masklocs(mask, loc)
                mem[ml] = parse(Int64, getval(line))
            end
        end
    end
    mem
end
println("Part 2: sum = $(sum(values(run2(program))))")