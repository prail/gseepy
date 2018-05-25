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
    """
    Parses Gopher menus into DirEntity objects.
    """
    def __init__(self, text):
        self._text = text
        self._i, self._char = -1, None
        self._get_char()

    def _get_char(self):
        """
        Get a character and store it in self._char if it tries to read over the text.
        """
        self._i += 1
        if self._i < len(self._text):
            self._char = self._text[self._i]
        else:
            self._char = -1

    def _error(self, msg):
        print(f"error: {msg}", file = sys.stderr) # put error here for match failure
        sys.exit(-1)

    def _match(self, c):
        buf = ""
        while self._char != -1 and len(c) > len(buf):
            buf += self._char
            self._get_char()
        if c != buf:
            c, buf = repr(c), repr(buf)
            self._error(f"expected {c} not {buf}")

    def _grab_type(self):
        """
        Grabs a single type character and returns it.
        """
        c = self._char
        if not c in "0123456789+TgI" + "ih":
            c = repr(c)
            self._error(f"unknown type {c}")
        self._get_char()
        return c

    def _grab_unascii(self):
        """
        Grabs an ascii string that doesn't include NUL, Tab or CR-LF.
        """
        unascii = ""
        while self._char != -1 and not self._char in "\x00\t\r\n":
            unascii += self._char
            self._get_char()
        return unascii

    def _grab_host(self):
        """
        Parses a host and returns it.
        """
        host = ""
        while True:
            while self._char != -1 and not self._char in ".\x00\t\r\n":
                host += self._char
                self._get_char()
            if self._char == ".":
                host += "."
                self._get_char()
            else:
                break
        return host

    def _grab_port(self):
        """
        Parses a port and returns an integer. If, there is no port it raises an error.
        """
        port = ""
        while self._char != -1 and self._char in "0123456789":
            port += self._char
            self._get_char()
        if len(port) == 0:
            self._error("port empty")
        return int(port)

    def _parse_dir(self):
        """
        Parses a single directory entity and returns a new DirEntity object.
        """
        type_char = self._grab_type()
        user_name = self._grab_unascii() #This gets the user_name field for the DirEntity
        self._match("\t")
        selector = self._grab_unascii() #This gets the selector.
        self._match("\t")
        host = self._grab_host()
        self._match("\t")
        port = self._grab_port()
        self._match("\r\n")
        return DirEntity(type_char, user_name, selector, host, port)
    
    def parse_menu(self):
        """
        Returns a list of DirEntity objects.
        """
        dirs = []
        while self._char != -1 and self._char != ".":
            dirs.append(self._parse_dir())
        return dirs

def run_tests():
    """
    Runs tests on the MenuParser class.
    """
    p = MenuParser(b"0\t\tgopher.example.com\t70\r\n".decode("ascii"))
    print(p._parse_dir() == ("0", "", "", "gopher.example.com", 70))

if __name__ == "__main__":
    run_tests()
