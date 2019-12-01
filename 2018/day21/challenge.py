from aoc.challenge_base import ChallengeBase
from day16.challenge import Emulator
from day19.challenge import Challenge as Day19Challenge
class Challenge(Day19Challenge):
    """
    Day 21 challenges
    """
    def challenge1(self):
        """
        Day 21 challenge 1
        """
        # Let's try to understand the program... here is pseudocode...
        # r5 = 123
        # while r5 & 456 != 72:
        #     pass
        # We can optimize all the above "bug check" out, we really start here:

        # r5 = 0
        # do:
        #     r4 = 65536 | r5   (=0x10000 | r5)
        #     r5 = 3935295
        #     while True:
        #         r5 += r4 & 255  (=0xff)
        #         r5 &= 16777215  (=0xffffffff)
        #         r5 *= 65899
        #         r5 &= 16777215 (=0xffffffff)
        #         if r4 < 256:
        #             break
        #
        #         r4 = r4 / 256
        #
        # while r0 != r5
        #
        # So to get it to stop, in the least number of instructions, we need to see what r5 is
        # in the first "eqrr 5 0 2" (instruction 28)
        # It should be as follows:
        # r5 = ((((((((3935295 + (65536 & 255)) & 16777215) * 65899) & 16777215
        #      + 257 & 255) & 16777215) * 65899) & 16777215
        #      + 2 & 255) & 16777215) * 65899) & 16777215
        #    = (((((6577493 + 0) * 65899) & 16777215 + 1) & 16777215) * 65899) & 16777215
        #    = 16457176

        self.parse_input()

        # Create emulator, with 6 registers
        emulator = Emulator(6)

        # Try the number we computed in r0
        emulator.registers[0] = 16457176

        # Run the program until the test condition
        def dump_registers_at_ip28(ip):
            if ip == 28:
                raise RuntimeError()

        try:
            self.execute_program(emulator, callback=dump_registers_at_ip28)
        except RuntimeError:
            print(f"Final register state: {emulator.registers}. Answer is {emulator.registers[0]}.")

    def challenge2(self):
        """
        Day 21 challenge 2
        """
        # Try running the unrolled version instead of emulating things slowly!
        # We should keep going until we loop back round to the first value we found
        r5 = 0
        prev_r5 = 0
        r5_values = set()
        while r5 not in r5_values:
            r5_values.add(r5)
            prev_r5 = r5
            r4 = 65536 | r5
            r5 = 3935295
            while True:
                r5 += r4 & 255
                r5 &= 16777215
                r5 *= 65899
                r5 &= 16777215
                if r4 < 256:
                    break
        
                r4 = r4 // 256

            if len(r5_values) % 1000 == 0:
                print(f"{len(r5_values)}th value: {r5}")

        print(f"Last r5 value: {prev_r5}")