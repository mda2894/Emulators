class FlagRegister:
    def __init__(self, *flags):
        self.register = dict.fromkeys(flags, False)


    def __getitem__(self, flag):
        return self.register[flag]


    def __setitem__(self, flag, value):
        self.register[flag] = value


    def set(self, flag):
        self.register[flag] = True
    

    def clear(self, flag):
        self.register[flag] = False


    def clear_all(self):
        self.register = dict.fromkeys(self.register, False)


    def toggle(self, flag):
        self.register[flag] = not self.register[flag]


    def add_flag(self, flag):
        self.register[flag] = False


    def dump(self):
        for flag, value in self.register:
            print(f"{flag}: {value}")