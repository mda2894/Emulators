import math, os

class Memory:
    def __init__(self, size, value_size = 8):
        self.size = size
        self.value_size = value_size

        self.max_value = 2 ** value_size - 1
        self.max_hex_chars = math.ceil(math.log(size, 16))

        self.memory = [0] * size
    

    def __getitem__(self, address):
        return self.memory[address]


    def __setitem__(self, address, value):
        self.memory[address] = value & self.max_value


    def write(self, program, start_address = 0):
        if not 0 <= start_address < self.size:
            raise ValueError(f"Invalid Address: {start_address}")

        elif isinstance(program, list):
            end_address = start_address + len(program) - 1

            if end_address >= self.size:
                raise ValueError(f"Invalid Address: {start_address}")

            for i in range(start_address, end_address + 1):
                self.memory[i] = program[i]

        elif os.path.isfile(program) and os.path.exists(program):
            pass


    def dump(self, start_address = 0, end_address = None):
        end_address = end_address or self.size - 1

        if not 0 <= start_address <= end_address < self.size:
            raise ValueError(f"Invalid dump range: {start_address} - {end_address}")

        for i in range(start_address, end_address + 1):
            print("{i:0{self.max_hex_chars}x}: {self.memory[i]:0{self.value_size}b}")
