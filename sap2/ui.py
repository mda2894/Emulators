'''functions for handling the "terminal" interface and user input'''


def program_mode(cpu):
    '''main terminal interface mode'''
    display_program_help()
    current = get_address_from_user()

    while True:
        match (cmd := input(f"\n{(current):04x}: ")):
            case "view":
                cpu.memory.hex_dump()

            case "cpu":
                display_state(cpu)
            
            case "restart":
                cpu.memory.clear()

                display_program_help()
                current = get_address_from_user()
            
            case "run":
                cpu.reset()

                try:
                    cpu.run()

                    display_program_help()
                    current = get_address_from_user()

                except:
                    display_program_run_error()
            
            case "step":
                cpu.reset()

                try:
                    step_mode(cpu)
                    
                    display_program_help()
                    current = get_address_from_user()

                except:
                    display_program_run_error()
            
            case "exit":
                break

            case "help":
                display_program_help()

            case "jump":
                current = get_address_from_user()

            case "export":
                print("\nPlease input a file name to export your program to. \
                \n  Include the extension (.hex for hex output or .bin for binary)")

                valid_file = False

                while not valid_file:
                    file = input("\nFile name: ")

                    if file[-4:] in [".hex", ".bin"]:
                        try:
                            export_memory(cpu, file)
                            valid_file = True
                            print("\nProgram succesfully exported")
                        except:
                            display_program_export_error()

                    else:
                        print("\nInvalid file extension. \
                        \n  Only .hex or .bin files are allowed.")

            case _:
                if current <= 0xFFFF:
                    try:
                        cpu.store_hex_input(cmd, address)

                        current += 1

                    except:
                        display_invalid_input_error()

                else:
                    print("\nEnd of memory. Jump somewhere else in memory to continue programming.")


def step_mode(cpu, program = None):
    '''cpu step-by-step operation mode'''
    if program:
        try:
            cpu.memory.write(program, start)
        except:
            print

    display_step_help()

    while True:
        match input("\nEnter command: "): 
            case "":
                step(cpu)
            
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
    if not cpu.flags["halt"]:
        cpu.fetch_instruction()
        cpu.execute_instruction()
        display_state(cpu)

    else:
        print('\nCPU is halted. Type "reset" to start over or "exit" to exit the program.')


def display_state(cpu, start = 0, end = None):
    print('\nFlags')
    cpu.flags.dump()

    print('\nRegisters\n')
    for register in cpu.registers:
        register.hex_dump()

    print("\nMemory")
    cpu.memory.hex_dump(start, end)


def export_memory(cpu, file):
    with open(file, 'w') as f:
        if file[-4:] == ".hex":
            for byte in cpu.memory.contents:
                f.write(f"{byte:02x}\n")
        elif file[-4:] == ".bin":
            for byte in cpu.memory.contents:
                f.write(f"{byte:08b}\n")


'''general UI functions - don't need access to CPU object'''


def get_address_from_user():
    address = -1
    
    while address < 0:
        try:
            address = int(input("\nEnter address (hex 0000 - FFFF): "), 16)
        except:
            print("\nInvalid memory address")
            continue

        if not (0x0000 <= address <= 0xFFFF):
            address = -1
            print("\nInvalid memory address")

    return address


def display_program_help():
    print('\nManual Program Mode \
    \n\nPlease enter program as hex bytes (00 - FF). Type: \
    \n  "view" to view the program you have entered \
    \n  "cpu" to view the current state of your CPU \
    \n  "restart" to restart your program from the beginning \
    \n  "run" to run the program from start to finish \
    \n  "step" to run the program step by step \
    \n  "exit" to exit the program \
    \n  "jump" to jump to a particular line and edit your program from there \
    \n  "help" to repeat this message')


def display_step_help():
    print('\nStep-by-Step Operation Mode \
    \n\nHit enter to execute the next instruction. Or type: \
    \n  "reset" to reset the CPU \
    \n  "exit" to exit step mode \
    \n  "help" to repeat this message')


def display_program_run_error():
    print('\nThere was an error while running your program. \
    \n  Type "cpu" to view the state of your CPU when it failed.')


def display_program_load_error():
    print('\nThere was an error while loading your program.')


def display_program_export_error():
    print('\nThere was an error while exporting your program.')


def display_invalid_input_error():
    print('\nDid not recognize command: type "help" for information on accepted commands.')