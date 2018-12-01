import sys

def main(args):
    """
    Day 1 Challenge 1
    """
    freq = 0
    with open(args[0], "rt") as f:
        for line in f.readlines():
            freq += int(line)

    print(f"Final freq: {freq}")

if __name__ == "__main__":
    main(sys.argv[1:])
