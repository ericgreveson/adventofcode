# Part 1: digits never decreasing, has a double digit, is 6 digits long.
has_double_digit(ds) = any([ds[i] == ds[i+1] for i in 1:5])
never_decreasing(ds) = all([ds[i] >= ds[i+1] for i in 1:5])
valid_password(ds) = has_double_digit(ds) && never_decreasing(ds)
passwords = filter(x -> valid_password(digits(x)), 165432:707912)
println("Part 1: Number of possible passwords: $(length(passwords))")

# Part 2: now we need at least one group of 2 adjacent digits to not be part of larger group
has_isolated_double_digit(ds) =
    (ds[1] == ds[2] != ds[3]) ||
    any(ds[i] != ds[i+1] == ds[i+2] != ds[i+3] for i in 1:3) ||
    (ds[4] != ds[5] == ds[6])
passwords = [password for password in passwords if has_isolated_double_digit(digits(password))]
println("Part 2: Number of possible passwords: $(length(passwords))")