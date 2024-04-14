import string


class Keyboard:
    def __init__(self, rotor):
        self.right_rotor = rotor
        self.signal = None

    def press(self, letter, case):
        mid = self.right_rotor.neighbour
        slow = mid.neighbour
        if self.right_rotor.inner[0] != self.right_rotor.notch and mid.inner[0] == mid.notch:
            mid.rotate()
        self.right_rotor.rotate()
        self.right_rotor.receive_signal_forward(string.ascii_uppercase.index(letter), case)
