module day23

using LinkedLists

wrap(i, len) = i == 0 ? len : i

function playcups(cups, iterations)
    len = length(cups)
    circle = LinkedList{Int}()
    append!(circle, cups)
    lookups = repeat([lastindex(circle)], len)
    for index in keys(circle)
        lookups[getindex(circle, index)] = index
    end

    for i in 1:iterations
        # Put current back at the end of the list
        currentlabel = popfirst!(circle)
        push!(circle, currentlabel)
        lookups[currentlabel] = lastindex(circle)
        # Remove next three
        removed = [popfirst!(circle) for i in 1:3]
        # Find destination
        destlabel = wrap(currentlabel - 1, len)
        while destlabel ∈ removed destlabel = wrap(destlabel - 1, len) end
        destindex = lookups[destlabel]
        # Replace three removed after dest
        for r in removed
            destindex = last(iterate(circle, destindex))
            destindex = insert!(circle, destindex, r)
            lookups[r] = destindex
        end
    end
    cups = [i for i in circle]
end

cups = parse.(Int, collect("247819356"))
cups = playcups(cups, 10)
println("Part 1: remaining = $(join(circshift(cups, -(only(indexin(1, cups)) - 1))[2:end]))")

# Part 2
bigcups = collect(1:1000000)
bigcups[1:9] = parse.(Int, collect("247819356"))
bigcups = playcups(bigcups, 10000000)
println("Part 2: score = $(prod(circshift(bigcups, -(only(indexin(1, bigcups)) - 1))[2:3]))")

end