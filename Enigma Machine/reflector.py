import string


class Reflector:
    def __init__(self, wiring):
        self.name = "r"
        self.wiring = wiring
        self.mappings = string.ascii_uppercase

    def reflect(self, signal):

        pos = self.mappings.index(self.wiring[signal])
        return pos