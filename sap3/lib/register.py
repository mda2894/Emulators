import math

class Register:
    def __init__(self, name, width = 8):
        self.name = name
        self.width = width
        self.max_value = 2 ** width - 1

        self.value = 0


    '''Getting, setting, and clearing register value'''


    @property
    def value(self):
        return self._value


    @value.setter
    def value(self, new_value):
        self._value = new_value & self.max_value

    
    def clear(self):
        self.value = 0


    '''Displaying register contents'''


    def bin_dump(self):
        print(f'{self.name} Register: {self.value:0{self.width}b}')


    def hex_dump(self):
        print(f'{self.name.ljust(3)} {self.value:0{math.ceil(self.width // 4)}x}')


    '''Transferring data between registers and memory'''


    def transfer_to(self, other):
        other.value = self.value

    
    def transfer_from(self, other):
        self.value = other.value


    def store(self, memory, address):
        memory[address] = self.value


    def load(self, memory, address):
        self.value = memory[address]


    '''Mathematical and logical operations'''


    def msb(self, bits = 1):
        return self.value >> (self.width - bits)


    def lsb(self, bits = 1):
        return self.value & 2 ** bits - 1


    def inc(self):
        self.value += 1


    def dec(self):
        self.value -= 1


    def comp(self):
        self.value ^= self.max_value


    def add(self, other):
        self.value += other.value


    def sub(self, other):
        self.value -= other.value


    def and_reg(self, other):
        self.value &= other.value


    def and_imm(self, val):
        self.value &= val


    def or_reg(self, other):
        self.value |= other.value


    def or_imm(self, val):
        self.value |= val


    def xor_reg(self, other):
        self.value ^= other.value


    def xor_imm(self, val):
        self.value ^= val


    def ror(self, rot_bits = 1):
        self.value = (self.value >> (rot_bits % self.width)) | (self.value << (self.width - (rot_bits % self.width)))


    def rol(self, rot_bits = 1):
        self.value = (self.value << (rot_bits % self.width)) | (self.value >> (self.width - (rot_bits % self.width)))



class DoubleRegister(Register):
    def __init__(self, name, upper_register, lower_register):
        self.name = name
        self.upper_register = upper_register
        self.lower_register = lower_register

        self.upper_width = self.upper_register.width
        self.lower_width = self.lower_register.width
        self.width = self.upper_width + self.lower_width

        self.max_value = 2 ** self.width - 1

        self.value = 0


    @property
    def value(self):
        return (self.upper_register.value << self.lower_width) | self.lower_register.value


    @value.setter
    def value(self, new_value):
        self.lower_register.value = new_value & self.lower_register.max_value
        self.upper_register.value = new_value >> self.lower_width



class PseudoRegister(Register):
    def __init__(self, name, memory, pointer_register):
        self.name = name
        self.memory = memory
        self.pointer_register = pointer_register

        self.width = self.memory.width
        self.max_value = 2 ** self.width - 1

    
    @property
    def value(self):
        return self.memory[self.pointer_register.value]


    @value.setter
    def value(self, new_value):
        self.memory[self.pointer_register.value] = new_value