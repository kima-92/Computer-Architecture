"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.running = True

        self.program_counter = 0        # Index of the current executing intruction
        self.instruction_register = 0   # Copy of the program_counter
        self.mar = 0                    # Memory Address Register, holds the memory address we're reading or writing
        self.mdr = 0                    # Memory Data Register, holds the value to write or the value just read
        self.flags = []                 # Flags, current flags status

        self.registers = [0] * 8        # 8 general-purpose registers, like variables. R0, R1, R2, R3...

        # Commands
        self.HLT = 0b00000001
        self.PRN = 0b01000111
        self.LDI = 0b10000010

    def load(self):
        """Load a program into memory."""
        address = 0

        # For now, we've just hardcoded a program:
        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def alu(self, op, registers_a, registers_b):
        """ALU operations."""

        if op == "ADD":
            self.registers[registers_a] += self.reg[registers_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.program_counter,
            #self.fl,
            #self.ie,
            self.ram_read(self.program_counter),
            self.ram_read(self.program_counter + 1),
            self.ram_read(self.program_counter + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.registers[i], end='')

        print()

    def ram_read(self, program_counter):
        return self.ram[program_counter]

    def run(self):
        """Run the CPU."""
        self.trace()  # For debugging

        while self.running:
            
            instruction_register = self.ram[self.program_counter]

            if instruction_register == self.PRN:
                print("Asked to print something")
                self.program_counter += 1

            elif instruction_register == self.HLT:
                print(f"Gonna HALT now..")
                self.running = False
                self.program_counter += 1

            else:
                self.program_counter += 1

