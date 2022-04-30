WIDTH = 32
MASK = (1 << WIDTH) - 1


class Int32(int):
    def __add__(self, other):
        return Int32((int(self) + int(other)) & MASK)

    def __sub__(self, other):
        return Int32((int(self) - int(other)) & MASK)

    def __mul__(self, other):
        return Int32((int(self) * int(other)) & MASK)

    def __invert__(self):
        return Int32(MASK - int(self))

    def __lshift__(self, s):
        l, r = (int(self) << int(s)) & MASK, int(self) >> (WIDTH - int(s))
        return Int32(l | r)

    def __rshift__(self, s):
        l, r = (int(self) << (WIDTH - int(s))) & MASK, int(self) >> int(s)
        return Int32(l | r)
