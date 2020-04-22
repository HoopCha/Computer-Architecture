"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
POP = 0b01000110
PUSH = 0b01000101
SP = 7 #This is always reserved for the stack pointer. 

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.pc = 0

    def load(self):
        """Load a program into memory."""
        try:
            filename = sys.argv[1]
            address = 0
            with open(filename) as f:
                for line in f:
                    # remove comments
                    line = line.split("#")
                    # remove whitespace
                    line = line[0].strip()
                    # skip empty lines
                    if line == "":
                        continue
                    value = int(line, 2)
                    # set the instruction to memory
                    self.ram[address] = value
                    address += 1
        except FileNotFoundError:
            print("File not found")
            sys.exit(2)

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        running = True

        while running:
            IR = self.ram[self.pc]

            if IR == LDI:
                # store value in register
                a = self.ram_read(self.pc + 1)
                b = self.ram_read(self.pc + 2)
                self.reg[a] = b
                self.pc += 3

            elif IR == PRN:
                #Print 
                data = self.ram_read(self.pc + 1)
                print(self.reg[data])
                self.pc += 2

            elif IR == MUL:
                #Multiply
                a = self.ram[self.pc + 1]
                b = self.ram[self.pc + 2]
                self.reg[a] *= self.reg[b]
                self.pc += 3

            elif IR == PUSH:
                #Push
                #Grab the register argument
                reg = self.ram[self.pc + 1]
                val = self.reg[reg]
                #Decrement the SP
                self.reg[SP] -= 1
                #Copy the value in the register to the address pointed by the SP
                self.ram[self.reg[SP]] = val

                self.pc += 2

            elif IR == POP:
                #Pop
                #Grab the register argument
                reg = self.ram[self.pc + 1]
                val = self.ram[self.reg[SP]]
                # Copy the value of address pointed to by SP to given reg
                self.reg[reg] = val
                #Increment the SP
                self.reg[SP] += 1
                self.pc += 2

            elif IR == HLT:
                running = False


test = CPU()
test.load()
test.run()


