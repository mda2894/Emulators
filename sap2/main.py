from cpu import CPU

def main():
    sap2 = CPU()
    sap2.program('test_programs/test.hex')
    sap2.run()

if __name__ == '__main__':
    main()
