'''Module for storing CPU instruction methods and instruction decoding table'''

# instruction methods

def ADDB(cpu):
    cpu.A.add(cpu.B)

    cpu.update_flags()
    cpu.clock.pulse(4)


def ADDC(cpu):
    cpu.A.add(cpu.C)

    cpu.update_flags()
    cpu.clock.pulse(4)

    
def ANAB(cpu):
    cpu.A.and_reg(cpu.B)

    cpu.update_flags()
    cpu.clock.pulse(4)


def ANAC(cpu):
    cpu.A.and_reg(cpu.C)

    cpu.update_flags()
    cpu.clock.pulse(4)


def ANI(cpu):
    cpu.fetch_byte()

    cpu.A.and_reg(cpu.TMP)

    cpu.update_flags()
    cpu.clock.pulse(7)


def CALL(cpu):
    cpu.memory[0xFFFE] = cpu.PC.value # store lower byte of PC
    cpu.memory[0XFFFF] = cpu.PC.value >> 8 # store upper byte of PC

    cpu.fetch_address() # fetch subroutine address
    cpu.PC.value = cpu.MDR.value << 8 | cpu.TMP.value # load subroutine address into PC

    cpu.clock.pulse(18)


def CMA(cpu):
    cpu.A.comp()

    cpu.clock.pulse(4)


def DCRA(cpu):
    cpu.A.dec()

    cpu.update_flags()
    cpu.clock.pulse(4)


def DCRB(cpu):
    cpu.B.dec()

    cpu.update_flags()
    cpu.clock.pulse(4)


def DCRC(cpu):
    cpu.C.dec()

    cpu.update_flags()
    cpu.clock.pulse(4)


def HLT(cpu):
    cpu.flags.set("halt")

    cpu.clock.pulse(5)
    cpu.clock.stop()


def IN(cpu):
    cpu.fetch_byte()

    if cpu.TMP.value == 1:
        cpu.A.transfer_from(cpu.IN1)

    elif cpu.TMP.value == 2:
        cpu.A.transfer_from(cpu.IN2)
            
    else:
        raise ValueError(f"Invalid Input Port: {cpu.TMP.value}")

    cpu.clock.update(10)
    
    
def INRA(cpu):
    cpu.A.inc()

    cpu.update_flags()
    cpu.clock.pulse(4)


def INRB(cpu):
    cpu.B.inc()

    cpu.update_flags()
    cpu.clock.pulse(4)


def INRC(cpu):
    cpu.C.inc()

    cpu.update_flags()
    cpu.clock.pulse(4)


def JM(cpu):
    if cpu.flags["sign"]:
        cpu.fetch_address()

        cpu.PC.value = cpu.MDR.value << 8 | cpu.TMP.value

        cpu.clock.pulse(10)

    else:
        cpu.clock.pulse(7)


def JMP(cpu):
    cpu.fetch_address()

    cpu.PC.value = cpu.MDR.value << 8 | cpu.TMP.value

    cpu.clock.pulse(10)


def JNZ(cpu):
    if not cpu.flags["zero"]:
        cpu.fetch_address()

        cpu.PC.value = cpu.MDR.value << 8 | cpu.TMP.value

        cpu.clock.pulse(10)

    else:
        cpu.clock.pulse(7)


def JZ(cpu):
    if cpu.flags["zero"]:
        cpu.fetch_address()

        cpu.PC.value = cpu.MDR.value << 8 | cpu.TMP.value

        cpu.clock.pulse(10)

    else:
        cpu.clock.pulse(7)


def LDA(cpu):
    cpu.fetch_address()

    cpu.MAR.value = cpu.MDR.value << 8 | cpu.TMP.value
    cpu.A.load(cpu.memory, cpu.MAR.value)

    cpu.clock.pulse(13)


def MOVAB(cpu):
    cpu.B.transfer_to(cpu.A)

    cpu.clock.pulse(4)


def MOVAC(cpu):
    cpu.C.transfer_to(cpu.A)

    cpu.clock.pulse(4)


def MOVBA(cpu):
    cpu.A.transfer_to(cpu.B)

    cpu.clock.pulse(4)


def MOVBC(cpu):
    cpu.C.transfer_to(cpu.B)

    cpu.clock.pulse(4)


def MOVCA(cpu):
    cpu.A.transfer_to(cpu.C)

    cpu.clock.pulse(4)


def MOVCB(cpu):
    cpu.B.transfer_to(cpu.C)

    cpu.clock.pulse(4)


def MVIA(cpu):
    cpu.fetch_byte()

    cpu.TMP.transfer_to(cpu.A)

    cpu.clock.pulse(7)


def MVIB(cpu):
    cpu.fetch_byte()

    cpu.TMP.transfer_to(cpu.B)

    cpu.clock.pulse(7)


def MVIC(cpu):
    cpu.fetch_byte()

    cpu.TMP.transfer_to(cpu.C)

    cpu.clock.pulse(7)


def NOP(cpu):
    cpu.clock.pulse(4)


def ORAB(cpu):
    cpu.A.or_reg(cpu.B)

    cpu.update_flags()
    cpu.clock.pulse(4)


def ORAC(cpu):
    cpu.A.or_reg(cpu.C)

    cpu.update_flags()
    cpu.clock.pulse(4)


def ORI(cpu):
    cpu.fetch_byte()

    cpu.A.or_reg(cpu.TMP)

    cpu.update_flags()
    cpu.clock.pulse(7)


def OUT(cpu):
    cpu.fetch_byte()

    if cpu.TMP.value == 3:
        cpu.A.transfer_to(cpu.OUT3)

    elif cpu.TMP.value == 4:
        cpu.A.transfer_to(cpu.OUT4)

    else:
        raise ValueError(f"Invalid Output Port: {cpu.TMP.value}")

    print(f"{cpu.A.value:08b}")

    cpu.clock.pulse(10)


def RAL(cpu):
    cpu.A.rol()

    cpu.clock.pulse(4)


def RAR(cpu):
    cpu.A.ror()

    cpu.clock.pulse(4)


def RET(cpu):
    cpu.PC.value = cpu.memory[0xFFFF] << 8 | cpu.memory[0xFFFE]

    cpu.clock.pulse(10)


def STA(cpu):
    cpu.fetch_address()

    cpu.MAR.value = cpu.MDR.value << 8 | cpu.TMP.value
    cpu.A.store(cpu.memory, cpu.MAR.value)

    cpu.clock.pulse(13)


def SUBB(cpu):
    cpu.A.sub(cpu.B)

    cpu.update_flags()
    cpu.clock.pulse(4)


def SUBC(cpu):
    cpu.A.sub(cpu.C)

    cpu.update_flags()
    cpu.clock.pulse(4)


def XRAB(cpu):
    cpu.A.xor_reg(cpu.B)

    cpu.update_flags()
    cpu.clock.pulse(4)


def XRAC(cpu):
    cpu.A.xor_reg(cpu.C)

    cpu.update_flags()
    cpu.clock.pulse(4)


def XRI(cpu):
    cpu.fetch_byte()

    cpu.A.xor_reg(cpu.TMP)

    cpu.update_flags()
    cpu.clock.pulse(7)


# instruction table

instruction_table = {
    0x00 : NOP,
    0x04 : INRB,
    0x05 : DCRB,
    0x06 : MVIB,
    0x0C : INRC,
    0x0D : DCRC,
    0x0E : MVIC,
    0x17 : RAL,
    0x1F : RAR,
    0x2F : CMA,
    0x32 : STA,
    0x3A : LDA,
    0x3C : INRA,
    0x3D : DCRA,
    0x3E : MVIA,
    0x41 : MOVBC,
    0x47 : MOVBA,
    0x48 : MOVCB,
    0x4F : MOVCA,
    0x76 : HLT,
    0x78 : MOVAB,
    0x79 : MOVAC,
    0x80 : ADDB,
    0x81 : ADDC,
    0x90 : SUBB,
    0x91 : SUBC,
    0xA0 : ANAB,
    0xA1 : ANAC,
    0xA8 : XRAB,
    0xA9 : XRAC,
    0xB0 : ORAB,
    0xB1 : ORAC,
    0xC2 : JNZ,
    0xC3 : JMP,
    0xC9 : RET,
    0xCA : JZ,
    0xCD : CALL,
    0xD3 : OUT,
    0xDB : IN,
    0xE6 : ANI,
    0xEE : XRI,
    0xF6 : ORI,
    0xFA : JM
}