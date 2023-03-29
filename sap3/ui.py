'''Module for handling the "terminal" interface and user input'''
import os

def program_mode(cpu):
    '''Main terminal interface mode'''

    display_program_help()

    program = [0] * cpu.memory.size
    current = get_address_from_user()


    while True:
        match (cmd := input(f"\n{(current):04x}: ")):
            case "view":
                program_hex_dump(program)

            case "cpu":
                display_state(cpu)
            
            case "clear":
                program = [0] * cpu.memory.size

                display_program_help()
                current = get_address_from_user()
            
            case "run":
                try:
                    cpu.reset()
                    cpu.load(program)
                    cpu.run()

                    display_program_help()
                    current = get_address_from_user()

                except Exception as exc:
                    display_program_run_error()
                    print(exc)
            
            case "step":
                cpu.reset()
                cpu.load(program)
                step_mode(cpu)
                
                display_program_help()
                current = get_address_from_user()

            case "reset":
                cpu.reset()
                cpu.memory.clear()

                print('\nCPU Reset')
            
            case "exit":
                break

            case "help":
                display_program_help()

            case "jump":
                current = get_address_from_user()

            case "save":
                print("\nPlease input a file name to save your program to. \
                \n  Include the extension (.hex for hex output or .bin for binary)")

                valid_file = False

                while not valid_file:
                    file = input("\nFile name: ")
                    
                    if file == "exit":
                        print("\nFailed to save file")
                        break

                    if file[-4:] in [".hex", ".bin"]:
                        try:
                            save_program(file, program)
                            valid_file = True
                            print("\nProgram successfully saved")
                        except Exception as exc:
                            display_program_save_error()
                            print(exc)

                    else:
                        print("\nInvalid file extension. \
                        \n  Only .hex or .bin files are allowed.")


            case "load":
                print("\nPlease input a file name to load into memory. \
                \n  Include the extension (.hex for hex output or .bin for binary)")

                valid_file = False

                while not valid_file:
                    file = input("\nFile name: ")

                    if file == "exit":
                        print("\nFailed to load file")
                        break

                    if file[-4:] in [".hex", ".bin"]:
                        try:
                            load_program(file, program)
                            valid_file = True
                            print("\nProgram successfully loaded")
                        except Exception as exc:
                            display_program_load_error()
                            print(exc)

                    else:
                        print("\nInvalid file extension. \
                        \n  Only .hex or .bin files are allowed.")


            case _:
                try:
                    cmd = int(cmd, 16)
                except Exception as exc:
                    display_invalid_input_error()
                    print(exc)
                    continue

                if not (0 <= cmd <= 0xFF):
                    print('\nInput was not a valid hex byte')

                elif 0 <= current <= 0xFFFF:
                    program[current] = cmd
                    current += 1

                else:
                    print("\nInvalid memory location. Jump somewhere else to continue programming.")


def step_mode(cpu):
    '''CPU step-by-step operation mode'''

    display_step_help()

    input("\nPress enter to begin: ")
    display_state(cpu)

    while True:
        match input("\nEnter command: "): 
            case "":
                try:
                    step(cpu)
                except Exception as exc:
                    display_step_error()
                    print(exc)

            case "exit":
                break

            case "reset":
                print("\nResetting computer")

                cpu.reset()
                step_mode(cpu)
                break

            case "help":
                display_step_help()

            case _:
                display_invalid_input_error()


def step(cpu):
    if not cpu.halt:
        cpu.fetch_instruction()
        cpu.execute_instruction()
        display_state(cpu)

    else:
        print('\nCPU is halted. Type "reset" to start over or "exit" to exit the program.')


def display_state(cpu, start = 0, end = None):
    print('\nFlags')
    cpu.F.dump()

    print('\nRegisters\n')
    for register in cpu.registers:
        register.hex_dump()

    print("\nMemory")
    cpu.memory.hex_dump(start, end)


def save_program(file, program):
    with open(file, 'w') as f:
        file_ext = os.path.splitext(file)[1]
        if file_ext == ".hex":
            for byte in program:
                f.write(f"{byte:02x}\n")
        elif file_ext == ".bin":
            for byte in program:
                f.write(f"{byte:08b}\n")


def load_program(file, program):
    if os.path.isfile(file) and os.path.exists(file):
        file_ext = os.path.splitext(file)[1]
        
        if file_ext == '.hex':
            length = 2
            base = 16
        elif file_ext == '.bin':
            length = 8
            base = 2

        with open(file, 'r') as f:
            index = 0

            while (line := f.readline()[0:length]):
                if index >= 0xFFFF:
                    raise IndexError("Program too large")

                program[index] = int(line, base)

                index += 1

    else:
        raise ValueError("Invalid File")


def program_hex_dump(program):
        prev_line = []
        consecutive_lines = 0

        print()

        for i in range(0, 0xFFFF, 16):
            line = program[i:i+16]

            if line == prev_line:
                consecutive_lines += 1

                if consecutive_lines == 2:
                    print('*')

            else:
                consecutive_lines = 0
                prev_line = line

                hex_values = [f'{byte:02x}' for byte in line]
                
                print(f'{i:04x}: ' + ' '.join(hex_values))

        if consecutive_lines > 0:
            hex_values = [f'{byte:02x}' for byte in line]
                
            print(f'{i:04x}: ' + ' '.join(hex_values))


'''General UI functions - don't need access to CPU object'''


def get_address_from_user():
    address = -1
    
    while address < 0:
        try:
            address = int(input("\nEnter address (hex 0000 - FFFF): "), 16)
        except Exception as exc:
            print("\nInvalid memory address")
            print(exc)
            continue

        if not (0x0000 <= address <= 0xFFFF):
            address = -1
            print("\nInvalid memory address")

    return address


def display_program_help():
    print('\nManual Program Mode \
    \n\nPlease enter program as hex bytes (00 - FF). Type: \
    \n  "view" to view your program \
    \n  "jump" to jump to a particular line and edit your program from there \
    \n  "clear" to clear your current program and restart program mode \
    \n  "save" to save your program to a file \
    \n  "load" to load a program from a file \
    \n  "step" to load the program into memory and run it step by step \
    \n  "run" to load the program into memory and run it from start to finish \
    \n  "cpu" to display the current state of the CPU (flags, registers, & memory) \
    \n  "reset" to reset the CPU (clear all flags, registers, and memory) \
    \n  "exit" to exit program mode \
    \n  "help" to repeat this message')


def display_program_run_error():
    print('\nThere was an error while running your program. \
    \n  Type "cpu" to view the state of your CPU when it failed.')


def display_program_load_error():
    print('\nThere was an error while loading your program.')


def display_program_save_error():
    print('\nThere was an error while saving your program.')


def display_step_help():
    print('\nStep-by-Step Operation Mode \
    \n\nHit enter to execute the next instruction. Or type: \
    \n  "reset" to reset the CPU \
    \n  "exit" to exit step mode \
    \n  "help" to repeat this message')


def display_step_error():
    print('\nThere was an error while executing the next instruction.')


def display_invalid_input_error():
    print('\nInvalid input: type "help" for information on accepted commands.')
