import math
import enum


class CoinType(enum.Enum):
    PP = 0
    GP = 1
    SP = 2
    CP = 3


class Purse:
    def __init__(self, purse: list):
        if purse is None or len(purse) != 4:
            self.purse = [0, 0, 0, 0]
        else:
            self.purse = purse

    def add(self, coinType: int, amount: int):
        if coinType != 0 and self.purse[coinType] + amount >= 10:
            self.add(coinType - 1, math.floor((amount + self.purse[coinType])/10))
            self.purse[coinType] = (self.purse[coinType] + amount) % 10
        else:
            self.purse[coinType] += amount

    def remove(self, coinType: int, amount: int):
        if self.purse[coinType] < amount:
            if coinType == 0:
                return False
            else:
                if self.remove(coinType - 1, math.ceil((amount - self.purse[coinType])/10)):
                    self.purse[coinType] = self.purse[coinType] + (math.ceil((amount - self.purse[coinType])/10)) * 10 - amount
                    return True
                else:
                    return False
        else:
            self.purse[coinType] -= amount
            return True

    def get(self, coinType: CoinType):
        return self.purse[coinType.value]

    def getPurse(self):
        return self.purse
