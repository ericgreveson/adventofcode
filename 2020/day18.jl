module day18

function evalnext(s; addfirst=false)
    while true
        m = match(r"\((\d+[\+\*])+\d+\)", s)
        if isnothing(m) break end
        val = evalnext(m.match[2:end-1]; addfirst)
        s = replace(s, m.match => "$val")
    end
    
    if addfirst
        while true
            m = match(r"\d+\+\d+", s)
            if isnothing(m) break end
            val = +(parse.(Int64, split(m.match, '+'))...)
            s = replace(s, m.match => "$val")
        end
    end

    lhs = match(r"\d+", s).match
    current = parse(Int64, lhs)
    if length(lhs) == length(s) return current end
    s = s[length(lhs)+1:end]
    while true
        op = Dict('+' => +, '*' => *)[s[1]]
        rhs = match(r"\d+", s[2:end]).match
        current = op(current, parse(Int64, rhs))
        if length(rhs) + 1 == length(s) return current end
        s = s[length(rhs)+2:end]
    end
end

equations = map(x -> replace(x, " "=>""), readlines("day18_input.txt"))
println("Part 1: sum = $(sum(evalnext.(equations)))")

# Part 2
println("Part 2: sum = $(sum(evalnext.(equations; addfirst=true)))")

end