"""CPU functionality."""

import sys

#These increase readability
LDI = 0b10000010
PRN = 0b001000111
HLT = 0b00000001
MUL = 0b10100010
ADD = 0b10100000
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001
CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110
AND = 0b10101000
OR = 0b10101010
XOR = 0b10101011
NOT = 0b01101001
SHL = 0b10101100
SHR = 0b10101101
MOD = 0b10100100
SP = 7  # R7 is reservered for the pointer to the stack

#Creating the CPU Class
class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""

        # Dispatch table with all the functions
        self.dispatch_table = {LDI: self.ldi, PRN: self.prn, HLT: self.hlt, MUL: self.mul,
                               ADD: self.add, PUSH: self.push, POP: self.pop,
                               CALL: self.call, RET: self.ret, CMP: self.cmp, JMP: self.jmp, 
                               JEQ: self.jeq, JNE: self.jne, AND: self.andO, OR: self.orO, XOR: self.xor,
                               NOT: self.notO, SHL: self.shl, SHR: self.shr, MOD: self.mod}

        self.ram = [0] * 256 
        self.reg = [0] * 8  
        self.pc = 0 
        self.running = False
        self.FL = 0b00000000 


    #Various Functions
    #Sets the value of a register to an int
    def ldi(self, *argv):
        self.reg[argv[0]] = argv[1]
        self.pc += 3
    #Prints the number in given register
    def prn(self, *argv):
        print(self.reg[argv[0]])
        self.pc += 2
    #Halts and exits the emulator
    def hlt(self, *argv):
        self.running = False
        self.pc += 1
    #Multiplies two registers and stores in register A
    def mul(self, *argv):
        self.alu('MUL', argv[0], argv[1])
        self.pc += 3
    #adds two registers and stores in register A
    def add(self, *argv):
        self.alu("ADD", argv[0], argv[1])
        self.pc += 3
    #Push value of register onto the stack
    def push(self, *argv):
        self.reg[SP] -= 1
        self.ram[self.reg[SP]] = self.reg[argv[0]]
        self.pc += 2
    #Pop the value at the top of the stack into the given register
    def pop(self, *argv):
        copy_stack = self.ram[self.reg[SP]]
        self.reg[argv[0]] = copy_stack
        self.reg[SP] += 1
        self.pc += 2
    #Calls a subroutine at the address stored in the register.
    def call(self, *argv):
        self.reg[SP] -= 1
        self.ram[self.reg[SP]] = self.pc + 2
        new_reg = self.ram[self.pc + 1]
        self.pc = self.reg[new_reg]
    #Return from subroutine.
    def ret(self, *argv):
        self.pc = self.ram[self.reg[SP]]
        self.reg[SP] += 1
    #
    def cmp(self, *argv):
        self.alu("CMP", argv[0], argv[1])
        self.pc += 3
    #Jump to address stored in the given register
    def jmp(self, *argv):
        address = self.reg[argv[0]]
        #print("Jump!")
        self.pc = address
    #if equal flag is true jump to address stored in the register
    def jeq(self, *argv):
        address = self.reg[argv[0]]
        if self.FL == 1:
            self.pc = address
        else:
            self.pc += 2
    #if equal flag is clear go to register point
    def jne(self, *argv):
        address = self.reg[argv[0]]
        #print("jne:", self.FL)
        if self.FL == 4 or self.FL == 2:
            self.pc = address
        else:
            self.pc += 2
    def andO(self, *argv):
        self.alu("AND", argv[0], argv[1])
        self.pc += 3
    def orO(self, *argv):
        self.alu("OR", argv[0], argv[1])
        self.pc += 3
    def xor(self, *argv):
        self.alu("XOR", argv[0], argv[1])
        self.pc += 3
    def notO(self, *argv):
        self.alu("NOT", argv[0], argv[1])
        self.pc += 2
    def shl(self, *argv):
        self.alu("SHL", argv[0], argv[1])
        self.pc += 3
    def shr(self, *argv):
        self.alu("SHR", argv[0], argv[1])
        self.pc += 3
    def mod(self, *argv):
        self.alu("MOD", argv[0], argv[1])
        self.pc += 3

    def ram_read(self, mar):
        return self.ram[mar]

    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr

    def load(self, filename):
        """Load a program into memory."""
        address = 0
        try:
            with open(filename) as f:
                for line in f:
                    line = line.split('#')
                    line = line[0].strip()

                    if line == "":
                        continue

                    value = int(line, 2)
                    self.ram[address] = value
                    address += 1

        except FileNotFoundError:
            print("File not found...")
            sys.exit()

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "CMP":
            #print("CMP", self.reg[reg_a], self.reg[reg_b])
            # check equal to
            if self.reg[reg_a] == self.reg[reg_b]:
                self.FL = 0b00000001
            # check greater than
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.FL = 0b00000010
            # check less than
            elif self.reg[reg_a] < self.reg[reg_b]:
                self.FL = 0b00000100
        elif op == "AND": 
            self.reg[reg_a] = self.reg[reg_a] & self.reg[reg_b]
        elif op == "OR": 
            self.reg[reg_a] = self.reg[reg_a] | self.reg[reg_b]
        elif op == "XOR": 
            self.reg[reg_a] = self.reg[reg_a] ^ self.reg[reg_b]
        elif op == "NOT": 
            register = self.reg[reg_a]
            value = self.reg[register]
            self.reg[register] = ~value
        elif op == "SHL": 
            valueA = self.reg[self.reg_a]
            number_of_bits = self.reg[self.reg_b]
            self.reg[self.reg_a] = (valueA << number_of_bits) % 255
        elif op == math_op["SHR"]:
            valueA = self.reg[self.reg_a]
            number_of_bits = self.reg[self.reg_b]
            self.reg[self.reg_a] = (valueA >> number_of_bits) % 255
        elif op == math_op["MOD"]:
            valueA = self.reg[self.reg_a]
            valueB = self.reg[self.reg_b]
            self.reg[self.reg_a] = valueA % valueB

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


    #Runs the CPU
    def run(self):
        """Run the CPU."""
        self.running = True

        while self.running:
            #Set the instruction from the RAM according the PC pointer
            instruction = self.ram[self.pc]
            #print(instruction)
            #Get the followup instructions if any
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            #print(instruction)
            #Check the dispatch table for the instruction then run
            if instruction in self.dispatch_table:
                self.dispatch_table[instruction](operand_a, operand_b)
            else:
                print('Invalid instruction...')
                sys.exit()