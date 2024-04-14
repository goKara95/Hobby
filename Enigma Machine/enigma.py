import string


class Enigma:
    def __init__(self, keyboard, plugboard, reflector):
        self.keyboard = keyboard
        self.plugboard = plugboard
        self.reflector = reflector

    def encrypt(self, message):
        for letter in message:
            if letter not in string.ascii_uppercase and letter not in string.ascii_lowercase:
                print(letter, end="")
            elif letter in string.ascii_lowercase:
                self.keyboard.press(letter.upper(), "l")
            else:
                self.keyboard.press(letter, "U")

    def decrypt(self, message):
        self.encrypt(message)
