'''Module for storing CPU instruction methods and instruction decoding table'''

# instruction methods

# UPDATE FLAGS
# CHECK CLOCK TIMINGS


def ACI(cpu):
    cpu.fetch_byte()
    cpu.A.value += cpu.Z.value + cpu.flags["carry"]
    cpu.update_flags()
    cpu.clock.pulse(7)


def ADC(cpu, register):
    cpu.A.value += register.value + cpu.flags["carry"]
    cpu.update_flags()
    cpu.clock.pulse(4)

def ADCA(cpu):
    ADC(cpu, cpu.A)

def ADCB(cpu):
    ADC(cpu, cpu.B)

def ADCC(cpu):
    ADC(cpu, cpu.C)

def ADCD(cpu):
    ADC(cpu, cpu.D)

def ADCE(cpu):
    ADC(cpu, cpu.E)

def ADCH(cpu):
    ADC(cpu, cpu.H)

def ADCL(cpu):
    ADC(cpu, cpu.L)

def ADCM(cpu):
    cpu.A.value += cpu.M.value + cpu.flags["carry"]
    cpu.update_flags()
    cpu.clock.pulse(7)


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
    cpu.A.add(cpu.M)
    cpu.update_flags()
    cpu.clock.pulse(7)


def ADI(cpu):
    cpu.fetch_byte()
    cpu.A.add(cpu.Z)
    cpu.update_flags()
    cpu.clock.pulse(7)


def ANA(cpu, register):
    cpu.A.and_reg(register)
    cpu.update_flags()
    cpu.clock.pulse(4)

def ANAA(cpu):
    ANA(cpu, cpu.A)
    
def ANAB(cpu):
    ANA(cpu, cpu.B)

def ANAC(cpu):
    ANA(cpu, cpu.C)

def ANAD(cpu):
    ANA(cpu, cpu.D)

def ANAE(cpu):
    ANA(cpu, cpu.E)

def ANAH(cpu):
    ANA(cpu, cpu.H)

def ANAL(cpu):
    ANA(cpu, cpu.L)

def ANAM(cpu):
    cpu.A.and_reg(cpu.M)
    cpu.update_flags()
    cpu.clock.pulse(7)


def ANI(cpu):
    cpu.fetch_byte()
    cpu.A.and_reg(cpu.Z)
    cpu.update_flags()
    cpu.clock.pulse(7)


def CALL(cpu):
    cpu.memory[cpu.SP.value] = cpu.PC.msb(8)
    cpu.SP.dec()
    cpu.memory[cpu.SP.value] = cpu.PC.lsb(8)
    cpu.SP.dec()

    cpu.fetch_address()
    cpu.PC.transfer_from(cpu.WZ)
    cpu.clock.pulse(18)


def CC(cpu):
    if cpu.flags["carry"]:
        CALL(cpu)
    else:
        cpu.PC.inc(2)
        cpu.clock_pulse(9)


def CM(cpu):
    if cpu.flags["sign"]:
        CALL(cpu)
    else:
        cpu.PC.inc(2)
        cpu.clock_pulse(9)


def CMA(cpu):
    cpu.A.comp()
    cpu.clock.pulse(4)


def CMC(cpu):
    cpu.flags.toggle_flag("carry")
    cpu.clock.pulse(4)


def CMP(cpu, register):
    cpu.A.transfer_to(cpu.TMP)
    cpu.TMP.sub(register)
    cpu.update_flags(cpu.TMP)
    cpu.clock.pulse(4)

def CMPA(cpu):
    CMP(cpu, cpu.A)

def CMPB(cpu):
    CMP(cpu, cpu.B)

def CMPC(cpu):
    CMP(cpu, cpu.C)

def CMPD(cpu):
    CMP(cpu, cpu.D)

def CMPE(cpu):
    CMP(cpu, cpu.E)

def CMPH(cpu):
    CMP(cpu, cpu.H)

def CMPL(cpu):
    CMP(cpu, cpu.L)

def CMPM(cpu):
    cpu.A.transfer_to(cpu.TMP)
    cpu.TMP.sub(cpu.M)
    cpu.update_flags(cpu.TMP)
    cpu.clock.pulse(7)


def CNC(cpu):
    if not cpu.flags["carry"]:
        CALL(cpu)
    else:
        cpu.PC.inc(2)
        cpu.clock_pulse(9)


def CNZ(cpu):
    if not cpu.flags["zero"]:
        CALL(cpu)
    else:
        cpu.PC.inc(2)
        cpu.clock_pulse(9)


def CP(cpu):
    if not cpu.flags["sign"]:
        CALL(cpu)
    else:
        cpu.PC.inc(2)
        cpu.clock_pulse(9)


def CPE(cpu):
    if cpu.flags["parity"]:
        CALL(cpu)
    else:
        cpu.PC.inc(2)
        cpu.clock_pulse(9)


def CPI(cpu):
    cpu.fetch_byte()
    cpu.A.transfer_to(cpu.TMP)
    cpu.TMP.sub(cpu.Z)
    cpu.update_flags(cpu.TMP)
    cpu.clock.pulse(7)


def CPO(cpu):
    if not cpu.flags["parity"]:
        CALL(cpu)
    else:
        cpu.PC.inc(2)
        cpu.clock_pulse(9)


def CZ(cpu):
    if cpu.flags["zero"]:
        CALL(cpu)
    else:
        cpu.PC.inc(2)
        cpu.clock_pulse(9)


def DCR(cpu, register):
    register.dec()
    cpu.update_flags(register, "abc")
    cpu.clock.pulse(4)

def DCRA(cpu):
    DCR(cpu, cpu.A)

def DCRB(cpu):
    DCR(cpu, cpu.B)

def DCRC(cpu):
    DCR(cpu, cpu.C)

def DCRD(cpu):
    DCR(cpu, cpu.D)

def DCRE(cpu):
    DCR(cpu, cpu.E)

def DCRH(cpu):
    DCR(cpu, cpu.H)

def DCRL(cpu):
    DCR(cpu, cpu.L)

def DCRM(cpu):
    cpu.M.dec()
    cpu.update_flags(cpu.M, "abc")
    cpu.clock.pulse(10)


def HLT(cpu):
    cpu.halt = True
    cpu.clock.pulse(5)
    cpu.clock.stop()


def IN(cpu):
    cpu.PC.inc()
    cpu.A.transfer_from(cpu.IN)
    cpu.clock.update(10)
    
    
def INR(cpu, register):
    register.inc()
    cpu.update_flags(register, "abc")
    cpu.clock.pulse(4)

def INRA(cpu):
    INR(cpu, cpu.A)

def INRB(cpu):
    INR(cpu, cpu.B)

def INRC(cpu):
    INR(cpu, cpu.C)

def INRD(cpu):
    INR(cpu, cpu.D)

def INRE(cpu):
    INR(cpu, cpu.E)

def INRH(cpu):
    INR(cpu, cpu.H)

def INRL(cpu):
    INR(cpu, cpu.L)

def INRM(cpu):
    cpu.M.inc()
    cpu.update_flags(cpu.M, "abc")
    cpu.clock.pulse(10)


def JC(cpu):
    if cpu.flags["carry"]:
        JMP(cpu)
    else:
        cpu.PC.inc(2)
        cpu.clock.pulse(7)


def JM(cpu):
    if cpu.flags["sign"]:
        JMP(cpu)
    else:
        cpu.PC.inc(2)
        cpu.clock.pulse(7)


def JMP(cpu):
    cpu.fetch_address()
    cpu.PC.transfer_from(cpu.WZ)
    cpu.clock.pulse(10)


def JNC(cpu):
    if not cpu.flags["carry"]:
        JMP(cpu)
    else:
        cpu.PC.inc(2)
        cpu.clock.pulse(7)


def JNZ(cpu):
    if not cpu.flags["zero"]:
        JMP(cpu)
    else:
        cpu.PC.inc(2)
        cpu.clock.pulse(7)


def JP(cpu):
    if not cpu.flags["sign"]:
        JMP(cpu)
    else:
        cpu.PC.inc(2)
        cpu.clock.pulse(7)


def JPE(cpu):
    if cpu.flags["parity"]:
        JMP(cpu)
    else:
        cpu.PC.inc(2)
        cpu.clock.pulse(7)


def JPO(cpu):
    if not cpu.flags["parity"]:
        JMP(cpu)
    else:
        cpu.PC.inc(2)
        cpu.clock.pulse(7)


def JZ(cpu):
    if cpu.flags["zero"]:
        JMP(cpu)
    else:
        cpu.PC.inc(2)
        cpu.clock.pulse(7)


def LDA(cpu):
    cpu.fetch_address()
    cpu.A.load(cpu.memory, cpu.WZ.value)
    cpu.clock.pulse(13)


def MOV(cpu, reg1, reg2):
    reg1.transfer_from(reg2)
    cpu.clock.pulse(4)

def MOVAA(cpu):
    NOP(cpu)

def MOVAB(cpu):
    MOV(cpu, cpu.A, cpu.B)
    
def MOVAC(cpu):
    MOV(cpu, cpu.A, cpu.C)

def MOVAD(cpu):
    MOV(cpu, cpu.A, cpu.D)

def MOVAE(cpu):
    MOV(cpu, cpu.A, cpu.E)

def MOVAH(cpu):
    MOV(cpu, cpu.A, cpu.H)

def MOVAL(cpu):
    MOV(cpu, cpu.A, cpu.L)

def MOVAM(cpu):
    cpu.A.transfer_from(cpu.M)
    cpu.clock.pulse(7)

def MOVBA(cpu):
    MOV(cpu, cpu.B, cpu.A)

def MOVBB(cpu):
    NOP(cpu)

def MOVBC(cpu):
    MOV(cpu, cpu.B, cpu.C)

def MOVBD(cpu):
    MOV(cpu, cpu.B, cpu.D)

def MOVBE(cpu):
    MOV(cpu, cpu.B, cpu.E)

def MOVBH(cpu):
    MOV(cpu, cpu.B, cpu.H)

def MOVBL(cpu):
    MOV(cpu, cpu.B, cpu.L)

def MOVBM(cpu):
    cpu.B.transfer_from(cpu.M)
    cpu.clock.pulse(7)

def MOVCA(cpu):
    MOV(cpu, cpu.C, cpu.A)

def MOVCB(cpu):
    MOV(cpu, cpu.C, cpu.B)

def MOVCC(cpu):
    NOP(cpu)

def MOVCD(cpu):
    MOV(cpu, cpu.C, cpu.D)

def MOVCE(cpu):
    MOV(cpu, cpu.C, cpu.E)

def MOVCH(cpu):
    MOV(cpu, cpu.C, cpu.H)

def MOVCL(cpu):
    MOV(cpu, cpu.C, cpu.L)

def MOVCM(cpu):
    cpu.C.transfer_from(cpu.M)
    cpu.clock.pulse(7)

def MOVDA(cpu):
    MOV(cpu, cpu.D, cpu.A)

def MOVDB(cpu):
    MOV(cpu, cpu.D, cpu.B)

def MOVDC(cpu):
    MOV(cpu, cpu.D, cpu.C)

def MOVDD(cpu):
    NOP(cpu)

def MOVDE(cpu):
    MOV(cpu, cpu.D, cpu.E)

def MOVDH(cpu):
    MOV(cpu, cpu.D, cpu.H)

def MOVDL(cpu):
    MOV(cpu, cpu.D, cpu.L)

def MOVDM(cpu):
    cpu.D.transfer_from(cpu.M)
    cpu.clock.pulse(7)

def MOVEA(cpu):
    MOV(cpu, cpu.E, cpu.A)

def MOVEB(cpu):
    MOV(cpu, cpu.E, cpu.B)

def MOVEC(cpu):
    MOV(cpu, cpu.E, cpu.C)

def MOVED(cpu):
    MOV(cpu, cpu.E, cpu.D)

def MOVEE(cpu):
    NOP(cpu)

def MOVEH(cpu):
    MOV(cpu, cpu.E, cpu.H)

def MOVEL(cpu):
    MOV(cpu, cpu.E, cpu.L)

def MOVEM(cpu):
    cpu.E.transfer_from(cpu.M)
    cpu.clock.pulse(7)

def MOVHA(cpu):
    MOV(cpu, cpu.H, cpu.A)

def MOVHB(cpu):
    MOV(cpu, cpu.H, cpu.B)

def MOVHC(cpu):
    MOV(cpu, cpu.H, cpu.C)

def MOVHD(cpu):
    MOV(cpu, cpu.H, cpu.D)

def MOVHE(cpu):
    MOV(cpu, cpu.H, cpu.E)

def MOVHH(cpu):
    NOP(cpu)

def MOVHL(cpu):
    MOV(cpu, cpu.H, cpu.L)

def MOVHM(cpu):
    cpu.H.transfer_from(cpu.M)
    cpu.clock.pulse(7)

def MOVLA(cpu):
    MOV(cpu, cpu.L, cpu.A)

def MOVLB(cpu):
    MOV(cpu, cpu.L, cpu.B)

def MOVLC(cpu):
    MOV(cpu, cpu.L, cpu.C)

def MOVLD(cpu):
    MOV(cpu, cpu.L, cpu.D)

def MOVLE(cpu):
    MOV(cpu, cpu.L, cpu.E)

def MOVLH(cpu):
    MOV(cpu, cpu.L, cpu.H)

def MOVLL(cpu):
    NOP(cpu)

def MOVLM(cpu):
    cpu.L.transfer_from(cpu.M)
    cpu.clock.pulse(7)

def MOVMA(cpu):
    cpu.M.transfer_from(cpu.A)
    cpu.clock.pulse(7)

def MOVMB(cpu):
    cpu.M.transfer_from(cpu.B)
    cpu.clock.pulse(7)

def MOVMC(cpu):
    cpu.M.transfer_from(cpu.C)
    cpu.clock.pulse(7)

def MOVMD(cpu):
    cpu.M.transfer_from(cpu.D)
    cpu.clock.pulse(7)

def MOVME(cpu):
    cpu.M.transfer_from(cpu.E)
    cpu.clock.pulse(7)

def MOVMH(cpu):
    cpu.M.transfer_from(cpu.H)
    cpu.clock.pulse(7)

def MOVML(cpu):
    cpu.M.transfer_from(cpu.L)
    cpu.clock.pulse(7)


def MVI(cpu, register):
    cpu.fetch_byte()
    register.transfer_from(cpu.Z)
    cpu.clock.pulse(7)

def MVIA(cpu):
    MVI(cpu, cpu.A)

def MVIB(cpu):
    MVI(cpu, cpu.B)

def MVIC(cpu):
    MVI(cpu, cpu.C)

def MVID(cpu):
    MVI(cpu, cpu.D)

def MVIE(cpu):
    MVI(cpu, cpu.E)

def MVIH(cpu):
    MVI(cpu, cpu.H)

def MVIL(cpu):
    MVI(cpu, cpu.L)

def MVIM(cpu):
    cpu.fetch_byte()
    cpu.M.transfer_from(cpu.Z)
    cpu.clock.pulse(10)


def NOP(cpu):
    cpu.clock.pulse(4)


def ORA(cpu, register):
    cpu.A.or_reg(register)
    cpu.update_flags()
    cpu.clock.pulse(4)

def ORAA(cpu):
    ORA(cpu, cpu.A)

def ORAB(cpu):
    ORA(cpu, cpu.B)

def ORAC(cpu):
    ORA(cpu, cpu.C)

def ORAD(cpu):
    ORA(cpu, cpu.D)

def ORAE(cpu):
    ORA(cpu, cpu.E)

def ORAH(cpu):
    ORA(cpu, cpu.H)

def ORAL(cpu):
    ORA(cpu, cpu.L)

def ORAM(cpu):
    cpu.A.or_reg(cpu.M)
    cpu.update_flags()
    cpu.clock.pulse(7)


def ORI(cpu):
    cpu.fetch_byte()
    cpu.A.or_reg(cpu.Z)
    cpu.update_flags()
    cpu.clock.pulse(7)


def OUT(cpu):
    cpu.PC.inc()
    cpu.A.transfer_to(cpu.OUT)
    print(f"\n{cpu.A.value:08b} {cpu.A.value:02x}")
    cpu.clock.pulse(10)


def RAL(cpu):
    cpu.A.rol() # normal 8-bit rotate left
    new_carry = cpu.A.lsb()
    cpu.A.set_bit(0, cpu.flags["carry"]) # swap the lsb and carry bit
    cpu.flags["carry"] = new_carry
    cpu.clock.pulse(4)

def RAR(cpu):
    cpu.A.ror() # normal 8-bit rotate right
    new_carry = cpu.A.msb()
    cpu.A.set_bit(7, cpu.flags["carry"]) # swap the msb and carry bit
    cpu.flags["carry"] = new_carry
    cpu.clock.pulse(4)


def RET(cpu):
    cpu.SP.inc()
    cpu.Z.load(cpu.memory, cpu.SP.value)
    cpu.SP.inc()
    cpu.W.load(cpu.memory, cpu.SP.value)

    cpu.PC.transfer_from(cpu.WZ)
    cpu.clock.pulse(10)


def RLC(cpu):
    cpu.A.rol()
    cpu.flags["carry"] = cpu.A.lsb()
    cpu.clock.pulse(4)


def RRC(cpu):
    cpu.A.ror()
    cpu.flags["carry"] = cpu.A.msb()
    cpu.clock.pulse(4)


def SBB(cpu, register):
    cpu.A.value -= register.value + cpu.flags["carry"]
    cpu.update_flags()
    cpu.clock.pulse(4)

def SBBA(cpu):
    SBB(cpu, cpu.A)

def SBBB(cpu):
    SBB(cpu, cpu.B)

def SBBC(cpu):
    SBB(cpu, cpu.C)

def SBBD(cpu):
    SBB(cpu, cpu.D)

def SBBE(cpu):
    SBB(cpu, cpu.E)

def SBBH(cpu):
    SBB(cpu, cpu.H)

def SBBL(cpu):
    SBB(cpu, cpu.L)

def SBBM(cpu):
    cpu.A.value -= cpu.M.value + cpu.flags["carry"]
    cpu.update_flags()
    cpu.clock.pulse(7)


def SBI(cpu):
    cpu.fetch_byte()
    cpu.A.value -= cpu.Z.value + cpu.flags["carry"]
    cpu.update_flags()
    cpu.clock.pulse(7)


def STA(cpu):
    cpu.fetch_address()
    cpu.A.store(cpu.memory, cpu.WZ.value)
    cpu.clock.pulse(13)


def STC(cpu):
    cpu.flags.set_flag("carry")
    cpu.clock.pulse(4)


def SUB(cpu, register):
    cpu.A.sub(register)
    cpu.update_flags()
    cpu.clock.pulse(4)

def SUBA(cpu):
    SUB(cpu, cpu.A)

def SUBB(cpu):
    SUB(cpu, cpu.B)

def SUBC(cpu):
    SUB(cpu, cpu.C)

def SUBD(cpu):
    SUB(cpu, cpu.D)

def SUBE(cpu):
    SUB(cpu, cpu.E)

def SUBH(cpu):
    SUB(cpu, cpu.H)

def SUBL(cpu):
    SUB(cpu, cpu.L)

def SUBM(cpu):
    cpu.A.sub(cpu.M)
    cpu.update_flags()
    cpu.clock.pulse(7)


def SUI(cpu):
    cpu.fetch_byte()
    cpu.A.sub(cpu.Z)
    cpu.update_flags()
    cpu.clock.pulse(7)


def XRA(cpu, register):
    cpu.A.xor_reg(register)
    cpu.update_flags()
    cpu.clock.pulse(4)

def XRAA(cpu):
    XRA(cpu, cpu.A)

def XRAB(cpu):
    XRA(cpu, cpu.B)

def XRAC(cpu):
    XRA(cpu, cpu.C)

def XRAD(cpu):
    XRA(cpu, cpu.D)

def XRAE(cpu):
    XRA(cpu, cpu.E)

def XRAH(cpu):
    XRA(cpu, cpu.H)

def XRAL(cpu):
    XRA(cpu, cpu.L)

def XRAM(cpu):
    cpu.A.xor_reg(cpu.M)
    cpu.update_flags()
    cpu.clock.pulse(7)


def XRI(cpu):
    cpu.fetch_byte()
    cpu.A.xor_reg(cpu.Z)
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
