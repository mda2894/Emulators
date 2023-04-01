'''Module for different type of Register classes'''

import math

class Register:
    '''Standard Register'''

    def __init__(self, name, width = 8):
        self.name = name
        self.width = width
        self.max_value = 2 ** width - 1

        self.value = 0
        self.carry = 0

    '''Getting, setting, and clearing register value'''

    @property
    def value(self):
        return self._value


    @value.setter
    def value(self, new_value):
        self._value = new_value & self.max_value
        self.carry = self._value < new_value

    
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


    def inc(self, n = 1):
        self.value += n


    def dec(self, n = 1):
        self.value -= n


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


    # set the i-th bit of this register to x
    def set_bit(self, i, x):
        mask = 1 << i
        if x:
            self.value |= mask
        else:
            self.value &= ~mask



class DoubleRegister(Register):
    '''Double Register - made up of two standard registers'''

    def __init__(self, name, upper_register, lower_register):
        self.name = name
        self.upper_register = upper_register
        self.lower_register = lower_register

        self.upper_width = self.upper_register.width
        self.lower_width = self.lower_register.width
        self.width = self.upper_width + self.lower_width

        self.max_value = 2 ** self.width - 1


    @property
    def value(self):
        return (self.upper_register.value << self.lower_width) | self.lower_register.value


    @value.setter
    def value(self, new_value):
        self.lower_register.value = new_value & self.lower_register.max_value
        self.upper_register.value = new_value >> self.lower_width



class PseudoRegister(Register):
    '''Pseudo-Register - memory location addressed by a separate "pointer" register'''

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



class FlagsRegister(Register):
    '''
    Flags Register - collects the flags for a CPU in a single register object

    **flag_index should be used to provide the names of the flags to be stored
    and the index of the bit within the register that represents that flag's value
    e.g. FlagRegister(width = 2, flag_at_index_0 = 0, flag_at_index_1 = 1)

    If width is greater than the number of flag arguments given,
    then all bits in the register without an associated flag will remain 0
    '''

    def __init__(self, name, width = 8, **flag_index):
        self.name = name
        self.width = width
        self.flags = dict.fromkeys(flag_index.keys(), False)
        self.index = flag_index


    def __getitem__(self, flag):
        return self.flags[flag]


    def __setitem__(self, flag, value):
        self.flags[flag] = value & 1

    
    @property
    def value(self):
        value = 0

        for flag in self.flags.keys():
            value |= self.flags[flag] << self.index[flag]

        return value


    @value.setter
    def value(self, new_value):
        for flag in self.flags.keys():
            self.flags[flag] = new_value & (1 << self.index[flag]) > 0


    def set_flag(self, flag):
        self.flags[flag] = 1
    

    def clear_flag(self, flag):
        self.flags[flag] = 0


    def toggle_flag(self, flag):
        self.flags[flag] = not self.flags[flag]


    def dump(self):
        print()
        for flag, value in self.flags.items():
            print(f"{flag.ljust(6)} {value:01d}")
