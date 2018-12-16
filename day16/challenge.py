from ast import literal_eval

from aoc.challenge_base import ChallengeBase

class Sample:
    """
    Register/operation/register sample
    """
    def __init__(self, before, instruction, after):
        """
        Constructor
        before: array of register states before
        instruction: array of [opcode, op1, op2, op3]
        after: array of register states after
        """
        self.before = before
        self.instruction = instruction
        self.after = after

class Emulator:
    """
    Emulator for the wrist device
    """
    def __init__(self):
        """
        Constructor
        """
        self.registers = [0, 0, 0, 0]
        self.dispatch_table = {
            "addr": self.addr,
            "addi": self.addi,
            "mulr": self.mulr,
            "muli": self.muli,
            "banr": self.banr,
            "bani": self.bani,
            "borr": self.borr,
            "bori": self.bori,
            "setr": self.setr,
            "seti": self.seti,
            "gtir": self.gtir,
            "gtri": self.gtri,
            "gtrr": self.gtrr,
            "eqir": self.eqir,
            "eqri": self.eqri,
            "eqrr": self.eqrr
        }

    def set_registers(self, new_state):
        """
        Copy new_state into the registers
        """
        for i in range(4):
            self.registers[i] = new_state[i]

    def addr(self, a, b, c):
        """
        addr (add register) stores into register C the result of adding register A and register B.
        """
        self.registers[c] = self.registers[a] + self.registers[b]

    def addi(self, a, b, c):
        """
        addi (add immediate) stores into register C the result of adding register A and value B.
        """
        self.registers[c] = self.registers[a] + b
        
    def mulr(self, a, b, c):
        """
        mulr (multiply register) stores into register C the result of multiplying register A and register B.
        """
        self.registers[c] = self.registers[a] * self.registers[b]

    def muli(self, a, b, c):
        """
        muli (multiply immediate) stores into register C the result of multiplying register A and value B.
        """
        self.registers[c] = self.registers[a] * b

    def banr(self, a, b, c):
        """
        banr (bitwise AND register) stores into register C the result of the bitwise AND of register A and register B.
        """
        self.registers[c] = self.registers[a] & self.registers[b]

    def bani(self, a, b, c):
        """
        bani (bitwise AND immediate) stores into register C the result of the bitwise AND of register A and value B.
        """
        self.registers[c] = self.registers[a] & b

    def borr(self, a, b, c):
        """
        borr (bitwise OR register) stores into register C the result of the bitwise OR of register A and register B.
        """
        self.registers[c] = self.registers[a] | self.registers[b]

    def bori(self, a, b, c):
        """
        bori (bitwise OR immediate) stores into register C the result of the bitwise OR of register A and value B.
        """
        self.registers[c] = self.registers[a] | b

    def setr(self, a, b, c):
        """
        setr (set register) copies the contents of register A into register C. (Input B is ignored.)
        """
        self.registers[c] = self.registers[a]

    def seti(self, a, b, c):
        """
        seti (set immediate) stores value A into register C. (Input B is ignored.)
        """
        self.registers[c] = a

    def gtir(self, a, b, c):
        """
        gtir (greater-than immediate/register) sets register C to 1 if value A is greater than register B.
        Otherwise, register C is set to 0.
        """
        self.registers[c] = 1 if a > self.registers[b] else 0

    def gtri(self, a, b, c):
        """
        gtri (greater-than register/immediate) sets register C to 1 if register A is greater than value B.
        Otherwise, register C is set to 0.
        """
        self.registers[c] = 1 if self.registers[a] > b else 0

    def gtrr(self, a, b, c):
        """
        gtrr (greater-than register/register) sets register C to 1 if register A is greater than register B.
        Otherwise, register C is set to 0.
        """
        self.registers[c] = 1 if self.registers[a] > self.registers[b] else 0

    def eqir(self, a, b, c):
        """
        eqir (equal immediate/register) sets register C to 1 if value A is equal to register B.
        Otherwise, register C is set to 0.
        """
        self.registers[c] = 1 if a == self.registers[b] else 0

    def eqri(self, a, b, c):
        """
        eqri (equal register/immediate) sets register C to 1 if register A is equal to value B.
        Otherwise, register C is set to 0.
        """
        self.registers[c] = 1 if self.registers[a] == b else 0

    def eqrr(self, a, b, c):
        """
        eqrr (equal register/register) sets register C to 1 if register A is equal to register B.
        Otherwise, register C is set to 0.
        """
        self.registers[c] = 1 if self.registers[a] == self.registers[b] else 0

class Challenge(ChallengeBase):
    """
    Day 16 challenges
    """
    def parse_input(self):
        """
        Parse input lines
        """
        # First, load up all the samples
        is_sample = True
        current_line = 0
        self.samples = []
        while is_sample:
            # Samples come in blocks of 4 lines
            before = literal_eval(self.lines[current_line].strip()[len("Before: "):].strip())
            instruction = self.lines[current_line + 1].strip().split(" ")
            after = literal_eval(self.lines[current_line + 2].strip()[len("After: "):].strip())
            self.samples.append(Sample([int(b) for b in before], [int(i) for i in instruction], [int(a) for a in after]))

            # Is the next one a sample too?
            current_line += 4
            is_sample = len(self.lines[current_line].strip()) > 0

        # OK, now we can parse the sample program
        self.sample_program = []
        for line in self.lines[current_line:]:
            stripped_line = line.strip()
            if stripped_line:
                instruction = [int(i) for i in stripped_line.split(" ")]
                self.sample_program.append(instruction)

    def challenge1(self):
        """
        Day 16 challenge 1
        """
        self.parse_input()

        samples_with_three_or_more = []
        emulator = Emulator()
        self.possible_opcodes = {i: {opcode for opcode in emulator.dispatch_table.keys()} for i in range(16)}
        for sample in self.samples:
            # Try all opcodes and see if they work
            working_opcode_count = 0
            possible_opcodes_for_sample = set()
            for opcode, func in emulator.dispatch_table.items():
                # Set emulator state
                emulator.set_registers(sample.before)

                # Run the instruction
                func(*sample.instruction[1:])
                if emulator.registers == sample.after:
                    possible_opcodes_for_sample.add(opcode)
                    working_opcode_count += 1

            self.possible_opcodes[sample.instruction[0]].intersection_update(possible_opcodes_for_sample)
            if working_opcode_count >= 3:
                samples_with_three_or_more.append(sample)

        print(f"Samples with >= 3 opcode options: {len(samples_with_three_or_more)}")

    def challenge2(self):
        """
        Day 16 challenge 2
        """
        # Figure out opcode mappings iteratively
        opcode_mappings = dict()
        while len(opcode_mappings.keys()) < 16:
            # Any unique mappings?
            for opnum, opcodes in self.possible_opcodes.items():
                if len(opcodes) == 1:
                    # Yep, this one's good
                    opcode_str = next(iter(opcodes))
                    opcode_mappings[opnum] = opcode_str

                    # Remove it from all other sets
                    for opnum, opcodes in self.possible_opcodes.items():
                        opcodes.discard(opcode_str)

                    # Next iteration
                    break

        # Execute program
        emulator = Emulator()
        for instruction in self.sample_program:
            # Map the numeric opcode to the name, and run it
            opcode = opcode_mappings[instruction[0]]
            emulator.dispatch_table[opcode](*instruction[1:])

        # What's the final state?
        print(f"Final register state: {emulator.registers}")
