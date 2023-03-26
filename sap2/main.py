from cpu import CPU

def main():
    sap2 = CPU()
    sap2.load('test_programs/test.hex')
    sap2.program_mode()

if __name__ == '__main__':
    main()
