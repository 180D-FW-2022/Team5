# Driver's Edd Communications Interface

## Hardware Architecture
Required Materials
* \>= 2 Raspberry Pi's
* 1 Teensy 3.5
* 1 Breadboard
* Jumper Wires

This hardware architecture supports 1 main controller  Pi, and up to 4 peripheral Raspberry Pi's from which the main controller can read data from through UART. The Teensy acts as a buffer. It will organize the data received from the peripheral Pi's, and send it to the main controller.

Wiring:
1. Connect all grounds (all raspi's and teensy) together
2. Setup UART wiring, see bottom of the README for which pins TX/RX pins represent which device address


Before starting, be sure to also enable UART on your Pi
```
sudo raspi-config
3 - Interface Options
I6 - Serial Port
No - Login Shell
Yes - Enable Serial Hardware
Finish
```

## Pi Comms Usage: An overview of all functions
### In uart_proc.py (UART utilities needed by both the main controller and peripheral Pi's)
* `initialize_serial` Initialize Serial Comms at a baud rate of 9600.
* `byte2str` Decode a received byte string to an actual string, encoded in UTF-8.
* `str2byte` Encode a UTF-8 encoded string so that it can be sent through serial.

### In uart_rec.py (Only needed for the main controller, as it receives information from peripheral pi's)
* `read_all(port)` Takes in "port", a serial Object created by `initialize_serial`, and reads data coming into the port until the buffer is empty. Returns the data in the form of a byte string.
* `extract_msg(raw_data_str)` Takes in a UTF-encoded string and checks if it is valid (if any information is lost in the comms process). Returns an (int, string) tuple, the int value represents from which peripheral pi the message is from (this address is hardcoded in the Teensy software). The string value is the cleaned up data string. It would be the same string as the one sent by the write_str function by the peripheral pi.

### In uart_send.py (Only needed for peripheral pi's, as they need to send data to the main controller)
* `write_str(ser, data_str)` Takes in "ser", a serial Object created by `initialize_serial`, and sends a string "data-str" through the channel.


## Teensy buffer
Serial1: TX/RX pins 0, 1 is reserved for the main controller pi.\
Serial2: TX/RX pins 9, 10 represents device source address 1.\
Serial3: TX/RX pins 7, 8 represents device source address 2.\
Other Serial Ports are not set up yet.

