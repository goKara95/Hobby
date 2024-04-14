class Plugboard:
    def __init__(self, pairs=None):
        self.name = "plug"
        self.wiring = {}
        if pairs is not None:
            pairs = pairs.split(" ")
            for pair in pairs:
                self.wiring[pair[0]] = pair[1]
                self.wiring[pair[1]] = pair[0]

    def receive_signal_forward(self, signal):
        return self.wiring.get(signal, signal)

    def backward_pass(self, signal):
        return self.wiring.get(signal, signal)

