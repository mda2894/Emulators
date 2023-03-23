'''SAP-2 CPU - Still updating from SAP-1'''
from lib.memory import Memory
from lib.register import Register
from lib.clock import Clock
from lib.flagregister import FlagRegister

K = 1024

class CPU:
    def __init__(self, clockspeed = 1_000_000):
        # Memory
        self.RAM = Memory(64*K)

        # Clock
        self.clock = Clock(clockspeed)

        # Registers
        self.A = Register("A") # accumulator
        self.TMP = Register("TMP") # temp register used for ALU instructions

        self.B = Register("B") # B & C general purpose registers
        self.C = Register("C")

        self.PC = Register("PC", 16) # program counter
        self.MAR = Register("MAR", 16) # memory address register

        self.MDR = Register("MDR") # memory data register
        self.IR = Register("IR") # instruction register
        self.OP = Register("OP") # operation decode register

        # IO
        self.IN1 = Register("IN1") # input ports 1 & 2
        self.IN2 = Register("IN2")

        self.OUT3 = Register("OUT3") # output ports 3 & 4
        self.OUT4 = Register("OUT4")

        self.registers = [
            self.A,
            self.TMP,
            self.B,
            self.C,
            self.PC,
            self.MAR,
            self.MDR,
            self.IR,
            self.OP,
            self.IN1,
            self.IN2,
            self.OUT3,
            self.OUT4
        ]

        # Flag Register
        self.flag = FlagRegister(
            "halt",
            "sign",
            "zero"
        )

        # Instruction table
        self.instruction_table = {
            0x00 : self.NOP,
            0x04 : self.INRB,
            0x05 : self.DCRB,
            0x06 : self.MVIB,
            0x0C : self.INRC,
            0x0D : self.DCRC,
            0x0E : self.MVIC,
            0x17 : self.RAL,
            0x1F : self.RAR,
            0x2F : self.CMA,
            0x32 : self.STA,
            0x3A : self.LDA,
            0x3C : self.INRA,
            0x3D : self.DCRA,
            0x3E : self.MVIA,
            0x41 : self.MOVBC,
            0x47 : self.MOVBA,
            0x48 : self.MOVCB,
            0x4F : self.MOVCA,
            0x76 : self.HLT,
            0x78 : self.MOVAB,
            0x79 : self.MOVAC,
            0x80 : self.ADDB,
            0x81 : self.ADDC,
            0x90 : self.SUBB,
            0x91 : self.SUBC,
            0xA0 : self.ANAB,
            0xA1 : self.ANAC,
            0xA8 : self.XRAB,
            0xA9 : self.XRAC,
            0xB0 : self.ORAB,
            0xB1 : self.ORAC,
            0xC2 : self.JNZ,
            0xC3 : self.JMP,
            0xC9 : self.RET,
            0xCA : self.JZ,
            0xCD : self.CALL,
            0xD3 : self.OUT,
            0xDB : self.IN,
            0xE6 : self.ANI,
            0xEE : self.XRI,
            0xF6 : self.ORI,
            0xFA : self.JM
        }


    def program(self, program, start_address = 0):
        self.RAM.write(program, start_address)

    
    def run(self):
        self.clock.reset()

        while not self.flag["halt"]:
            self.fetch_instruction()
            self.execute_instruction()


    def reset(self):
        self.flag.clear_all()
        
        for register in self.registers:
            register.clear()

        self.clock.reset()


    def fetch_instruction(self):
        self.PC.transfer_to(self.MAR)
        self.IR.load(self.RAM, self.MAR.value)
        self.PC.inc()

        self.clock.pulse(3)


    def execute_instruction(self):
        self.OP.value = self.IR.msb(4)
        self.MAR.value = self.IR.lsb(4)

        if self.PC.value > 15 and self.OP.value != 0xF:
            raise ValueError("Invalid Program (Program Counter Overflow): SAP-1 programs must end with a HLT instruction")

        try:
            self.instruction_table[self.OP.value]()
        except KeyError as exc:
            raise ValueError(f"Invalid Opcode {self.OP.value:04b} at Memory Address {self.MAR.value}") from exc

        self.clock.pulse(3)


    # opcode execution methods


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
        print(f"{self.IO.value:08b}")


    def HLT(self):
        self.flag.set("halt")
        self.clock.stop()


    # debugging methods


    def display_state(self, start_address = 0, end_address = None):
        print('\nFlags')
        self.flag.dump()

        print('\nRegisters')
        for register in self.registers:
            register.bin_dump()

        print("\nRAM")
        self.RAM.bin_dump(start_address, end_address)


    def peek(self, address):
        return self.RAM[address]


    def poke(self, address, value):
        self.RAM[address] = value
