import serial

# Initialize Serial comms
def initialize_serial():
    ser = serial.Serial ("/dev/ttyS0", 9600, timeout=2)    #Open port with baud rate
    print("===== Serial Receiver Initialized =====")
    print(ser)
    return ser

def byte2str(bytestr):
    try:
        return bytestr.decode("utf-8")
    except:
        print(bytestr)
        return ""

def str2byte(str):
    return str.encode('utf-8')