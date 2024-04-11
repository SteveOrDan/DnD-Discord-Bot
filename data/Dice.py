from random import randint


class Dice:
    faces: int

    def throw(self) -> int:
        return randint(1, self.faces)

    def throw_n(self, n) -> int:
        res = 0
        for i in range(n):
            res += self.throw()
        return res


class D4(Dice):
    faces = 4


class D6(Dice):
    faces = 6


class D8(Dice):
    faces = 8


class D10(Dice):
    faces = 10


class D12(Dice):
    faces = 12


class D20(Dice):
    faces = 20


class D100(Dice):
    faces = 100
