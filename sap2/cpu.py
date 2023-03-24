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


    def reset(self):
        self.flags.clear_all()
        
        for register in self.registers:
            register.clear()

        self.clock.reset()

    
    def run(self):
        self.clock.reset()

        while not self.flags["halt"]:
            self.fetch_instruction()
            self.execute_instruction()


    def fetch_instruction(self):
        self.IR.load(self.memory, self.PC.value)
        self.PC.inc()


    def fetch_byte(self):
        self.TMP.load(self.memory, self.PC.value) # load byte into TMP
        self.PC.inc()


    def fetch_address(self):
        self.TMP.load(self.memory, self.PC.value) # load lower byte of address into TMP
        self.PC.inc()
        
        self.MDR.load(self.memory, self.PC.value) # load upper byte of address into MDR
        self.PC.inc()

    def execute_instruction(self):
        try:
            self.instruction_table[self.IR.value]()
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


    '''debugging methods'''


    def display_state(self, start_address = 0, end_address = None):
        print('\nFlags')
        self.flags.dump()

        print('\nRegisters')
        for register in self.registers:
            register.bin_dump()

        print("\nMemory")
        self.memory.bin_dump(start_address, end_address)


    '''instruction execution methods'''


    def ADDB(self):
        self.A.add(self.B)

        self.update_flags()
        self.clock.pulse(4)


    def ADDC(self):
        self.A.add(self.C)

        self.update_flags()
        self.clock.pulse(4)

    
    def ANAB(self):
        self.A.and_reg(B)

        self.update_flags()
        self.clock.pulse(4)


    def ANAC(self):
        self.A.and_reg(C)

        self.update_flags()
        self.clock.pulse(4)


    def ANI(self):
        self.fetch_byte()

        self.A.and_reg(self.TMP)

        self.update_flags()
        self.clock.pulse(7)


    def CALL(self):
        self.memory[0xFFFE] = self.PC.value # store lower byte of PC
        self.memory[0XFFFF] = self.PC.value >> 8 # store upper byte of PC

        self.fetch_address() # fetch subroutine address
        self.PC.value = self.MDR.value << 8 | self.TMP.value # load subroutine address into PC

        self.clock.pulse(18)


    def CMA(self):
        self.A.comp()

        self.clock.pulse(4)


    def DCRA(self):
        self.A.dec()

        self.update_flags()
        self.clock.pulse(4)


    def DCRB(self):
        self.B.dec()

        self.update_flags()
        self.clock.pulse(4)


    def DCRC(self):
        self.C.dec()

        self.update_flags()
        self.clock.pulse(4)


    def HLT(self):
        self.flags.set("halt")

        self.clock.pulse(5)
        self.clock.stop()


    def IN(self):
        self.fetch_byte()

        if self.TMP.value == 1:
            self.A.transfer_from(self.IN1)

        elif self.TMP.value == 2:
            self.A.transfer_from(self.IN2)
            
        else:
            raise ValueError(f"Invalid Input Port: {self.TMP.value}")

        self.clock.update(10)
    
    
    def INRA(self):
        self.A.inc()

        self.update_flags()
        self.clock.pulse(4)


    def INRB(self):
        self.B.inc()

        self.update_flags()
        self.clock.pulse(4)


    def INRC(self):
        self.C.inc()

        self.update_flags()
        self.clock.pulse(4)


    def JM(self):
        if self.flags["sign"]:
            self.fetch_address()

            self.PC.value = self.MDR.value << 8 | self.TMP.value

            self.clock.pulse(10)

        else:
            self.clock.pulse(7)


    def JMP(self):
        self.fetch_address()

        self.PC.value = self.MDR.value << 8 | self.TMP.value

        self.clock.pulse(10)


    def JNZ(self):
        if not self.flags["zero"]:
            self.fetch_address()

            self.PC.value = self.MDR.value << 8 | self.TMP.value

            self.clock.pulse(10)

        else:
            self.clock.pulse(7)


    def JZ(self):
        if self.flags["zero"]:
            self.fetch_address()

            self.PC.value = self.MDR.value << 8 | self.TMP.value

            self.clock.pulse(10)

        else:
            self.clock.pulse(7)


    def LDA(self):
        self.fetch_address()

        self.MAR.value = self.MDR.value << 8 | self.TMP.value
        self.A.load(self.memory, self.MAR.value)

        self.clock.pulse(13)


    def MOVAB(self):
        self.B.transfer_to(self.A)

        self.clock.pulse(4)


    def MOVAC(self):
        self.C.transfer_to(self.A)

        self.clock.pulse(4)


    def MOVBA(self):
        self.A.transfer_to(self.B)

        self.clock.pulse(4)


    def MOVBC(self):
        self.C.transfer_to(self.B)

        self.clock.pulse(4)


    def MOVCA(self):
        self.A.transfer_to(self.C)

        self.clock.pulse(4)


    def MOVCB(self):
        self.B.transfer_to(self.C)

        self.clock.pulse(4)


    def MVIA(self):
        self.fetch_byte()

        self.TMP.transfer_to(self.A)

        self.clock.pulse(7)


    def MVIB(self):
        self.fetch_byte()

        self.TMP.transfer_to(self.B)

        self.clock.pulse(7)


    def MVIC(self):
        self.fetch_byte()

        self.TMP.transfer_to(self.C)

        self.clock.pulse(7)


    def NOP(self):
        self.clock.pulse(4)


    def ORAB(self):
        self.A.or_reg(self.B)

        self.update_flags()
        self.clock.pulse(4)


    def ORAC(self):
        self.A.or_reg(self.C)

        self.update_flags()
        self.clock.pulse(4)


    def ORI(self):
        self.fetch_byte()

        self.A.or_reg(self.TMP)

        self.update_flags()
        self.clock.pulse(7)


    def OUT(self):
        self.fetch_byte()

        if self.TMP.value == 3:
            self.A.transfer_to(self.OUT3)

        elif self.TMP.value == 4:
            self.A.transfer_to(self.OUT4)

        else:
            raise ValueError(f"Invalid Output Port: {self.TMP.value}")

        self.clock.update(10)


    def RAL(self):
        self.A.rol()

        self.clock.pulse(4)


    def RAR(self):
        self.A.ror()

        self.clock.pulse(4)


    def RET(self):
        self.PC.value = self.memory[0xFFFF] << 8 | self.memory[0xFFFE]

        self.clock.pulse(10)


    def STA(self):
        self.fetch_address()

        self.MAR.value = self.MDR.value << 8 | self.TMP.value
        self.A.store(self.memory, self.MAR.value)

        self.clock.pulse(13)


    def SUBB(self):
        self.A.sub(self.B)

        self.update_flags()
        self.clock.pulse(4)


    def SUBC(self):
        self.A.sub(self.C)

        self.update_flags()
        self.clock.pulse(4)


    def XRAB(self):
        self.A.xor_reg(self.B)

        self.update_flags()
        self.clock.pulse(4)


    def XRAC(self):
        self.A.xor_reg(self.C)

        self.update_flags()
        self.clock.pulse(4)


    def XRI(self):
        self.fetch_byte()

        self.A.xor_reg(self.TMP)

        self.update_flags()
        self.clock.pulse(7)