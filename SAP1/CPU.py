from Memory import *

class CPU:
    def __init__(self):
        # Registers
        self.A = 0
        self.B = 0
        self.PC = 0
        self.IR = 0
        self.OUT = 0

        # Memory
        self.memory = Memory(16)


    def loadROM(self, program, start_address = 0):
        self.memory.write(program, start_address)


    def peek(self, address):
        return self.memory[address]


    def poke(self, address, value):
        self.memory[address] = value


    def run(self):
        HALT = False

        while not HALT:
            # fetch instruction
            self.IR = self.memory[self.PC]

            # increment pc
            self.PC += 1
         
            # split instruction
            opcode, address = self.IR >> 4, self.IR & 0x0F

            if self.PC > 15 and opcode != 0xF:
                raise ValueError("Invalid Program (Program Counter Overflow): SAP-1 programs must end with a HLT instruction")
            
            # decode / execute instruction
            match opcode:
            
                case 0x0:
                    self.A = self.memory[address]

                case 0x1:
                    self.B = self.memory[address]
                    self.A = (self.A + self.B) & 0xFF

                case 0x2:
                    self.B = self.memory[address]
                    self.A = (self.A - self.B) & 0xFF

                case 0xE:
                    self.out = self.A
                    print(bin(self.out))

                case 0xF:
                    HALT = True

                case _:
                    raise ValueError(f"Invalid Opcode {opcode:04b} at Memory Address {address}")