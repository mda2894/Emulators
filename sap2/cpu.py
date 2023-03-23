'''SAP-2 CPU - Still updating from SAP-1'''
from lib.memory import Memory
from lib.register import Register
from lib.clock import Clock
from lib.flagregister import FlagRegister

K = 1024

class CPU:
    def __init__(self, clockspeed = 1_000_000):
        '''Initialize CPU hardware'''
        
        # Memory
        self.memory = Memory(64*K)

        # Clock
        self.clock = Clock(clockspeed)

        # Registers - create register variables while appending them to self.registers list
        self.registers = []

        self.A = self.registers.append(Register("A")) or self.registers[-1] # accumulator
        self.TMP = self.registers.append(Register("TMP")) or self.registers[-1] # temp register used for ALU instructions

        self.B = self.registers.append(Register("B")) or self.registers[-1] # B & C general purpose registers
        self.C = self.registers.append(Register("C")) or self.registers[-1]

        self.PC = self.registers.append(Register("PC", 16)) or self.registers[-1] # program counter - 16 bits
        self.MAR = self.registers.append(Register("MAR", 16)) or self.registers[-1] # memory address register - 16 bits

        self.MDR = self.registers.append(Register("MDR")) or self.registers[-1] # memory data register
        self.IR = self.registers.append(Register("IR")) or self.registers[-1] # instruction register
        self.OP = self.registers.append(Register("OP")) or self.registers[-1] # operation decoder

        # IO
        self.IN1 = self.registers.append(Register("IN1")) or self.registers[-1] # input ports 1 & 2
        self.IN2 = self.registers.append(Register("IN2")) or self.registers[-1]

        self.OUT3 = self.registers.append(Register("OUT3")) or self.registers[-1] # output ports 3 & 4
        self.OUT4 = self.registers.append(Register("OUT4")) or self.registers[-1]

        # Flag Register
        self.flags = FlagRegister(
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


    '''CPU operation methods'''


    def program(self, program, start_address = 0):
        self.memory.write(program, start_address)

    
    def run(self):
        self.clock.reset()

        while not self.flags["halt"]:
            self.fetch_instruction()
            self.execute_instruction()


    def reset(self):
        self.flags.clear_all()
        
        for register in self.registers:
            register.clear()

        self.clock.reset()


    def fetch_instruction(self):
        self.PC.transfer_to(self.MAR)
        self.PC.inc()
        self.MDR.load(self.memory, self.MAR.value)
        self.MDR.transfer_to(self.IR)


    def execute_instruction(self):
        self.IR.transfer_to(self.OP)

        try:
            self.instruction_table[self.OP.value]()
        except KeyError as exc:
            raise ValueError(f"Invalid Opcode {self.OP.value:02x} at Memory Address {self.MAR.value:04x}") from exc

        self.clock.pulse(3)


    ''' debugging methods '''


    def display_state(self, start_address = 0, end_address = None):
        print('\nFlags')
        self.flags.dump()

        print('\nRegisters')
        for register in self.registers:
            register.bin_dump()

        print("\nMemory")
        self.memory.bin_dump(start_address, end_address)


    def peek(self, address):
        return self.memory[address]


    def poke(self, address, value):
        self.memory[address] = value


    ''' instruction execution methods '''


