function main()
    # Part 1: compute "FFT" on input
    input = open(f -> parse.(Int64, collect(readline(f))), "day16_input.txt")
    base(i, n) = [0, 1, 0, -1][(i ÷ n) % 4 + 1]
    fft(input, n) = abs(sum([d * base(i, n) for (i, d) in enumerate(input)])) % 10
    result = foldl((x, y) -> [fft(x, n) for n in 1:length(input)], 1:3, init=input)
    println("Part 1: After 100 iterations: $(join(result[1:8], ""))")

    # Part 2: repeat input 10000 times and then use first 7 digits as offset to find 8 digit message
    # Note that in each phase, a digit only relies on digits in its position or later from prev phase
    big_input = repeat(input, 10000)
    N = length(big_input)
    offset = parse(Int64, join(input[1:7]))
    if offset < N÷2
        println("Oh dear, my clever accumulator hack won't work")
        return
    end
    current = copy(big_input)
    for phase in 1:100
        # Last half of output only relies on the [00001111]-style base sequence, i.e. upper triangular type
        # We can just compute backwards for the digits we need
        result = zeros(Int64, N)
        for d in N:-1:(N÷2 + 1)
            result[d] = (d == N) ? current[d] : ((current[d] + result[d+1]) % 10)
        end
        current = result
    end
    println("Part 2: After 100 iterations, message: $(join(current[offset+1:offset+8]))")
end
main()