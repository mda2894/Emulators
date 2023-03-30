'''Module for storing CPU instruction methods and instruction decoding table'''

# instruction methods

def ADD(cpu, register):
    cpu.A.add(register)

    cpu.update_flags()
    cpu.clock.pulse(4)

def ADDA(cpu):
    ADD(cpu, cpu.A)

def ADDB(cpu):
    ADD(cpu, cpu.B)

def ADDC(cpu):
    ADD(cpu, cpu.C)

def ADDD(cpu):
    ADD(cpu, cpu.D)

def ADDE(cpu):
    ADD(cpu, cpu.E)

def ADDH(cpu):
    ADD(cpu, cpu.H)

def ADDL(cpu):
    ADD(cpu, cpu.L)

def ADDM(cpu):
    ADD(cpu, cpu.M)

    
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

    cpu.A.and_reg(cpu.W)

    cpu.update_flags()
    cpu.clock.pulse(7)


def CALL(cpu):
    cpu.memory[0xFFFE] = cpu.PC.value # store lower byte of PC
    cpu.memory[0XFFFF] = cpu.PC.value >> 8 # store upper byte of PC

    cpu.fetch_address() # fetch subroutine address
    cpu.PC.transfer_from(cpu.WZ) # load subroutine address into PC

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
    cpu.halt = True

    cpu.clock.pulse(5)
    cpu.clock.stop()


def IN(cpu):
    cpu.A.transfer_from(cpu.IN)

    cpu.clock.update(4)
    
    
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

        cpu.PC.transfer_from(cpu.WZ)

        cpu.clock.pulse(10)

    else:
        cpu.clock.pulse(7)


def JMP(cpu):
    cpu.fetch_address()

    cpu.PC.transfer_from(cpu.WZ)

    cpu.clock.pulse(10)


def JNZ(cpu):
    if not cpu.flags["zero"]:
        cpu.fetch_address()

        cpu.PC.transfer_from(cpu.WZ)

        cpu.clock.pulse(10)

    else:
        cpu.clock.pulse(7)


def JZ(cpu):
    if cpu.flags["zero"]:
        cpu.fetch_address()

        cpu.PC.transfer_from(cpu.WZ)

        cpu.clock.pulse(10)

    else:
        cpu.clock.pulse(7)


def LDA(cpu):
    cpu.fetch_address()

    cpu.A.load(cpu.memory, cpu.WZ.value)

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

    cpu.A.or_reg(cpu.W)

    cpu.update_flags()
    cpu.clock.pulse(7)


def OUT(cpu):
    cpu.A.transfer_to(cpu.OUT)

    print(f"\n{cpu.A.value:08b} {cpu.A.value:02x}")

    cpu.clock.pulse(4)


def RAL(cpu):
    cpu.A.rol()

    cpu.clock.pulse(4)


def RAR(cpu):
    cpu.A.ror()

    cpu.clock.pulse(4)


def RET(cpu):
    cpu.W.load(cpu.memory, 0xFFFF)
    cpu.Z.load(cpu.memory, 0xFFFe)

    cpu.PC.transfer_from(cpu.WZ)

    cpu.clock.pulse(10)


def STA(cpu):
    cpu.fetch_address()

    cpu.A.store(cpu.memory, cpu.WZ.value)

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

    cpu.A.xor_reg(cpu.W)

    cpu.update_flags()
    cpu.clock.pulse(7)


# instruction table

instruction_table = {
    0x00 : NOP,
    0x01 : LXIB,
    0x02 : STAXB,
    0x03 : INXB,
    0x04 : INRB,
    0x05 : DCRB,
    0x06 : MVIB,
    0x07 : RLC,
    0x09 : DADB,
    0x0A : LDAXB,
    0x0B : DCXB,
    0x0C : INRC,
    0x0D : DCRC,
    0x0E : MVIC,
    0x0F : RRC,
    0x11 : LXID,
    0x12 : STAXD,
    0x13 : INXD,
    0x14 : INRD,
    0x15 : DCRD,
    0x16 : MVID,
    0x17 : RAL,
    0x19 : DADD,
    0x1A : LDAXD,
    0x1B : INRE,
    0x1D : DCRE,
    0x1E : MVIE,
    0x1F : RAR,
    0x21 : LXIH,
    0x22 : SHLD,
    0x23 : INXH,
    0x24 : INRH,
    0x25 : DCRH,
    0x26 : MVIH,
    0x27 : DAA,
    0x29 : DADH,
    0x2A : LHLD,
    0x2B : DCXH,
    0x2C : INRL,
    0x2D : DCRL,
    0x2E : MVIL,
    0x2F : CMA,
    0x31 : LXISP,
    0x32 : STA,
    0x33 : INXSP,
    0x34 : INRM,
    0x35 : DCRM,
    0x36 : DCRM,
    0x37 : STC,
    0x39 : DADSP,
    0x3A : LDA,
    0x3B : DCXSP,
    0x3C : INRA,
    0x3D : DCRA,
    0x3E : MVIA,
    0x3F : CMC,
    0x40 : MOVBB,
    0x41 : MOVBC,
    0x42 : MOVBD,
    0x43 : MOVBE,
    0x44 : MOVBH,
    0x45 : MOVBL,
    0x46 : MOVBM,
    0x47 : MOVBA,
    0x48 : MOVCB,
    0x49 : MOVCC,
    0x4A : MOVCD,
    0x4B : MOVCE,
    0x4C : MOVCH,
    0x4D : MOVCL,
    0x4E : MOVCM,
    0x4F : MOVCA,
    0x50 : MOVDB,
    0x51 : MOVDC,
    0x52 : MOVDD,
    0x53 : MOVDE,
    0x54 : MOVDH,
    0x55 : MOVDL,
    0x56 : MOVDM,
    0x57 : MOVDA,
    0x58 : MOVEB,
    0x59 : MOVEC,
    0x5A : MOVED,
    0x5B : MOVEE,
    0x5C : MOVEH,
    0x5D : MOVEL,
    0x5E : MOVEM,
    0x5F : MOVEA,
    0x60 : MOVHB,
    0x61 : MOVHC,
    0x62 : MOVHD,
    0x63 : MOVHE,
    0x64 : MOVHH,
    0x65 : MOVHL,
    0x66 : MOVHM,
    0x67 : MOVHA,
    0x68 : MOVLB,
    0x69 : MOVLC,
    0x6A : MOVLD,
    0x6B : MOVLE,
    0x6C : MOVLH,
    0x6D : MOVLL,
    0x6E : MOVLM,
    0x6F : MOVLA,
    0x70 : MOVMB,
    0x71 : MOVMC,
    0x72 : MOVMD,
    0x73 : MOVME,
    0x74 : MOVMH,
    0x75 : MOVML,
    0x76 : HLT,
    0x77 : MOVMA,
    0x78 : MOVAB,
    0x79 : MOVAC,
    0x7A : MOVAD,
    0x7B : MOVAE,
    0x7C : MOVAH,
    0x7D : MOVAL,
    0x7E : MOVAM,
    0x7F : MOVAA,
    0x80 : ADDB,
    0x81 : ADDC,
    0x82 : ADDD,
    0x83 : ADDE,
    0x84 : ADDH,
    0x85 : ADDL,
    0x86 : ADDM,
    0x87 : ADDA,
    0x88 : ADCB,
    0x89 : ADCC,
    0x8A : ADCD,
    0x8B : ADCE,
    0x8C : ADCH,
    0x8D : ADCL,
    0x8E : ADCM,
    0x8F : ADCA,
    0x90 : SUBB,
    0x91 : SUBC,
    0x92 : SUBD,
    0x93 : SUBE,
    0x94 : SUBH,
    0x95 : SUBL,
    0x96 : SUBM,
    0x97 : SUBA,
    0x98 : SBBB,
    0x99 : SBBC,
    0x9A : SBBD,
    0x9B : SBBE,
    0x9C : SBBH,
    0x9D : SBBL,
    0x9E : SBBM,
    0x9F : SBBA,
    0xA0 : ANAB,
    0xA1 : ANAC,
    0xA2 : ANAD,
    0xA3 : ANAE,
    0xA4 : ANAH,
    0xA5 : ANAL,
    0xA6 : ANAM,
    0xA7 : ANAA,
    0xA8 : XRAB,
    0xA9 : XRAC,
    0xAA : XRAD,
    0xAB : XRAE,
    0xAC : XRAH,
    0xAD : XRAL,
    0xAE : XRAM,
    0xAF : XRAA,
    0xB0 : ORAB,
    0xB1 : ORAC,
    0xB2 : ORAD,
    0xB3 : ORAE,
    0xB4 : ORAH,
    0xB5 : ORAL,
    0xB6 : ORAM,
    0xB7 : ORAA,
    0xB8 : CMPB,
    0xB9 : CMPC,
    0xBA : CMPD,
    0xBB : CMPE,
    0xBC : CMPH,
    0xBD : CMPL,
    0xBE : CMPM,
    0xBF : CMPA,
    0xC0 : RNZ,
    0xC1 : POPB,
    0xC2 : JNZ,
    0xC3 : JMP,
    0xC4 : CNZ,
    0xC5 : PUSHB,
    0xC6 : ADI,
    0xC7 : RST0,
    0xC8 : RZ,
    0xC9 : RET,
    0xCA : JZ,
    0xCC : CZ,
    0xCD : CALL,
    0xCE : ACI,
    0xCF : RST1,
    0xD0 : RNC,
    0xD1 : POPD,
    0xD2 : JNC,
    0xD3 : OUT,
    0xD4 : CNC,
    0xD5 : PUSHD,
    0xD6 : SUI,
    0xD7 : RST2,
    0xD8 : RC,
    0xDA : JC,
    0xDB : IN,
    0xDC : CC,
    0xDE : SBI,
    0xDF : RST3,
    0xE0 : RPO,
    0xE1 : POPH,
    0xE2 : JPO,
    0xE3 : XTHL,
    0xE4 : CPO,
    0xE5 : PUSHH,
    0xE6 : ANI,
    0xE7 : RST4,
    0xE8 : RPE,
    0xE9 : PCHL,
    0xEA : JPE,
    0xEB : XCHG,
    0xEC : CPE,
    0xEE : XRI,
    0xEF : RST5,
    0xF0 : RP,
    0xF1 : POPPSW,
    0xF2 : JP,
    0xF3 : DI,
    0xF4 : CP,
    0xF5 : PUSHPSW,
    0xF6 : ORI,
    0xF7 : RST6,
    0xF8 : RM,
    0xF9 : SPHL,
    0xFA : JM,
    0xFB : EI,
    0xFC : CM,
    0xFE : CPI,
    0xFF : RST7
}
