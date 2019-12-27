deal_new(deck) = reverse(deck)
cut(deck, i) = (i < 0) ? [deck[end+i+1:end]; deck[1:end+i]] : [deck[i+1:end]; deck[1:i]]
function deal_inc(deck, increment)
    result = copy(deck)
    for i in 1:length(deck)
        result[((i-1)*increment % length(deck)) + 1] = deck[i]
    end
    return result
end

"""Parse an operation, returning a function that implements the required technique"""
function parse_operation(str)
    if str == "deal into new stack"
        return deal_new
    elseif startswith(str, "cut")
        return (x -> cut(x, parse(Int32, split(str)[end])))
    elseif startswith(str, "deal with increment")
        return (x -> deal_inc(x, parse(Int32, split(str)[end])))
    end
end

# Part 1: Apply all of the operations as described in the input file
operations = parse_operation.(open(f -> readlines(f), "day22_input.txt"))
deck = foldl((x, op) -> op(x), operations, init=collect(0:10006))
println("Card 2019 is at position $(indexin(2019, deck)[1] - 1)")

# Part 2: massive number of cards, shuffled a massive number of times
cards = 119315717514047
shuffle_repeats = 101741582076661
# We need to figure out which card ends up in position 2020