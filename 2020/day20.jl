module day20

struct Tile
    id
    data
    edges
end

bitstoint(arr) = parse(Int, join(UInt8.(arr)), base=2)

function parseimage(s)
    label, data = split(s, ":\n")
    data = Array{Bool}(hcat(map(line -> '#' .== collect(line), split(data, "\n"))...)')
    edges = bitstoint.(vcat(map(f -> f.([data[:, end], data[end, :], data[:, 1], data[1, :]]), [identity, reverse])...))
    Tile(parse(Int, label[5:end]), data, edges)
end

images = parseimage.(split(strip(read("day20_input.txt", String)), "\n\n"))
adj = Dict(im.id => Set(i.id for i in images if i.id != im.id && !isempty(im.edges ∩ i.edges)) for im in images)
println("Part 1: corner product = $(prod([i.id for i in images if length(adj[i.id]) == 2]))")

# Part 2
fourconnected(i) = map(x -> i + CartesianIndex(x...), [(0,1), (1,0), (0,-1), (-1,0)])

function fillgrid(grid, ids, adj)
    region = CartesianIndices(grid)
    if isempty(ids) return true, grid end

    # Try filling the next empty grid square
    i = first(i for i in region if grid[i] == 0)
    neighbours = [grid[j] for j in fourconnected(i) if j in region && grid[j] > 0]
    candidates = intersect(ids, [adj[n] for n in neighbours]...)
    if isempty(candidates) return false, grid end
    for c in candidates
        grid[i] = c
        newids = setdiff(ids, Set(c))
        result, grid = fillgrid(grid, newids, adj)
        if result return result, grid end
    end
    grid[i] = 0
    false, grid
end

function findlayout(images, adj)
    len = Int(sqrt(length(images)))

    # Try each tile in the top left and then see if we can make progress laying out the rest
    for im in images
        if length(adj[im.id]) > 2 continue end
        grid = zeros(Int, (len, len))
        grid[1,1] = im.id
        remaining = Set(i.id for i in images if i.id != im.id)
        filled, grid = fillgrid(grid, remaining, adj)
        if filled return grid end
    end
end

flip(im) = reverse(im, dims=1)
transforms = [identity, rotr90, rot180, rotl90]
alltransforms = [transforms; flip .∘ transforms]

function findtransform(im, nedges)
    for transform in alltransforms
        imt = transform(im)
        edges = bitstoint.([imt[:, end], imt[end, :], imt[:, 1], imt[1, :]])
        if all(map((a, b) -> isnothing(a) || b ∈ a, nedges, edges)) return imt[2:end-1, 2:end-1] end
    end
    edges = bitstoint.([im[:, end], im[end, :], im[:, 1], im[1, :]])
    error("Failed to find transform: nedges = $nedges, ours = $edges")
end

function countmonsterwaves(im)
    template = ["                  # ",
                "#    ##    ##    ###",
                " #  #  #  #  #  #   "]
    monster = Array{Bool}(hcat(map(line -> '#' .== collect(line), template)...)')
    mc = count(monster)
    region = CartesianIndices(im)
    n = 0
    for i in region
        finish = i + CartesianIndex(size(monster)...) - CartesianIndex(1, 1)
        if finish ∉ region continue end
        n += count(im[i:finish] .* monster) == mc ? mc : 0
    end
    n
end

function countwaves(images, adj)
    grid = findlayout(images, adj)
    full = zeros(Bool, size(grid) .* (size(images[1].data) .- (2, 2)))
    region = CartesianIndices(grid)
    imdict = Dict(i.id => i for i in images)
    unity = CartesianIndex(1, 1)
    for i in region
        nedges = [j in region ? Set(imdict[grid[j]].edges ∩ imdict[grid[i]].edges) : nothing for j in fourconnected(i)]
        im = findtransform(imdict[grid[i]].data, nedges)
        start = (i - unity) * size(im)[1] + unity
        finish = start + CartesianIndex(size(im)...) - unity
        full[start:finish] = im
    end

    for transform in alltransforms
        m = countmonsterwaves(transform(full))
        if m > 0 return sum(count(full)) - m end
    end
end

println("Part 2: roughness = $(countwaves(images, adj))")

end