import serial as sr

def main():
    port = sr.Serial('/dev/serial0', 9600)
    # or on PC using FTDI232
    # port = sr.Serial('COM7', 9600)
    
    # Set baudrate to 115200
    # a = b'\xAF\x54\xA5'
    # print(a.hex())
    # port.write(a)
    
    # port = sr.Serial('/dev/serial0', 115200)
    
    # Set to querry output
    # a = b'\xA5\x15\xBA'
    # print(a.hex())
    # port.write(a)
    
    while(port.isOpen()):
        # flush all imput before read new value
        port.reset_input_buffer()

        # Read n Bytes according to sensor specs -> read(n)
        # or read 1 byte each -> read()
        # or if sender has '\n' at the end -> readline()
        temp = port.read(9)
        if (hex(temp[0]) == '0x5a') and (hex(temp[1]) == '0x5a'):
            ObjTemp = temp[4] << 8 | temp[5]
            AmbientTemp = temp[6] << 8 | temp[7]
            print(f'Object temp is {ObjTemp/100}')
            print(f'Ambient temp is {AmbientTemp/100} \n')
            
# main entry point for program. we'll call main() to do what needs to be done.
if __name__ == "__main__":
    sys.exit(main())
