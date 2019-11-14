"""CPU functionality."""

import sys

LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.SP = 7
        self.reg[self.SP] = 0xf4  # initalize SP to empty stack

    def load(self):
        """Load a program into memory."""

        if len(sys.argv) != 2:
            print("usage: file")
            sys.exit(1)

        file = sys.argv[1]

        address = 0

        with open(file) as f:
            for line in f:
                line = line.split("#")[0]
                line = line.strip()

                if line == "":
                    continue

                val = int(line, 2)
                # print(val)

                self.ram[address] = val
                address += 1

        # If using hardcoded program = []
        # --------------------------
        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == MUL:
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def ram_read(self, MAR):
        """
        Accept the address to read and return the value stored there.
        """
        # Accepts the Address to read and returns the value stored there.
        return self.ram[MAR]

    def ram_write(self, MAR, MDR):
        """
        Accept a value to write and the address to write it to.
        """
        # accepts the MDR (value) and returns the address (MAR) to write it to.
        self.ram[MAR] = MDR

    def reg_read(self, MAR):
        """
        Accept the address to read and return the value stored there.
        """
        # Accepts the Address to read and returns the value stored there.
        return self.reg[MAR]

    def reg_write(self, MAR, MDR):
        """
        Accept a value to write and the address to write it to.
        """
        # accepts the MDR (value) and returns the address (MAR) to write it to.
        self.reg[MAR] = MDR

    def run(self):
        """Run the CPU."""

        # ready from ram_read() the bytes at PC+1 and PC+2
        # set them to variables operand_a and operand_b

        while self.ram_read(self.pc) != HLT:
            instruction = self.ram_read(self.pc)
            # LDI = Load 'immediate', set this register to 'value'
            # has two oprands, pc + 1 (registerID) and (int)pc + 2
            if instruction == LDI:
                register = self.ram_read(self.pc + 1)
                value = self.ram_read(self.pc + 2)

                self.reg_write(register, value)

                # Advance pc
                self.pc += 3
                # self.trace()

            elif instruction == MUL:
                self.alu(MUL, self.ram_read(self.pc + 1),
                         self.ram_read(self.pc + 2))

                self.pc += 3

            elif instruction == PUSH:
                self.reg[self.SP] -= 1  # decrement stack pointer

                # Copy the value in the given register to the address pointed to by SP

                # Address of register in ram
                reg_address = self.ram[self.pc + 1]
                # reg value from the given register in ram address
                reg_value = self.reg_read(reg_address)

                # copy reg value into memory at address self.SP
                self.ram[self.reg[self.SP]] = reg_value

                self.pc += 2

                # self.trace()

            elif instruction == POP:
                # copy the value from the address pointed to by SP to the given register

                # value from the address pointed to by SP in REG
                reg_value = self.ram_read(self.reg_read(self.SP))
                # the given register from file, location: pc + 1 in ram
                reg_num = self.ram[self.pc + 1]

                # copying the VALUE from above TO the register
                self.reg[reg_num] = reg_value
                # increment SP
                self.reg[self.SP] += 1

                self.pc += 2

                # self.trace()

            # elif instruction == CALL:
            #     pass

            # elif instruction == RET:
            #     pass

            # PRN = print numeric value stored in given register
            # # print to th econsole the decimal int value that is stored in reg
            elif instruction == PRN:
                value = self.reg_read(self.ram_read(self.pc + 1))
                print(f"Print: {value}")

                self.pc += 2
                self.trace()
            else:
                print(f"Unknown instruction at index {self.pc}")
                sys.exit(1)