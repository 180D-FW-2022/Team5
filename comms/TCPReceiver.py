# Reminder: This is a comment. The first line imports a default library "socket" into Python.
# You dont install this. The second line is initialization to add TCP/IP protocol to the
# endpoint.
import socket
class TCPReceiver: 
    def __init__(self):
        self.serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serv.bind(('0.0.0.0', 8080))
        self.serv.listen(5)
        self.recq = []

    def run(self):
        conn = self.serv.accept()
        return conn

    def interpret(self, conn):
        data = conn.recv(4096)
        self.recq.append(data.decode('utf_8'))