'''SAP-2 CPU - Still updating from SAP-1'''
from lib.memory import Memory
from lib.register import Register
from lib.clock import Clock
from lib.flagregister import FlagRegister
from lib.instructions import *

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
        self.TMP = self.registers.append(Register("TMP")) or self.registers[-1] # TMP register for ALU operations

        self.B = self.registers.append(Register("B")) or self.registers[-1] # B & C general purpose registers
        self.C = self.registers.append(Register("C")) or self.registers[-1]

        self.PC = self.registers.append(Register("PC", 16)) or self.registers[-1] # program counter - 16 bits
        self.MAR = self.registers.append(Register("MAR", 16)) or self.registers[-1] # memory address register - 16 bits
        self.MDR = self.registers.append(Register("MDR")) or self.registers[-1] # memory data register

        self.IR = self.registers.append(Register("IR")) or self.registers[-1] # instruction register

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

        
    '''CPU operation methods'''


    def program(self, program, start_address = 0):
        self.memory.write(program, start_address)


    def reset(self):
        self.flags.clear_all()
        
        for register in self.registers:
            register.clear()

        self.clock.reset()

    
    def run(self):
        while not self.flags["halt"]:
            self.fetch_instruction()
            self.execute_instruction()


    def fetch_instruction(self):
        self.PC.transfer_to(self.MAR)
        self.MDR.load(self.memory, self.MAR.value)
        self.MDR.transfer_to(self.IR)
        self.PC.inc()


    def fetch_byte(self):
        self.PC.transfer_to(self.MAR)
        self.MDR.load(self.memory, self.MAR.value)
        self.MDR.transfer_to(self.TMP)
        self.PC.inc()


    def fetch_address(self):
        self.TMP.load(self.memory, self.PC.value) # load lower byte of address into TMP
        self.PC.inc()
        
        self.MDR.load(self.memory, self.PC.value) # load upper byte of address into MDR
        self.PC.inc()


    def execute_instruction(self):
        try:
            instruction_table[self.IR.value](self)

        except KeyError as exc:
            raise ValueError(f"Invalid Opcode {self.IR.value:02x} at Memory Address {self.MAR.value:04x}") from exc


    def update_flags(self):
        if self.A.value == 0:
            self.flags.set("zero")
        else:
            self.flags.clear("zero")
        
        if self.A.msb():
            self.flags.set("sign")
        else:
            self.flags.clear("sign")


    def display_state(self, start_address = 0, end_address = None):
        print('\nFlags')
        self.flags.dump()

        print('\nRegisters')
        for register in self.registers:
            register.hex_dump()

        print("\nMemory")
        self.memory.hex_dump(start_address, end_address)


    def step(self, start = 0, end = 256):
        self.display_state(start, end)

        while True:
            match input("\nEnter command: "): 
                case "":
                    if not self.flags["halt"]:
                        self.fetch_instruction()
                        self.execute_instruction()
                        self.display_state(start, end)

                    else:
                        print('\nCPU is halted. Type "reset" to start over or "stop" to end the program.')
                
                case "stop":
                    break

                case "reset":
                    print("\nResetting computer")

                    self.reset()
                    self.step()
                    break

                case _:
                    print('\nDid not recognize command. \
                    \nType "reset" to start over, "stop" to end the program, or just hit enter to execute the next instruction.')
