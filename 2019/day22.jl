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

"""Parse an operation, returning (α, β) for the equation of the form αk + β mod N"""
function parse_operation_αβ(str)
    if str == "deal into new stack"
        return (-1, -1)
    elseif startswith(str, "cut")
        return (1, -parse(Int32, split(str)[end]))
    elseif startswith(str, "deal with increment")
        return (parse(Int32, split(str)[end]), 0)
    end
end

"""Compute repeated product Π(αk + β) m times, via power of two repeated multiplication"""
function fast_multiply_mod(α, β, m, N)
    result = (1, 0)
    power_two = (α, β)
    while m > 0
        if m & 1 == 1
            result = (mod(power_two[1] * result[1], N), mod(power_two[1] * result[2] + power_two[2], N))
        end
        m >>= 1
        power_two = (mod(power_two[1] * power_two[1], N), mod(power_two[1]*power_two[2] + power_two[2], N))
    end
    return result
end

function main()
    # Part 1: Apply all of the operations as described in the input file
    operations = parse_operation.(open(f -> readlines(f), "day22_input.txt"))
    deck = foldl((x, op) -> op(x), operations, init=collect(0:10006))
    println("Part 1: Card 2019 is at position $(indexin(2019, deck)[1] - 1)")

    # Part 2: massive number of cards, shuffled a massive number of times
    N = Int128(119315717514047)
    shuffle_repeats = Int128(101741582076661)
    # We need to figure out which card ends up in position 2020
    # What do the operations do to card k?
    # Deal into new stack:
    #   Forward:  D(C_k) = C_(N-1-k) for k ∈ 0:N-1
    # or alternatively
    #   Forward:  D(C_k) = C_(-k-1 mod N)
    # Cut:
    #   Forward:  U(C_k, c) = C_((k-c) mod N)
    # Deal with increment:
    #   Forward:  I(C_k, i) = C_(k*i mod N)
    #
    operations = parse_operation_αβ.(open(f -> readlines(f), "day22_input.txt"))
    α, β = foldl((x, op) -> (mod(x[1]*op[1], N), mod(x[2]*op[1] + op[2], N)), operations, init=(1, 0))
    # The shuffle repeats complicate things! After one round, k -> (αk + β) mod N.
    # After two rounds we have k -> (α^2k + αβ + β) mod N, etc
    # We need to compute the bit pattern of shuffle_repeats and apply it via power of two exponentiation
    α, β = fast_multiply_mod(α, β, shuffle_repeats, N)
    # Now we need to find the number on the card in position 2020. We have the sum:
    # (αk + β) mod N = 2020
    # To solve for k, we can say (αk) mod N = (2020 - β) mod N
    # So we need to solve linear Diophantine equation αk + Ny = (2020 - β) mod N.
    # Use extended Euclidean algorithm which solves related equation αu + Nv = gcd(α, N).
    d, u, v = gcdx(α, N)
    final = 2020
    k = mod(u * mod(final - β, N) ÷ d, N)
    println("Part 2: Card in pos $final has number $k on.")
end
main()