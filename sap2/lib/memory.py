import math
import os

class Memory:
    def __init__(self, size, width = 8):
        self.size = size
        self.bin_width = width
        self.hex_width = math.ceil(self.bin_width // 4)
        self.max_value = 2 ** width - 1

        self.contents = [0] * size
    

    def __getitem__(self, address):
        return self.contents[address]


    def __setitem__(self, address, value):
        self.contents[address] = value & self.max_value


    def peek(self, address):
        return self.contents[address]


    def poke(self, address, value):
        self.contents[address] = value


    def clear(self):
        self.contents = [0] * self.size


    def write(self, program, start_address = 0):
        if not 0 <= start_address < self.size:
            raise ValueError(f"Invalid Starting Address: {start_address}")

        elif isinstance(program, list):
            end_address = start_address + len(program) - 1

            if end_address >= self.size:
                raise IndexError(f"Program too large")

            for i in range(start_address, end_address + 1):
                self.contents[i] = program[i]

        elif os.path.isfile(program) and os.path.exists(program):
            file_ext = os.path.splitext(program)[1]
            
            if file_ext == '.hex':
                length = 2
                base = 16
            elif file_ext == '.bin':
                length = 8
                base = 2
            else:
                raise TypeError("Wrong file type: file must have extension .bin (for binary) or .hex (for hexadecimal)")

            with open(program, 'r') as f:
                if (line := f.readline()[0:length]):
                    self.contents[start_address] = int(line, base)

                else:
                    raise ValueError("File is empty")

                index = start_address + 1
                while (line := f.readline()[0:length]):
                    if index >= self.size:
                        raise IndexError("Program too large")

                    self.contents[index] = int(line, base)

                    index += 1
        
        else:
            raise ValueError("Invalid File")


    def hex_dump(self, start_address = None, end_address = None):
        if not (start_address or end_address):
            first_value = 0
            last_value = self.size - 1
        
        else:
            start_address = start_address or 0
            end_address = end_address or self.size - 1

            first_value = (start_address // 16) * 16
            last_value = end_address + (15 - end_address % 16)

        address_hex_chars = len(str(hex(last_value))) - 2

        prev_line = []
        consecutive_lines = 0

        print()

        for i in range(first_value, last_value, 16):
            line = self.contents[i:i+16]

            if line == prev_line:
                consecutive_lines += 1

                if consecutive_lines == 2:
                    print('*')

            else:
                consecutive_lines = 0
                prev_line = line

                hex_values = [f'{byte:0{self.hex_width}x}' for byte in line]
                
                print(f'{i:0{address_hex_chars}x}: ' + ' '.join(hex_values))

        if consecutive_lines > 0:
            hex_values = [f'{byte:0{self.hex_width}x}' for byte in line]
                
            print(f'{i:0{address_hex_chars}x}: ' + ' '.join(hex_values))

