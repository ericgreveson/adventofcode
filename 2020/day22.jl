module day22


p1, p2 = (x -> (parse.(Int, x[2:26]), parse.(Int, x[29:53])))(readlines("day22_input.txt"))

function playround(a, b)
    ta, tb = popfirst!.([a, b])
    ta > tb ? append!(a, [ta, tb]) : append!(b, [tb, ta])
end

function winningscore(a, b)
    while minimum(length.([a, b])) > 0
        playround(a, b)
    end
    sum(prod.(enumerate(reverse(length(a) == 0 ? b : a))))
end

println("Part 1: score = $(winningscore(copy(p1), copy(p2)))")

# Part 2
function recround(a, b)
    ta, tb = popfirst!.([a, b])
    if length(a) < ta || length(b) < tb
        ta > tb ? append!(a, [ta, tb]) : append!(b, [tb, ta])
        return a, b
    end

    awins = recgame(copy(a[1:ta]), copy(b[1:tb]))
    awins ? append!(a, [ta, tb]) : append!(b, [tb, ta])
    a, b
end

# Return true if a wins, false if b wins
function recgame(a, b)
    roundmem = Set()
    while minimum(length.([a, b])) > 0
        if [a, b] ∈ roundmem return true end
        push!(roundmem, [copy(a), copy(b)])
        a, b = recround(a, b)
    end
    length(a) != 0
end

awins = recgame(p1, p2)
println("Part 2: score = $(sum(prod.(enumerate(reverse(awins ? p1 : p2)))))")

end