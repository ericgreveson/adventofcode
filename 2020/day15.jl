module day15

# Part 1
function playgame(turns)
    numbers = [0,8,15,2,12,1,4]
    numturns = Dict(num => idx for (idx, num) in enumerate(numbers) if idx < lastindex(numbers))
    lastnum = numbers[end]
    for i in (lastindex(numbers)+1):turns
        if lastnum ∈ keys(numturns)
            num = (i - 1) - numturns[lastnum]
        else
            num = 0
        end
        numturns[lastnum] = i - 1
        lastnum = num
    end
    lastnum
end
println("Part 1: 2020th number = $(playgame(2020))")

# Part 2
println("Part 2: 30,000,000th number = $(playgame(30000000))")

end