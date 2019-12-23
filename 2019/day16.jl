# Part 1: compute "FFT" on input
input = open(f -> parse.(Int64, collect(readline(f))), "day16_input.txt")
base(i, n) = [0, 1, 0, -1][(i ÷ n) % 4 + 1]
fft(input, n) = abs(sum([d * base(i, n) for (i, d) in enumerate(input)])) % 10
result = foldl((x, y) -> [fft(x, n) for n in 1:length(input)], 1:3, init=input)
println("After 100 iterations: $(join(result[1:8], ""))")

# Part 2: repeat input 10000 times and then use first 7 digits as offset to find 8 digit message
println("TODO!")