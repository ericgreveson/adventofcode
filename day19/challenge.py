from ast import literal_eval

from aoc.challenge_base import ChallengeBase
from day16.challenge import Emulator

class Challenge(ChallengeBase):
    """
    Day 16 challenges
    """
    def parse_input(self):
        """
        Parse input lines
        """
        # Parse the input program and parse any #ip commands
        self.program = []
        for line in self.lines:
            stripped_line = line.strip()
            if stripped_line.startswith("#ip "):
                self.ip_reg = int(stripped_line[len("#ip "):])
            elif stripped_line:
                tokens = stripped_line.split(" ")
                instruction = [tokens[0]] + [int(token) for token in tokens[1:]]
                self.program.append(instruction)

    def execute_program(self, emulator, callback=None, ip=0):
        """
        Execute the program on the given emulator
        emulator: The emulator to run the program on
        callback: Function to call after each instruction with the current IP
        ip: initial instruction pointer value
        """
        while ip >=0 and ip < len(self.program):
            # Write IP value to IP reg
            emulator.registers[self.ip_reg] = ip

            # Execute instruction
            instruction = self.program[ip]
            emulator.dispatch_table[instruction[0]](*instruction[1:])

            # Read IP back from IP reg
            ip = emulator.registers[self.ip_reg]

            # Increment IP as per requirements
            ip += 1

            if callback:
                callback(ip)

    def challenge1(self):
        """
        Day 16 challenge 1
        """
        self.parse_input()

        # Create emulator, with 6 registers
        emulator = Emulator(6)

        # Run the program until the halt condition
        self.execute_program(emulator)

        print(f"Final value of registers: {emulator.registers}")

    def challenge2(self):
        """
        Day 16 challenge 2
        """
        # Create emulator, with 6 registers. Set register 0 to 1
        emulator = Emulator(6)
        emulator.registers[0] = 1

        # Running this program seems to take forever... let's see if there's a pattern.
        # OK, so after dumping out about 1000000 instructions, there is an obvious pattern.
        # IP:  4 Reg: [0, 1, 10551376, 145834, 3, 145834]
        # ...
        # IP:  4 Reg: [0, 1, 10551376, 145835, 3, 145835]
        # ...
        # etc etc. When would this pattern end? Let's help it out a bit.
        # We would need to optimize the inner loop that's taking all the time by figuring out what it does...

        print(f"Final value of registers: {emulator.registers}")
