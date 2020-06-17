"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.running = True
        self.functions_dict = {}

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

        # Grab the file with the intructions entered,
        # after running this program:
        intruction_file = sys.argv[1]

        # TODO: error checking on sys.argv

        with open(intruction_file) as f:
            # Go through each line,
            # and grab the index for each
            for index, line in enumerate(f):
                # Split the string by #
                str_line = line.split("#")

                # Try to get the number in that line
                try:
                    number = int(str_line[0], 2)  # The 2 tells it that this should be a base 2 number (binary)
                    # Save it in RAM
                    self.ram_write(index, number)

                # If you can't, just continue to the next line
                except ValueError:
                    continue

        # Print what you have in memory for index 0-num
        num = 15
        print(f"\nRAM's current state from [:{num}]: \n{self.ram[:num]}\n")

        # Set up functions dictionary
        self.setup_functions_dict()
    
    # Set up functions dictionary
    def setup_functions_dict(self):
        self.functions_dict = {
            self.HLT : self.halt,
            self.PRN : self.print_somth,
            self.LDI : self.ldi
        }

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

    # Return what's in RAM at this index (program_counter)
    def ram_read(self, program_counter):
        return self.ram[program_counter]

    # Save a value into RAM, at this index (program_counter)
    def ram_write(self, program_counter, value):
        self.ram[program_counter] = value
        return value

    # Run the CPU
    def run(self):
        self.trace()  # For debugging

        # While-Loop that constantly runs the Program
        while self.running:
            # Set the current_instruction
            curr_instruction = self.ram[self.program_counter]

            # Print what instruction is currently beign called
            print(f"\nIntruction called: {curr_instruction}")
            print(f"program counter: {self.program_counter}\n")

            # If curr_instruction is in the functions_dictionary
            if curr_instruction in self.functions_dict:
                # Call the function for that instruction
                f = self.functions_dict[curr_instruction]
                f()

            # Else: If that instruction is not in the functions_dict
            else:
                # Just go to the next instruction
                self.program_counter += 1

    # Stop running the program
    def halt(self):
        # Set running to False, to stop the While-Loop
        self.running = False

        # Print that we used HALT
        print(f"Gonna HALT now..")

    # Some printing function
    def print_somth(self):
        # TODO: Still need to properly implement this function

        # Go to the next instruction
        self.program_counter += 1

        # Alert that we called this function
        print("Asked to print something")

    # Saving a value in a Register
    def ldi(self):
        # grab the next intruction from RAM;
        # Which it's the register_index at which to save the value
        self.program_counter += 1
        reg_index = self.ram[self.program_counter]

        # Grab the next intruction,
        # Which is the value that needs to be saved
        self.program_counter += 1
        num = self.ram[self.program_counter]

        # Save that value in correct Register
        self.registers[reg_index] = num

        # Go to the next instruction
        self.program_counter += 1

        print(f"Used LDI.\nSaved num: {num}, at reg: {reg_index}")


        


