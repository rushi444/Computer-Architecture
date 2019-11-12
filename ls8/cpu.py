"""CPU functionality."""

import sys

LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010,  # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111,  # PRN R0
            0b00000000,
            0b00000001,  # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
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

        # self.ram_read(instruction)

        # cascade if elif statements for each instruction

        # while not halted ?
        # HLT
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

            # PRN = print numeric value stored in given register
            # # print to th econsole the decimal int value that is stored in reg
            elif instruction == PRN:
                value = self.reg_read(self.ram_read(self.pc + 1))
                print(f"Print: {value}")

                self.pc += 2
            else:
                print(f"Unknown instruction at index {self.pc}")
                sys.exit(1)