import string

class MenuToken:
    def __init__(self, type, value = None):
        self.type = type
        self.value = value

    def __str__(self):
        return f"MenuToken(type = {self.type}, value = {self.value})"

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
            self.char = None

    def grab_type(self):
        c = self.char
        self.get_char()
        return c

    def grab_unascii(self):
        unascii = ""
        while not self.char in "\x00\t\r\n":
            unascii += self.char
            self.get_char()
        return unascii

    def grab_host(self):
        host = ""
        while True:
            while not self.char in ".\x00\t\r\n":
                host += self.char
                self.get_char()
            if self.char == ".":
                host += "."
                self.get_char()
            else:
                break
        return host
        

    def grab_port(self):
        pass

    def grab_last_line(self):
        pass

    def parse_dir(self):
        type_char = self.grab_type()
        user_name = self.grab_unascii()
        self.get_char()
        host_name = self.grab_host()
        return type_char, user_name, host_name

def run_tests():
    prices = b"0About PricesFPrices/AboutusFpserver.bookstore.umn.eduF70\r\n0Macintosh PricesFPrices/MacFpserver.bookstore.umn.eduF70\r\n0IBM PricesFPrices/IckFpserver.bookstore.umn.eduF70\r\n0Printer & Peripheral PricesFPrices/PPPFpserver.bookstore.umn.eduF70\r\n"
    p = MenuParser(b"0Example\tgopher.example.com\r\n".decode("ascii"))
    print(p.parse_dir())
if __name__ == "__main__":
    run_tests()