include("intcode.jl")

mutable struct IntcodeComputer
    address::Int32
    input::Channel
    output::Channel
    idle::Bool
end

"""Simulate the NAT behaviour, return true if message sent twice in a row"""
function do_nat(nat_state, nat_sent_state, computers) 
    if length(nat_state) > 0
        x, y = nat_state[end]
        push!(nat_sent_state, (x, y))
        if length(nat_sent_state) > 1 && nat_sent_state[end][2] == nat_sent_state[end-1][2]
            println("First NAT message sent twice: $x, $y")
            for computer in computers
                close(computer.input)
                close(computer.output)
            end
            return true
        else
            println("Computers are idle: NAT sending $x, $y")
            put!(computers[1].input, x)
            put!(computers[1].input, y)
        end
    end
    return false
end

function main(path=:part1)
    # Fire up 50 intcode computers
    prog = open(f -> parse.(Int64, split(readline(f), ",")), "day23_input.txt")
    computers = [IntcodeComputer(i, Channel(2), Channel(3), false) for i in 0:49]
    [put!(computers[i].input, computers[i].address) for i in 1:length(computers)]
    nat_state = []
    nat_sent_state = []
    @sync begin
        for (i, computer) in enumerate(computers)
            @async begin
                # Output loop: take triples of results and route them to the appropriate machine
                try
                    while true
                        dest_addr = take!(computer.output)
                        x = take!(computer.output)
                        y = take!(computer.output)
                        computer.idle = false
                        if dest_addr == 255
                            if path == :part1
                                println("Computer $i: First packet sent to 255: X=$x, Y=$y")
                                for computer in computers
                                    close(computer.input)
                                    close(computer.output)
                                end
                            else
                                # Send to NAT
                                println("Received NAT message from computer $i: $x, $y")
                                push!(nat_state, (x, y))
                            end
                        elseif dest_addr < 50
                            println("Computer $i: Writing ($x, $y) to computer $dest_addr")
                            put!(computers[dest_addr+1].input, x)
                            put!(computers[dest_addr+1].input, y)
                        else
                            println("Computer $i: Unknown destination $dest_addr, dropping packet")
                        end
                    end
                catch InvalidStateException
                end
            end
            @async begin
                # Input loop: feed -1 to the input periodically
                try
                    while true
                        sleep(0.05)
                        put!(computer.input, -1)
                        put!(computer.input, -1)
                        computer.idle = true
                    end
                catch InvalidStateException
                end
            end
            @async begin
                try
                    run_intcode!(copy(prog), computer.input, computer.output)
                catch InvalidStateException
                end
            end
        end

        @async begin
            # NAT loop
            while true
                sleep(0.1)
                if all(map(x -> x.idle, computers))
                    if do_nat(nat_state, nat_sent_state, computers) break end
                end
            end
        end
    end
end

# Part 1: build Intcode computer network and wait for an output instruction to address 255
#main(:part1)
# Part 2: do NAT instructions
main(:part2)