import socket

class TCPSender:
    def __init__(self, addr:str):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((addr, 8080))

    def send(self, msg:str):
        self.client.sendall((msg + '\n').encode())