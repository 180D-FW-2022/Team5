from comms import uart_proc


# Read an incoming message through UART
def read_all(port, chunk_size=200):
    if not port.timeout:
        raise TypeError('Port needs to have a timeout set!')

    read_buffer = b''

    while True:
        byte_chunk = port.read_until(size=chunk_size)
        read_buffer += byte_chunk
        if not len(byte_chunk) == chunk_size:
            break

    return read_buffer


# Checks if the message received is valid, returns the source of the message (this is hardcoded in the teensy)
def extract_msg(data_str):
    if (data_str[len(data_str)-1] != '\n'  or data_str.count('\n') != 1):
        return 0, ""
    if (data_str[0] == 'D' and data_str[2] == '-' and data_str[1].isdigit()):
        data_src = int(data_str[1])
        data_str = data_str[3:len(data_str)-1]
        return data_src, data_str
    return 0, ""

def main():
    ser = uart_proc.initialize_serial()

    while True:
        received_data = read_all(ser)              #read serial port
        if (len(received_data) != 0):
            raw_data_str = uart_proc.byte2str(received_data)
            data_src, data_str = extract_msg(raw_data_str)
            print(data_src)
            print(data_str)


if __name__ == "__main__":
    main()
