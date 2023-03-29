'''SAP-3 CPU'''

from lib.memory import Memory
from lib.clock import Clock
from lib.registers import *
from lib.instructions import *

class CPU:
    def __init__(self, clockspeed = 1_000_000):
        '''Initialize CPU hardware'''

        self.halt = False
        
        # Memory
        self.memory = Memory(2**16)

        # Clock
        self.clock = Clock(clockspeed)

        # Registers - create register variables while appending them to self.registers list
        self.registers = []

        self.A = self.registers.append(Register("A")) or self.registers[-1] # accumulator

        self.B = self.registers.append(Register("B")) or self.registers[-1] # B & C general purpose registers
        self.C = self.registers.append(Register("C")) or self.registers[-1]
        self.BC = self.registers.append(DoubleRegister("BC", self.B, self.C)) or self.registers[-1] # BC double register

        self.D = self.registers.append(Register("D")) or self.registers[-1] # D & E general purpose registers
        self.E = self.registers.append(Register("E")) or self.registers[-1]
        self.DE = self.registers.append(DoubleRegister("DE", self.D, self.E)) or self.registers[-1] # DE double register

        self.H = self.registers.append(Register("H")) or self.registers[-1] # H & L general purpose registers
        self.L = self.registers.append(Register("L")) or self.registers[-1]
        self.HL = self.registers.append(DoubleRegister("HL", self.H, self.L)) or self.registers[-1] # HL double register

        self.F = self.registers.append(
            FlagsRegister("F", carry = 0, parity = 2, zero = 6, sign = 7)) or self.registers[-1] # flags register

        self.M = self.registers.append(PseudoRegister("M", self.memory, self.HL)) or self.registers[-1] # memory pseudo-register

        self.SP = self.registers.append(Register("SP", 16)) or self.registers[-1] # stack pointer

        self.PC = self.registers.append(Register("PC", 16)) or self.registers[-1] # program counter - 16 bits
        self.MAR = self.registers.append(Register("MAR", 16)) or self.registers[-1] # memory address register

        self.IR = self.registers.append(Register("IR")) or self.registers[-1] # instruction register

        # IO
        self.IN = self.registers.append(Register("IN")) or self.registers[-1] # input port
        self.OUT = self.registers.append(Register("OUT")) or self.registers[-1] # output port

        
    '''CPU operation methods'''


    def load(self, program, start = 0):
        self.memory.write(program, start)


    def reset(self):
        for register in self.registers:
            if not isinstance(register, PseudoRegister):
                register.clear()

        self.clock.reset()

        self.halt = False

    
    def run(self):
        while not self.halt:
            self.fetch_instruction()
            self.execute_instruction()


    '''Helper methods'''


    def fetch_instruction(self):
        self.PC.transfer_to(self.MAR)
        self.IR.load(self.memory, self.MAR.value)
        self.PC.inc()


    def execute_instruction(self):
        try:
            instruction_table[self.IR.value](self)

        except KeyError as exc:
            raise ValueError(f"Invalid Opcode {self.IR.value:02x} at Memory Address {self.MAR.value:04x}") from exc


    def fetch_byte(self):
        self.PC.transfer_to(self.MAR)
        self.MDR.load(self.memory, self.MAR.value)
        self.MDR.transfer_to(self.TMP)
        self.PC.inc()


    def fetch_address(self):
        self.PC.transfer_to(self.MAR)
        self.MDR.load(self.memory, self.MAR.value)
        self.MDR.transfer_to(self.TMP) # load lower byte of address into TMP
        self.PC.inc()
        
        self.PC.transfer_to(self.MAR)
        self.MDR.load(self.memory, self.MAR.value) # load upper byte of address into MDR
        self.PC.inc()


    def update_flags(self):
        if self.A.value == 0:
            self.F.set("zero")
        else:
            self.F.clear("zero")
        
        if self.A.msb():
            self.F.set("sign")
        else:
            self.F.clear("sign")
