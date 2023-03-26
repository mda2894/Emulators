'''SAP-2 CPU - Still updating from SAP-1'''
from lib.memory import Memory
from lib.register import Register
from lib.clock import Clock
from lib.flagregister import FlagRegister
from lib.instructions import *

class CPU:
    def __init__(self, clockspeed = 1_000_000):
        '''Initialize CPU hardware'''
        
        # Memory
        self.memory = Memory(64*1024)

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
        self.IN = self.registers.append(Register("IN")) or self.registers[-1] # input port
        self.OUT = self.registers.append(Register("OUT")) or self.registers[-1] # output port

        # Flag Register
        self.flags = FlagRegister(
            "halt",
            "sign",
            "zero"
        )

        
    '''CPU operation methods'''


    def load(self, program, start = 0):
        self.memory.write(program, start)


    def reset(self):
        self.flags.clear_all()
        
        for register in self.registers:
            register.clear()

        self.clock.reset()

    
    def run(self, program = None, start = 0):
        if program:
            self.memory.write(program, start)

        while not self.flags["halt"]:
            self.fetch_instruction()
            self.execute_instruction()


    def step(self, program = None, start = 0, end = 256):
        if program:
            self.memory.write(program, start)

        self.display_state(start, end)

        while True:
            match input("\nEnter command: "): 
                case "":
                    if not self.flags["halt"]:
                        self.fetch_instruction()
                        self.execute_instruction()
                        self.display_state(start, end)

                    else:
                        print('\nCPU is halted. Type "reset" to start over or "exit" to exit the program.')
                
                case "exit":
                    break

                case "reset":
                    print("\nResetting computer")

                    self.reset()
                    self.step()
                    break

                case _:
                    print('\nDid not recognize command. \
                    \n  Type "reset" to start over, "exit" to exit the program, \
                    \n  or hit enter to execute the next instruction.')

    
    def program_mode(self):
        print('\nManual Program Mode')
        self.display_program_help()

        current = self.get_address_from_user()

        while True:
            match (cmd := input(f"\n{(current):04x}: ")):
                case "view":
                    self.memory.hex_dump()

                case "cpu":
                    self.display_state()
                
                case "restart":
                    self.memory.clear()

                    current = self.get_address_from_user()
                
                case "run":
                    self.reset()

                    try:
                        self.run()

                    except:
                        self.display_program_error()
                
                case "step":
                    self.reset()

                    try:
                        self.step()

                    except:
                        self.display_program_error()
               
                case "exit":
                    break

                case "help":
                    self.display_program_help()

                case "jump":
                    current = self.get_address_from_user()

                case _:
                    if current <= 0xFFFF:
                        try:
                            self.IN.value = int(cmd, base = 16)
                            self.MAR.value = current
                            self.IN.store(self.memory, current)

                            current += 1

                        except:
                            print('\nInvalid Input: type "help" for information on accepted inputs.')

                    else:
                        print("\nEnd of memory. Jump somewhere else in memory to continue programming.")
   

    '''Helper methods'''


    def fetch_instruction(self):
        self.PC.transfer_to(self.MAR)
        self.MDR.load(self.memory, self.MAR.value)
        self.MDR.transfer_to(self.IR)
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
        self.TMP.load(self.memory, self.PC.value) # load lower byte of address into TMP
        self.PC.inc()
        
        self.MDR.load(self.memory, self.PC.value) # load upper byte of address into MDR
        self.PC.inc()


    def update_flags(self):
        if self.A.value == 0:
            self.flags.set("zero")
        else:
            self.flags.clear("zero")
        
        if self.A.msb():
            self.flags.set("sign")
        else:
            self.flags.clear("sign")


    def display_state(self, start = 0, end = None):
        print('\nFlags')
        self.flags.dump()

        print('\nRegisters\n')
        for register in self.registers:
            register.hex_dump()

        print("\nMemory")
        self.memory.hex_dump(start, end)


    def get_address_from_user(self):
        address = -1
        
        while address < 0:
            try:
                address = int(input("\nEnter address (hex 0000 - FFFF): "), 16)
            except:
                print("\nInvalid memory address")
                continue

            if not (0x0000 <= address <= self.memory.size - 1):
                address = -1
                print("\nInvalid memory address")

        return address


    def display_program_help(self):
        print('\nPlease enter program as hex bytes (00 - FF). Type: \
        \n  "view" to view the program you have entered \
        \n  "cpu" to view the current state of your CPU \
        \n  "restart" to restart your program from the beginning \
        \n  "run" to run the program from start to finish \
        \n  "step" to run the program step by step \
        \n  "exit" to exit the program \
        \n  "jump" to jump to a particular line and edit your program from there \
        \n  "help" to repeat this message')


    def display_program_error(self):
        print('\nThere was an error while running your program. \
        \n  Type "cpu" to view the state of your CPU when it failed.')
