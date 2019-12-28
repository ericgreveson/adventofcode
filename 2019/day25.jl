include("intcode.jl")

function main()
    # Part 1: run the program interactively
    prog = open(f -> parse.(Int64, split(readline(f), ",")), "day25_input.txt")
    input = Channel(1)
    output = Channel(1)
    @sync begin
        # Screen printing loop
        @async begin
            try
                while true
                    print(Char(take!(output)))
                end
            catch InvalidStateException
            end
        end
        # Input loop
        @async begin
            try
                while true
                    command = readline()
                    if command == "q"
                        close(input)
                        close(output)
                        break
                    end
                    [put!(input, c) for c in Int32.(collect("$command\n"))]
                end
            catch InvalidStateException
            end
        end

        # Start the program
        @async begin
            try
                run_intcode!(copy(prog), input, output)
            catch InvalidStateException
            end
        end
    end
    # (answer was 529920)
end
main()