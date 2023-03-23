import math

class Register:
    def __init__(self, name, width = 8):
        self.name = name
        self.width = width
        self.max_value = 2 ** width - 1

        self.value = 0


    '''getting, setting, and clearing register value'''


    @property
    def value(self):
        return self._value


    @value.setter
    def value(self, new_value):
        self._value = new_value & self.max_value

    
    def clear(self):
        self.value = 0


    '''displaying register contents'''


    def bin_dump(self):
        print(f'{self.name} Register: {self.value:0{self.width}b}')


    def hex_dump(self):
        print(f'{self.name} Register: {self.value:0{math.ceil(self.width // 4)}x}')


    '''transferring data between registers and memory'''


    def transfer_to(self, other):
        other.value = self.value

    
    def transfer_from(self, other):
        self.value = other.value


    def store(self, memory, address):
        memory[address] = self.value


    def load(self, memory, address):
        self.value = memory[address]


    '''mathematical and logical operations'''


    def msb(self, bits = 1):
        return self.value >> (self.width - bits)


    def lsb(self, bits = 1):
        return self.value & 2 ** bits - 1


    def inc(self):
        self.value += 1


    def dec(self):
        self.value -= 1


    def add(self, other):
        self.value += other.value


    def sub(self, other):
        self.value -= other.value


    def ror(self, rot_bits = 1):
        self.value = (self.value >> (rot_bits % self.width)) | (self.value << (self.width - (rot_bits % self.width)))


    def rol(self, rot_bits = 1):
        self.value = (self.value << (rot_bits % self.width)) | (self.value >> (self.width - (rot_bits % self.width)))