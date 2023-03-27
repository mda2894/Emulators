from cpu import CPU
import ui

def main():
    sap2 = CPU()
    sap2.load('test_programs/test.hex')
    ui.program_mode(sap2)

if __name__ == '__main__':
    main()
