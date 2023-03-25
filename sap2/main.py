from cpu import CPU

def main():
    sap2 = CPU()
    sap2.program('test_programs/test.hex')
    sap2.step()

if __name__ == '__main__':
    main()
