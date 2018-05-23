import string

class MenuToken:
    def __init__(self, type, value = None):
        self.type = type
        self.value = value

    def __str__(self):
        return f"MenuToken(type = {self.type}, value = {self.value})"

    def __repr__(self):
        return self.__str__()

class MenuTokenizer:
    def __init__(self, text):
        self.text = text
        self.i = -1
        self.char = None
        self.token = None
        self.next_char()
        self.next_token()

    def next_char(self):
        self.i += 1
        if self.i < len(self.text):
            self.char = self.text[self.i]
        else:
            self.char = None

    def next_token(self):
        if self.char == "\r":
            self.next_char()
            if self.char == "\n":
                self.token = MenuToken("cr-lf")
        #elif self.char == ""

class MenuParser:
    def __init__(self, text):
        self.text = text
        self.i = 0
    def parse(self):
        pass

def run_tests():
    prices = b"0About PricesFPrices/AboutusFpserver.bookstore.umn.eduF70\r\n0Macintosh PricesFPrices/MacFpserver.bookstore.umn.eduF70\r\n0IBM PricesFPrices/IckFpserver.bookstore.umn.eduF70\r\n0Printer & Peripheral PricesFPrices/PPPFpserver.bookstore.umn.eduF70\r\n"
    tokenizer = MenuTokenizer(b"\r\n".decode("ascii"))
    print(tokenizer.char)
    tokenizer.next_token()
    print(tokenizer.token)
if __name__ == "__main__":
    run_tests()