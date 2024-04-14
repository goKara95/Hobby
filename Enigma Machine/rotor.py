import string


class Rotor:
    def __init__(self, name, ring, key, sequence, notch, neighbour=None, rNeighbour=None):
        self.name = name
        self.key = key
        self.outer = sequence  # right side
        self.inner = list(string.ascii_uppercase)  # left side
        self.notch = notch
        self.neighbour = neighbour
        self.rNeighbour = rNeighbour
        self.rotate_to(key)
        self.ring_settings(ring)

    def ring_settings(self, step):
        notch_pos = self.inner.index(self.notch)
        while step-1 > 0:
            a = self.outer.pop()
            b = self.inner.pop()
            self.outer.insert(0, a)
            self.inner.insert(0, b)
            step -= 1
            self.notch = self.inner[notch_pos]

    def rotate(self):
        a = self.outer.pop(0)
        b = self.inner.pop(0)
        self.outer.append(a)
        self.inner.append(b)
        if b == self.notch and self.neighbour is not None:
            self.neighbour.rotate()

    def rotate_to(self, letter):
        a = self.inner.pop(0)
        b = self.outer.pop(0)
        while a != letter:
            self.inner.append(a)
            self.outer.append(b)
            a = self.inner.pop(0)
            b = self.outer.pop(0)
        self.inner.insert(0, a)
        self.outer.insert(0, b)

    def receive_signal_backward(self, pos, case):
        next_pos = self.outer.index(self.inner[pos])
        if self.rNeighbour is None:
            if case == "l":
                print(string.ascii_uppercase[next_pos].lower(), end="")
            else:
                print(string.ascii_uppercase[next_pos], end="")
        elif self.rNeighbour.name == "plug":
            if self.rNeighbour.wiring.get(string.ascii_uppercase[next_pos]) is None:
                if case == "l":
                    print(string.ascii_uppercase[next_pos].lower(), end="")
                else:
                    print(string.ascii_uppercase[next_pos], end="")
            else:
                if case == "l":
                    print(self.rNeighbour.wiring.get(string.ascii_uppercase[next_pos]).lower(), end="")
                else:
                    print(self.rNeighbour.wiring.get(string.ascii_uppercase[next_pos]), end="")
        else:
            self.rNeighbour.receive_signal_backward(next_pos, case)

    def receive_signal_forward(self, pos, case):
        if self.neighbour.name == "r":
            next_pos = self.inner.index(self.outer[pos])
            reflected = self.neighbour.reflect(next_pos)
            self.receive_signal_backward(reflected, case)
        elif self.rNeighbour.name == "plug":
            if self.rNeighbour.wiring.get(string.ascii_uppercase[pos]) is None:
                next_pos = self.inner.index(self.outer[pos])
                self.neighbour.receive_signal_forward(next_pos, case)
            else:
                pos = string.ascii_uppercase.index(self.rNeighbour.wiring.get(string.ascii_uppercase[pos]))
                next_pos = self.inner.index(self.outer[pos])
                self.neighbour.receive_signal_forward(next_pos, case)

        else:
            next_pos = self.inner.index(self.outer[pos])
            self.neighbour.receive_signal_forward(next_pos, case)


