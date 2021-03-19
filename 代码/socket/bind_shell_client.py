import socket

ip = "192.168.110.3"
port = 4444

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((ip, port))

while True:
    userInput = input('>>> ')
    if userInput == "exit":         #用户输入exit就退出
        break
    s.send(userInput.encode())

    reced = s.recv(1024)
    if not reced:                   #服务器关闭连接，就退出程序
        break
    print(reced.decode())
s.close()