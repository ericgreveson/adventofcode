import Base.parse

# Part 1
struct Policy
    min::Int32
    max::Int32
    char::Char
end

function parse(::Type{Policy}, x)
    min, max, char = split(x, ('-', ' '))
    Policy(parse(Int32, min), parse(Int32, max), only(char))
end

# Load input
parse_line(policy, password) = (parse(Policy, policy), password)
policies_passwords = open("day02_input.txt") do f
    [parse_line(strip.(split(line, ':'))...) for line in eachline(f)]
end

is_valid(policy, password) = policy.min <= count(==(policy.char), password) <= policy.max
println("There are $(sum([is_valid(pp...) for pp in policies_passwords])) valid passwords")


# Part 2
new_is_valid(policy, password) = xor(password[policy.min] == policy.char, password[policy.max] == policy.char)
println("There are now $(sum([new_is_valid(pp...) for pp in policies_passwords])) valid passwords")