import socket
import time

class TCPSender:
    def __init__(self, addr:str, enabled:bool):
        self.enabled = enabled
        if (self.enabled):
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            while(True):
                try:
                    self.client.connect((addr, 8080))
                    break
                except:
                    print("-== Connection to LED CONTROLLER Failed, trying again ==-")
                    time.sleep(1)

    def send(self, msg:str):
        if (self.enabled):
            self.client.sendall((msg + '\n').encode())