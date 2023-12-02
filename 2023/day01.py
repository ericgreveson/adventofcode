import re

with open("day01_input.txt") as f:
    lines = f.readlines()
    
# Part 1
re_digit = re.compile("[0-9]")
sum = 0
for line in lines:
    matches = re_digit.findall(line)
    sum += int(f"{matches[0]}{matches[-1]}")
        
print(f"Part 1 sum: {sum}")

# Part 2
sum = 0
DIGIT_WORDS = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9}

def to_digit_char(value):
    """Convert a digit word or digit char to a digit char"""
    try:
        return str(DIGIT_WORDS[value])
    except KeyError:
        return value
    
re_mult_exp = "[0-9]"
for digit_word in DIGIT_WORDS.keys():
    re_mult_exp += "|" + digit_word

# Use lookahead to allow overlapping matches (match is zero width)    
re_multi = re.compile(f"(?=({re_mult_exp}))")
for line in lines:
    matches = re_multi.findall(line)
    first_match = to_digit_char(matches[0])
    last_match = to_digit_char(matches[-1])
    print(f"{first_match}{last_match}")
    sum += int(f"{first_match}{last_match}")
    
print(f"Part 2 sum: {sum}")
