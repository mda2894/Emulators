import math

class Register:
    def __init__(self, name, bits = 8):
        self.name = name
        self.bits = bits
        self.max_value = 2 ** bits - 1

        self.value = 0


    @property
    def value(self):
        return self._value


    @value.setter
    def value(self, new_value):
        self._value = new_value & self.max_value


    def inc(self):
        self.value += 1


    def dec(self):
        self.value -= 1


    def transfer_to(self, other):
        other.value = self.value


    def store(self, memory, address):
        memory[address] = self.value


    def load(self, memory, address):
        self.value = memory[address]


    def add(self, other):
        self.value += other.value


    def sub(self, other):
        self.value -= other.value


    def msb(self, bits):
        return self.value >> (self.bits - bits)


    def lsb(self, bits):
        return self.value & 2 ** bits - 1


    def bindump(self):
        print(f'{self.name} Register: {self.value:0{self.bits}b}')


    def hexdump(self):
        print(f'{self.name} Register: {self.value:0{math.ceil(self.bits // 4)}x}')