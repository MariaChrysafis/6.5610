import galois
import numpy as np
def print_condense (arr: list[int]) :
    for x in arr :
        print(x, end="")
    print()
class XORBasis : # maintains a set of linearly independent binary strings
    bitstrings = []
    def xor (self, a, b) -> list[int]:
        assert len(a) == len(b)
        res = [0] * len(a)
        for i in range(len(a)) :
            res[i] = a[i] ^ b[i]
        return res

    def bigger (self, a, b) -> bool: 
        assert len(a) == len(b)
        for i in range(len(a)) :
            if a[i] > b[i] :
                return True # a is bigger
            if a[i] < b[i] :
                return False
    def add (self, plaintext: list[int], ciphertext: list[int]) -> list[int] :
        for (p, c) in self.bitstrings :
            if self.bigger(plaintext, self.xor(p, plaintext)) :
                plaintext = self.xor(plaintext, p)
                ciphertext = self.xor(ciphertext, c)
        if self.bigger(plaintext, [0] * len(plaintext)) :
            self.bitstrings.append((plaintext, ciphertext))
            return ciphertext
        return ciphertext

    def __init__(self) :
        self.bitstrings = []

def to_int (c: chr) -> int :
    if '0' <= c <= '9' :
        return ord(c) - ord('0')
    # alphanumeric
    c = 10 + ord(c) - ord('a')
    return c

def get_binary (x: int) -> list[int]  :
    x = to_int(chr(x))
    arr = []
    for i in range(4) : 
        arr.append((x & (1 << i)) >> i)
    return arr
datatext = open("data.txt", "rb").read()
first_char_ascii = datatext[0]
tot = []
tot.append([[1], []])
y = 0
xorbasis = XORBasis()
for x in list(datatext) :
    if x == ord('\n') :
        tot.append([[1], []])
        y = 0
    elif x == ord(' ') :
        y = 1
        continue
    else :
        for res in get_binary(x) :
            tot[-1][y].append(res)
if len(tot[-1][1]) == 0 :
    tot.pop()

times = 8
for x in range(len(tot) - times) :
    xorbasis.add(tot[x][0], [tot[x][1][0]])
for x in range(times) :
    print(xorbasis.add(tot[len(tot) - x - 1][0], [0]), tot[len(tot) - x - 1][1][0])

print(len(xorbasis.bitstrings))

cipher = open("ciphertext.txt", "rb").read()
print(len(cipher))
for x in cipher :
    print(x, end=" ")
