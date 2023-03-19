class CPU:
    def __init__(self):
        # Registers
        self.A = 0
        self.B = 0
        self.PC = 0
        self.IR = 0
        self.OUT = 0

        # Memory
        self.memory = [0x0F, # 0 LDA 0xF
                       0xE0, # 1 OUT (0b1)
                       0x1E, # 2 ADD 0xE
                       0xE0, # 3 OUT (0b11)
                       0x1D, # 4 ADD 0xD
                       0xE0, # 5 OUT (0b110)
                       0x2C, # 6 SUB 0xC
                       0xE0, # 7 OUT (0b10)
                       0x2B, # 8 SUB 0xB
                       0xE0, # 9 OUT (0b11111101)
                       0xFF, # A HLT
                       0x05, # B 5
                       0x04, # C 4
                       0x03, # D 3
                       0x02, # E 2
                       0x01] # F 1

    def run(self):
        halted = False

        while not halted:
            # fetch instruction
            self.IR = self.memory[self.PC]

            # increment pc
            self.PC += 1

            # split instruction
            opcode, address = self.IR >> 4, self.IR & 0x0F
            
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
                    halted = True
                case _:
                    halted = True
                    print(f"Invalid Opcode {bin(opcode)} at Memory Address {address}")
                    
