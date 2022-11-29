from comms import uart_proc

def write_str(ser, data_str):
    ser.write(uart_proc.str2byte(data_str + '\0'))

def main():
    ser = uart_proc.initialize_serial()
    write_str(ser, "blake blake blake brian brian brian 123456789")

        
if __name__ == "__main__":
    main()