using Combinatorics
include("intcode.jl")

"""Compute the thruster signal given prog to run on amplifiers and phase setting list"""
function thruster_signal(prog, phase_settings)
    previous_output = 0
    for phase_setting in phase_settings
        previous_output = first(run_intcode!(copy(prog), [phase_setting, previous_output]))
    end
    return previous_output
end

"""Compute the thruster signal in feedback mode after all programs halt"""
function feedback_signal(prog, phase_settings)
    io_channels = [Channel(4) for i in 1:5]
    for (io_channel, phase_setting) in zip(io_channels, phase_settings) put!(io_channel, phase_setting) end
    put!(first(io_channels), 0)
    @sync for i in 1:5
        @async run_intcode!(copy(prog), io_channels[i], io_channels[i%5 + 1])
    end
    return take!(first(io_channels))
end

# Part 1: run the amplifier program with all permutations of 01234 as phase settings
prog = open(f -> parse.(Int32, split(readline(f), ",")), "day07_input.txt")
signals = [thruster_signal(prog, phase_settings) for phase_settings in permutations(0:4)]
println("Highest thruster signal: $(maximum(signals))")

# Part 2: this time we keep running in feedback mode
signals = [feedback_signal(prog, phase_settings) for phase_settings in permutations(5:9)]
println("Highest feedback thruster signal: $(maximum(signals))")
