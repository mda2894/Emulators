from cpu import CPU

def main():
    sap1 = CPU()
    sap1.program('test_programs/test.hex')
    sap1.run()

if __name__ == '__main__':
    main()
