from CPU import *

def main():
    SAP1 = CPU()

    program = [0x0F, # 0 LDA 0xF
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

    SAP1.writeMemory(program)
    SAP1.run()

if __name__ == '__main__':
    main()