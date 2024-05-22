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

    def __str__(self):
        return f"d{self.faces}"


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


def dice_from_int(n: int):
    if n == 4:
        return D4()
    elif n == 6:
        return D6()
    elif n == 8:
        return D8()
    elif n == 10:
        return D10()
    elif n == 12:
        return D12()
    elif n == 20:
        return D20()
    elif n == 100:
        return D100()
    else:
        return None
