from CPU import *

def main():
    SAP1 = CPU()
    SAP1.program('Programs/test.hex')
    SAP1.run()

if __name__ == '__main__':
    main()