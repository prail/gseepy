import socket

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
for line in data.split("\r\n"):
    if line == ".": break
    line = [line[0]] + line[1:].split("\t")
    if not line[0] in funs: continue
    funs[line[0]](line)