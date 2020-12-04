# Part 1 - parse passports
passports = strip.(split(read("day04_input.txt", String), "\n\n"))
passports = map(p -> Dict(split.(split(p), ':')), passports)
required = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]
println("Part 1: There are $(sum(map(p -> issubset(required, keys(p)), passports))) valid passports")

# Part 2
function number_valid(p, key, re, mini, maxi)
    m = match(re, p[key])
    if isnothing(m) return false end
    mini <= parse(Int32, first(m.captures)) <= maxi
end

validators = [
    p -> number_valid(p, "byr", r"^(\d{4})$", 1920, 2002),
    p -> number_valid(p, "iyr", r"^(\d{4})$", 2010, 2020),
    p -> number_valid(p, "eyr", r"^(\d{4})$", 2020, 2030),
    p -> number_valid(p, "hgt", r"^(\d{3})cm$", 150, 193) || number_valid(p, "hgt", r"^(\d{2})in$", 59, 76),
    p -> !isnothing(match(r"^#[0-9a-f]{6}$", p["hcl"])),
    p -> p["ecl"] in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"],
    p -> !isnothing(match(r"^\d{9}$", p["pid"]))
]
is_valid(p) = issubset(required, keys(p)) && all([v(p) for v in validators])
println("Part 2: There are $(sum(is_valid.(passports))) valid passports")
