module day21

parseline(line) = Set.(split.(split(rstrip(replace(line, "," => ""), ')'), " (contains "), " "))

function safeingredients(info, ingredients, allergens)
    allergmap = Dict(a => [i for i in info if a ∈ i[2]] for a in allergens)
    candidates = Dict(a => intersect(map(ing -> ing[1], i)...) for (a, i) in allergmap)
    setdiff(Set(ingredients), union(values(candidates)...))
end

info = parseline.(readlines("day21_input.txt"))
# info = [[Set(["mxmxvkd", "kfcds", "sqjhc", "nhms"]), Set(["dairy", "fish"])],
#         [Set(["trh", "fvjkl", "sbzzf", "mxmxvkd"]), Set(["dairy"])],
#         [Set(["sqjhc", "fvjkl"]), Set(["soy"])],
#         [Set(["sqjhc", "mxmxvkd", "sbzzf"]), Set(["fish"])]]
ingredients = union(map(x -> x[1], info)...)
allergens = union(map(x -> x[2], info)...)
safe = safeingredients(info, ingredients, allergens)
println("Part 1: count = $(sum(map(item -> length(safe ∩ item[1]), info)))")

# Part 2
function knownallergens(info, allergens)
    allergmap = Dict(a => [i for i in info if a ∈ i[2]] for a in allergens)
    candidates = Dict(a => intersect(map(ing -> ing[1], i)...) for (a, i) in allergmap)
    known = Dict()
    while !isempty(candidates)
        merge!(known, filter(x -> length(last(x)) == 1, candidates))
        filter!(x -> first(x) ∉ keys(known), candidates)
        candidates = Dict(a => setdiff(ilist, union(values(known)...)) for (a, ilist) in candidates)
    end
    Dict(a => only(i) for (a, i) in known)
end

known = knownallergens(info, allergens)
println("Part 2: $(join([known[a] for a in sort(collect(allergens))], ','))")

end