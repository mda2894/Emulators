'''SAP-3 CPU'''

from lib.memory import Memory
from lib.clock import Clock
from lib.registers import *
from lib.instructions import *

class CPU:
    '''Main CPU class for managing the hardware of the SAP-3 CPU'''

    def __init__(self, clockspeed = 1_000_000):
        '''Initialize CPU hardware'''

        # Unofficial "halt" flag
        self.halt = False
        
        # Memory
        self.memory = Memory(2**16)

        # Clock
        self.clock = Clock(clockspeed)

        # Registers - create register variables while appending them to self.registers list

        self.registers = []

        # Accumulator
        self.A = self.registers.append(Register("A")) or self.registers[-1]

        # B & C general purpose registers
        self.B = self.registers.append(Register("B")) or self.registers[-1]
        self.C = self.registers.append(Register("C")) or self.registers[-1]

        # BC double register
        self.BC = self.registers.append(DoubleRegister("BC", self.B, self.C)) or self.registers[-1]

        # D & E general purpose registers
        self.D = self.registers.append(Register("D")) or self.registers[-1]
        self.E = self.registers.append(Register("E")) or self.registers[-1]

        # DE double register
        self.DE = self.registers.append(DoubleRegister("DE", self.D, self.E)) or self.registers[-1]

        # H & L general purpose registers
        self.H = self.registers.append(Register("H")) or self.registers[-1]
        self.L = self.registers.append(Register("L")) or self.registers[-1]

        # HL double register
        self.HL = self.registers.append(DoubleRegister("HL", self.H, self.L)) or self.registers[-1]

        # W & Z internal registers - not directly accessible to user
        self.W = self.registers.append(Register("W")) or self.registers[-1]
        self.Z = self.registers.append(Register("Z")) or self.registers[-1]

        # WZ double register
        self.WZ = self.registers.append(DoubleRegister("WZ", self.W, self.Z)) or self.registers[-1]

        # Flags register
        self.F = self.registers.append(FlagsRegister("F", carry = 0, parity = 2, zero = 6, sign = 7)) or self.registers[-1]

        # M pseudo-register
        self.M = self.registers.append(PseudoRegister("M", self.memory, self.HL)) or self.registers[-1]

        # Stack pointer
        self.SP = self.registers.append(Register("SP", 16)) or self.registers[-1]

        # Program counter - 16 bits
        self.PC = self.registers.append(Register("PC", 16)) or self.registers[-1]

        # Instruction register
        self.IR = self.registers.append(Register("IR")) or self.registers[-1]

        
    '''CPU operation methods'''


    def load(self, program, start = 0):
        '''Load a program from either a list or an external file'''
        self.memory.write(program, start)


    def reset(self):
        '''Reset the CPU, including all flags and registers, and the clock - leaves memory as is'''

        for register in self.registers:
            if not isinstance(register, PseudoRegister):
                register.clear()

        self.clock.reset()

        self.halt = False

    
    def run(self):
        '''Run the program in memory (from address 0) until a HLT command is executed'''

        while not self.halt:
            self.fetch_instruction()
            self.execute_instruction()


    '''Helper methods'''


    def fetch_instruction(self):
        '''Fetch the next instruction and load it into the IR'''

        self.IR.load(self.memory, self.PC.value)
        self.PC.inc()


    def execute_instruction(self):
        '''Execute the instruction in the IR, using instructions.instruction_table'''

        try:
            instruction_table[self.IR.value](self)

        except KeyError as exc:
            raise ValueError(f"Invalid Opcode {self.IR.value:02x} at Memory Address {self.PC.value - 1:04x}") from exc


    def fetch_byte(self):
        '''Fetch the next byte of data from memory - store in W'''

        self.W.load(self.memory, self.PC.value)
        self.PC.inc()


    def fetch_address(self):
        '''Fetch address from next two bytes - store in WZ'''

        self.Z.load(self.memory, self.PC.value) # load lower byte into Z
        self.PC.inc()
        
        self.W.load(self.memory, self.PC.value) # load upper byte into W
        self.PC.inc()


    def update_flags(self, *flags):
        '''No arguments for all, "abc" for all but carry, otherwise list the specific flags'''
        if not flags:
            zero = sign = carry = parity = True
        elif "abc" in flags:
            zero = sign = parity = True
            carry = False
        else:
            zero = "zero" in flags
            sign = "sign" in flags
            carry = "carry" in flags
            parity = "parity" in flags

        if zero:
            self.F.flags["zero"] = self.A.value == 0

        if sign:
            self.F.flags["sign"] = self.A.msb()

        if carry:
            self.F.flags["carry"] = self.A.carry

        if parity:
            n = self.A.value
            n ^= n >> 4
            n ^= n >> 2
            n ^= n >> 1

            self.F.flags["parity"] = n & 1 == 0
