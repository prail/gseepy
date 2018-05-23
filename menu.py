import sys

class DirEntity:
    def __init__(self, type_char, user_name, selector, host, port):
        self.type = type_char
        self.user_name = user_name
        self.selector = selector
        self.host = host
        self.port = port

    def __str__(self):
        return str((self.type, self.user_name, self.selector, self.host, self.port))
    
    def __repr__(self):
        return self.__str__()

class MenuParser:
    def __init__(self, text):
        self.text = text
        self.i, self.char = -1, None
        self.get_char()

    def get_char(self):
        self.i += 1
        if self.i < len(self.text):
            self.char = self.text[self.i]
        else:
            self.char = -1

    def error(self, msg):
        print(f"error: {msg}", file = sys.stderr) # put error here for match failure
        sys.exit(-1)

    def match(self, c):
        buf = ""
        while self.char != -1 and len(c) > len(buf):
            buf += self.char
            self.get_char()
        if c != buf:
            c, buf = repr(c), repr(buf)
            self.error(f"expected {c} not {buf}")

    def grab_type(self):
        c = self.char
        if not c in "0123456789+TgI" + "ih":
            c = repr(c)
            self.error(f"unknown type {c}")
        self.get_char()
        return c

    def grab_unascii(self):
        unascii = ""
        while self.char != -1 and not self.char in "\x00\t\r\n":
            unascii += self.char
            self.get_char()
        return unascii

    def grab_host(self):
        host = ""
        while True:
            while self.char != -1 and not self.char in ".\x00\t\r\n":
                host += self.char
                self.get_char()
            if self.char == ".":
                host += "."
                self.get_char()
            else:
                break
        return host

    def grab_port(self):
        port = ""
        while self.char != -1 and self.char in "0123456789":
            port += self.char
            self.get_char()
        if len(port) == 0:
            self.error("port empty")
        return int(port)

    def parse_dir(self):
        type_char = self.grab_type()
        user_name = self.grab_unascii()
        self.match("\t")
        selector = self.grab_unascii()
        self.match("\t")
        host = self.grab_host()
        self.match("\t")
        port = self.grab_port()
        self.match("\r\n")
        return DirEntity(type_char, user_name, selector, host, port)
    
    def parse_menu(self):
        dirs = []
        while self.char != -1 and self.char != ".":
            dirs.append(self.parse_dir())
        return dirs

def run_tests():
    p = MenuParser(b"0\t\tgopher.example.com\t70\r\n".decode("ascii"))
    print(p.parse_dir() == ("0", "", "", "gopher.example.com", 70))

if __name__ == "__main__":
    run_tests()
