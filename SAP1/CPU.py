from Memory import *
from Register import *

class CPU:
    def __init__(self):
        # Registers
        self.A = Register("A")
        self.B = Register("B")

        self.PC = Register("PC", 4) # program counter
        self.MAR = Register("MAR", 4) # memory address register
        self.OP = Register("OP", 4) # operation decoder register
        self.IR = Register("IR") # instruction register
        
        self.IO = Register("IO") # input/output register

        self.registers = [self.A,
                          self.B,
                          self.PC,
                          self.MAR,
                          self.OP,
                          self.IR,
                          self.IO]

        # Memory
        self.RAM = Memory(16)

        # Flags
        self.flags = {'halt' : 0}

        # Instruction table
        self.instructionTable = {
            0x0 : self.LDA,
            0x1 : self.ADD,
            0x2 : self.SUB,
            0xE : self.OUT,
            0xF : self.HLT
        }


    def display_state(self, start_address = 0, end_address = None):
        print('\nRegisters')
        for register in self.registers:
            register.bindump()

        print("\nFlags")
        for flag_name, flag_value in self.flags.items():
            print(f"{flag_name}: {flag_value}")

        print("\nRAM")
        self.RAM.bindump(start_address, end_address)


    def program(self, program, start_address = 0):
        self.RAM.write(program, start_address)

    
    def run(self):
        self.flags['halt'] = 0

        while not self.flags['halt']:
            self.fetchInstruction()
            self.executeInstruction()


    def fetchInstruction(self):
        self.PC.transfer_to(self.MAR)
        self.IR.load(self.RAM, self.MAR.value)
        self.PC.inc()


    def executeInstruction(self):
        self.OP.value = self.IR.msb(4) # 4 MSBs
        self.MAR.value = self.IR.lsb(4) # 4 LSBs

        if self.PC.value > 15 and self.OP.value != 0xF:
            raise ValueError("Invalid Program (Program Counter Overflow): SAP-1 programs must end with a HLT instruction")

        try:
            self.instructionTable[self.OP.value]()

        except KeyError:
            raise ValueError(f"Invalid Opcode {self.OP.value:04b} at Memory Address {self.MAR.value}")

    
    def LDA(self):
        self.A.load(self.RAM, self.MAR.value)
    

    def ADD(self):
        self.B.load(self.RAM, self.MAR.value)
        self.A.add(self.B)


    def SUB(self):
        self.B.load(self.RAM, self.MAR.value)
        self.A.sub(self.B)


    def OUT(self):
        self.A.transfer_to(self.IO)
        print(self.IO.value)


    def HLT(self):
        self.flags['halt'] = 1


    def peek(self, address):
        return self.RAM[address]


    def poke(self, address, value):
        self.RAM[address] = value