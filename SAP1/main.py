from lib.cpu import CPU

def main():
    SAP1 = CPU()
    SAP1.program('test_programs/test.hex')
    SAP1.run()

if __name__ == '__main__':
    main()
