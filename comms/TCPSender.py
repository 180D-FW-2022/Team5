import socket

class TCPSender:
    def __init__(self, addr:str, enabled:bool):
        self.enabled = enabled
        if (self.enabled):
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect((addr, 8080))

    def send(self, msg:str):
        if (self.enabled):
            self.client.sendall((msg + '\n').encode())