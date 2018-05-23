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

def handle_dir(line):
    print("[dir]", line[1])

def handle_text(line):
    print("[txt]", line[1])

def handle_info(line):
    print(" " * 6 + line[1])

funs = {
    "0": handle_dir,
    "1": handle_text,
    "i": handle_info
}

data = data.decode("ascii")
p = menu.MenuParser(data)
for i in range(2):
    print("\n".join(map(str,p.parse_menu())))