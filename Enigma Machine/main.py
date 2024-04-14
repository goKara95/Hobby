from sys import argv

from reflector import Reflector
from keyboard import Keyboard
from rotor import Rotor
from plugboard import Plugboard
from enigma import Enigma

rotors = {"I": [list("EKMFLGDQVZNTOWYHXUSPAIBRCJ"), "Q"],
"II": [list("AJDKSIRUXBLHWTMCQGZNPYFVOE"), "E"],
"III": [list("BDFHJLCPRTXVZNYEIWGAKMUSQO"), "V"],
"IV": [list("ESOVPZJAYQUIRHXLNFTGKDCMWB"), "J"],
"V": [list("VZBRGITYUPSDNHLXAWMJQOFECK"), "Z"]}

reflectors = {"A": list("EJMZALYXVBWFCRQUONTSPIKHGD"),
"B": list("YRUHQSLDPXNGOKMIEBFZCWVJAT"),
"C": list("FVPJIAOYEDRZXWGCTKUQSBNMHL")}

f = open(argv[1], "r")
rotor_input = f.readline().strip().split("-")
rflct_input = f.readline().strip()
keys = f.readline().strip()
rings = f.readline().strip().split(",")
pairs = f.readline().strip()

if len(pairs) == 0:
    plBoard = Plugboard()
else:
    plBoard = Plugboard(pairs)
rflct = Reflector(reflectors.get(rflct_input))

slow = Rotor("slow", int(rings[0]), keys[0], rotors.get(rotor_input[0])[0], rotors.get(rotor_input[0])[1], rflct)
mid = Rotor("mid", int(rings[1]), keys[1], rotors.get(rotor_input[1])[0], rotors.get(rotor_input[1])[1], slow)
fast = Rotor("fast", int(rings[2]), keys[2], rotors.get(rotor_input[2])[0], rotors.get(rotor_input[2])[1], mid)

kBoard = Keyboard(fast)
mid.rNeighbour = fast
slow.rNeighbour = mid
fast.rNeighbour = plBoard

machine = Enigma(kBoard, plBoard, rflct)
f.close()

f = open(argv[2], "r")
text = f.read()

if len(argv) == 4 and argv[3] == "-d":
    machine.decrypt(text)
else:
    machine.encrypt(text)
