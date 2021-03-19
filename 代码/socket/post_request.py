import socket

#作为buffer overflow模板

content="cmd=whoami"

head = "POST /test.php HTTP/1.1\r\n"
head += "Host: localhost\r\n"
head += "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0\r\n"
head += "Accept: */*\r\n"
head += "Content-Type: application/x-www-form-urlencoded\r\n"
head += "Content-Length: " + str(len(content)) + "\r\n"
head += "Connection: close\r\n"
head += "\r\n"
head += content

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("127.0.0.1", 80))
s.send(head.encode())
print(head.encode())
data = s.recv(1024)
#print("\n" + data.decode())
s.close()
print("\nDone!")