import serial

# Initialize Serial comms
def initialize_serial():
    ser = serial.Serial ("/dev/ttyS0", 9600, timeout=1)    #Open port with baud rate
    print("===== Serial Receiver Initialized =====")
    print(ser)
    return ser

def byte2str(bytestr):
    return bytestr.decode("utf-8")

def str2byte(str):
    return str.encode('utf-8')