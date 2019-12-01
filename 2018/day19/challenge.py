from functools import reduce

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
        # OK, so after dumping out lots of instructions, this pattern is repeated a lot:
        # [ 3] mulr 1 5 3
        # [ 4] eqrr 3 2 3
        # [ 5] addr 3 4 4
        # [ 6] addi 4 1 4
        # [ 8] addi 5 1 5
        # [ 9] gtrr 5 2 3
        # [10] addr 4 3 4
        # [11] seti 2 2 4
        # In this program, register 4 is the IP register. (IP is shown in [] above)
        # So instruction 6 is just jumping to instruction 8, we can optimize that out
        # And seti 2 2 4 will act as a jump back to instruction 3 (= 2 + 1)
        # Registers look like this after instruction 3:
        # IP:  4 Reg: [0, 1, 10551376, 145834, 3, 145834]
        # So effectively we have, per loop iteration:
        # reg[3] = reg[1] * reg[5]
        # reg[3] = 1 if reg[3] == reg[2] else 0
        # reg[4] = reg[3] + reg[4] => If the above was false, we go to instruction 6.
        # Otherwise we go to instruction 7 (outside the normal loop flow) and do:
        # addr 1 0 0 => reg[0] = reg[0] + reg[1], then proceed as below.
        # If we stay in the loop, or just fallen through now, we are at instruction 8:
        # reg[5] = reg[5] + reg[1]
        # reg[3] = 1 if reg[5] > reg[2] else 0
        # reg[4] = reg[3] + reg[4] => If the above was false, we go to instruction 11 => back to the start.
        # Otherwise, we jump outside the loop to instruction 12.
        # So to write the above in Python code, with registers named R0 etc:
        # while R5 <= R2:
        #     R3 = R1 * R5
        #     if R3 == R2:
        #         R0 += R1
        #     R5 += R1
        #
        # This appears to be a brute force way of checking if R1 is a factor of R2 - and if it is, adding it to R0
        # After this loop, if we go to instruction 12:
        # addi 1 1 1 => R1 += 1
        # gtrr 1 2 3 => R3 = 1 if R1 > R2 else 0
        # addr 3 4 4
        # seti 1 4 4
        # mulr 4 4 4
        # These last three mean "jump to instruction 2 if R1 <= R2 else terminate (by squaring the IP)"
        # So putting this together, along with instructions 2 and 3 of:
        # seti 1 8 1 => R1 = 1
        # seti 1 3 5 => R5 = 1
        # We are brute-force finding all the factors of R2 and adding all of them together into R0
        # As R2 contains 10551376, we can do this in a cleverer, non brute force way to find the final value of R0!
        number_to_factorize = 10551376
        
        def factors(n):    
            return set(reduce(list.__add__, 
                              ([i, n//i] for i in range(1, int(n**0.5) + 1) if n % i == 0)))

        sum_factors = sum(factors(number_to_factorize))
        print(f"Final value of register 0: {sum_factors}")
