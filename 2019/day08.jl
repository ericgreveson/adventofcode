# Part 1: Read image and reshape to 25 x 6 x N layers then report required stat
image = reshape(open(f -> parse.(Int8, collect(readline(f))), "day08_input.txt"), 25, 6, :)
layer = image[:, :, argmin(mapslices(sum, map(iszero, image), dims = [1, 2])[:])]
println("count(1) * count(2) = $(sum(layer .== 1) * sum(layer .== 2))")

# Part 2: Collapse layers, 0 is black, 1 is white, 2 is transparent, first layer is top
rendered = mapslices(x -> first(filter(!isequal(2), x)), image, dims=[3])[:, :, 1]
println.([join(map(x -> x == 1 ? "█" : " ", col)) for col in eachcol(rendered)])