# Reminder: This is a comment. The first line imports a default library "socket" into Python.
# You dont install this. The second line is initialization to add TCP/IP protocol to the
# endpoint.
import socket
class TCPReceiver: 
    def __init__(self):
        self.serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serv.bind(('0.0.0.0', 8080))
        self.serv.listen(5)

    def run(self):
        while True:
            conn, addr = self.serv.accept()
            from_client = ''
            while True:
                data = conn.recv(4096)
                from_client += data.decode('utf_8')
                print(from_client)