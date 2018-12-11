import importlib
import os
import sys

def main(argv):
    """
    Entry point for running any challenge
    argv: command-line arguments
    """
    # Check args
    if len(argv) != 2 or not argv[1].startswith("day"):
        print(f"Usage: {argv[0]} <day1|day2|...>")
        sys.exit(1)

    # Load challenge code and execute both challenges
    day_name = argv[1]
    day_module = importlib.import_module(day_name + ".challenge")
    day_challenge = day_module.Challenge()

    # Load input data for this day, should be in day1/input.txt, etc
    # If not, no worries, maybe there's no input file
    input_file = os.path.join(day_name, "input.txt")
    print(f"Loading input from {input_file}...")
    try:
        day_challenge.load_input(input_file)
    except FileNotFoundError:
        print(f"No input file found.")
    
    print("Challenge 1 executing...")
    day_challenge.challenge1()

    print("Challenge 2 executing...")
    day_challenge.challenge2()

    sys.exit(0)

if __name__ == "__main__":
    main(sys.argv)
