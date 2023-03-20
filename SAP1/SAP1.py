from CPU import *

def main():
    SAP1 = CPU()
    SAP1.loadROM('Programs/test.hex')
    SAP1.run()

if __name__ == '__main__':
    main()