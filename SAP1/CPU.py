from Memory import *

class CPU:
    def __init__(self):
        # Registers
        self.A = Register("A")
        self.B = Register("B")

        self.PC = Register("PC", 4)
        self.MAR = Register("MAR", 4)
        self.IR = Register("IR")
        
        self.IO = Register("IO")

        # Memory
        self.RAM = Memory(16)

        # Flags
        self.haltFlag = False

        # Instruction table
        self.instructionTable = {
            0x0 : self.LDA,
            0x1 : self.ADD,
            0x2 : self.SUB,
            0xE : self.OUT,
            0xF : self.HLT
        }


    def program(self, program, start_address = 0):
        self.RAM.write(program, start_address)

    
    def run(self):
        self.haltFlag = False

        while not self.haltFlag:
            self.fetchInstruction()
            self.executeInstruction()


    def peek(self, address):
        return self.RAM[address]


    def poke(self, address, value):
        self.RAM[address] = value


    def fetchInstruction(self):
        self.MAR = self.PC
        self.IR = self.RAM[self.MAR]
        self.PC.increment()


    def executeInstruction(self):
        opcode, address = self.IR >> 4, self.IR & 0x0F
        self.MAR = address

        if self.PC > 15 and opcode != 0xF:
            raise ValueError("Invalid Program (Program Counter Overflow): SAP-1 programs must end with a HLT instruction")

        try:
            self.instructionTable[opcode]()

        except KeyError:
            raise ValueError(f"Invalid Opcode {opcode:04b} at Memory Address {address}")

    
    def LDA(self):
        self.A = self.RAM[self.MAR]
    

    def ADD(self):
        self.B = self.RAM[self.MAR]
        self.A += self.B


    def SUB(self):
        self.B = self.RAM[self.MAR]
        self.A -= self.B


    def OUT(self):
        self.IO = self.A
        print(self.IO)


    def HLT(self):
        self.haltFlag = True