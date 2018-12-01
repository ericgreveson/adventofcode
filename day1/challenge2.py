import sys

def main(args):
    """
    Day 1 Challenge 2
    """
    with open(args[0], "rt") as f:
        lines = list(f.readlines())

    found = False
    freq = 0
    freqs_hit = {freq}
    while not found:
        for line in lines:
            freq += int(line)
            if freq in freqs_hit:
                found = True
                break
            freqs_hit.add(freq)

    print(f"First repeated freq: {freq}")

if __name__ == "__main__":
    main(sys.argv[1:])
