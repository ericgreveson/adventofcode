"""
Parse a wire definition into a list of line segments
wire_def should look like ["R234", "U56", "L78"] etc
"""
function parse_wire_def(wire_def)
    cursor = [0 0]
    directions = Dict(
        'U' => [ 0  1],
        'D' => [ 0 -1],
        'L' => [-1  0],
        'R' => [ 1  0]
    )

    line_segs = []
    for seg in wire_def
        direction = seg[1]
        new_cursor = cursor + directions[direction] * parse(Int32, seg[2:end])
        push!(line_segs, (cursor, new_cursor))
        cursor = new_cursor
    end
    return line_segs
end

"""
Test if two line segments intersect, and if so, return their intersection point
"""
function find_intersection(seg1, seg2)
    # We only need to support vertical vs horizontal segment intersections...
    # at least I think a vert-vert or horz-horz intersection doesn't count based on task definition!
    (sx1, sy1), (ex1, ey1) = seg1
    (sx2, sy2), (ex2, ey2) = seg2
    
    # We need to order our segments so start x / start y are lower than end x / end y in each case
    sx1, sy1, ex1, ey1 = min(sx1, ex1), min(sy1, ey1), max(sx1, ex1), max(sy1, ey1)
    sx2, sy2, ex2, ey2 = min(sx2, ex2), min(sy2, ey2), max(sx2, ex2), max(sy2, ey2)

    # Now let's arrange as horizontal first, then vertical, if possible
    if sx1 == ex1 && sy2 == ey2
        # Vert then horz. Swap them.
        sx1, sy1, ex1, ey1, sx2, sy2, ex2, ey2 = sx2, sy2, ex2, ey2, sx1, sy1, ex1, ey1
    elseif !(sy1 == ey1 && sx2 == ex2)
        # It's not horz then vert either: no intersections
        return nothing
    end

    # OK, now sy1 == ey1 and sx2 == ey2. Is there an intersection?
    return (sy1 in sy2:ey2 && sx2 in sx1:ex1) ? [sx2, sy1] : nothing
end

# Part 1: read and parse input (should be 2 definitions, one for each wire)
w = open(f -> [parse_wire_def(split(line, ',')) for line in readlines(f)], "day03_input.txt")

# Do a stupid all-segs-vs-all-segs test to find all intersection points
isects = []
for seg1 in w[1]
    for seg2 in w[2]
        isect = find_intersection(seg1, seg2)
        if !isnothing(isect)
            push!(isects, isect)
        end
    end
end

# Find lowest Manhattan distance to origin apart from the first (0,0) intersection
filter!(isect -> isect[1] != 0 || isect[2] != 0, isects)
dists = [abs(x) + abs(y) for (x, y) in isects]
println("Minimum distance: $(minimum(dists))")


# Part 2: distance to intersection
"""
Compute lowest distance to the given intersection for the wire defined by list of segments wire_segs
"""
function distance_to_intersection(wire_segs, intersection)
    dist = 0
    for wire_seg in wire_segs
        # Is this wire segment going to hit the intersection?
        (sx, sy), (ex, ey) = wire_seg
        ix, iy = intersection
        if ix == sx == ex && iy in min(sy,ey):max(sy,ey)
            # Vertical segment reaching the intersection
            return dist + abs(iy - sy)
        elseif iy == sy == ey && ix in min(sx,ex):max(sx,ex)
            # Horizontal segment reaching the intersection
            return dist + abs(ix - sx)
        else
            dist += abs(ex - sx) + abs(ey - sy)
        end
    end
    return nothing
end

# Compute distance to each intersection along wire
wdists = [distance_to_intersection(w[1], isect) + distance_to_intersection(w[2], isect) for isect in isects]
println("Lowest combined distance along wire: $(minimum(wdists))")