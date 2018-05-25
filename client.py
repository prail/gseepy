import socket, menu

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("gopher.floodgap.com", 70))
sock.sendall("\r\n".encode("ascii"))

data = b""
while True:
    temp = sock.recv(1024)
    if not temp: break
    data += temp

sock.close()

data = data.decode("ascii")
p = menu.Parser(data)
for i in range(2):
    print("\n".join(map(str,p.parse())))