'''SAP-1 CPU'''
from lib.memory import Memory
from lib.register import Register
from lib.clock import Clock
from lib.flagregister import FlagRegister

class CPU:
    def __init__(self, clockspeed = 1_000_000):
        # Memory
        self.RAM = Memory(16)

        # Clock
        self.clock = Clock(clockspeed)

        # Registers
        self.A = Register("A")
        self.B = Register("B")

        self.PC = Register("PC", 4) # program counter
        self.MAR = Register("MAR", 4) # memory address register
        self.OP = Register("OP", 4) # operation decode register
        self.IR = Register("IR") # instruction register

        self.IO = Register("IO") # input/output register

        self.registers = [
            self.A,
            self.B,
            self.PC,
            self.MAR,
            self.OP,
            self.IR,
            self.IO
        ]

        # Flag Register
        self.flag = FlagRegister("Halt")

        # Instruction table
        self.instruction_table = {
            0x0 : self.LDA,
            0x1 : self.ADD,
            0x2 : self.SUB,
            0xE : self.OUT,
            0xF : self.HLT
        }


    def program(self, program, start_address = 0):
        self.RAM.write(program, start_address)

    
    def run(self):
        self.clock.reset()

        while not self.flag["Halt"]:
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
        self.flag.set("Halt")
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
