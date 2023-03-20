from CPU import *

def main():
    SAP1 = CPU()
    SAP1.loadROM('Programs/test.hex')
    SAP1.run()

if __name__ == '__main__':
    main()



# improvements:
# - implement Register class, and (possibly?) some sort of inheritance/dependence with the memory class
# - implement instruction decoding with dictionary instead of match/case
# - add ability to display full CPU state at once (registers, PC, IR, MAR, memory, etc)
# - implement clock cycling, with properly timed microinstructions
# - bus??