import math
import enum


def enum_from_str(coin_type: str):
    coins = {
        "PP": CoinType.PP,
        "GP": CoinType.GP,
        "SP": CoinType.SP,
        "CP": CoinType.CP
    }

    return coins.get(coin_type)


class CoinType(enum.Enum):
    PP = 0
    GP = 1
    SP = 2
    CP = 3

    def __str__(self):
        match self.value:
            case 0:
                return "PP"
            case 1:
                return "GP"
            case 2:
                return "SP"
            case 3:
                return "CP"


class Purse:
    def __init__(self, purse: [int]):
        if purse is None or len(purse) != 4:
            self.purse = [0, 0, 0, 0]
        else:
            new_purse = []
            for val in purse:
                new_purse.append(int(val))

            self.purse = new_purse

    def add(self, amount: int, coinType: int):
        if coinType != 0 and self.purse[coinType] + amount >= 10:
            self.add(coinType - 1, math.floor((amount + self.purse[coinType])/10))
            self.purse[coinType] = (self.purse[coinType] + amount) % 10
        else:
            self.purse[coinType] += amount

    def remove(self, amount: int, coinType: int):
        if self.purse[coinType] < amount:
            if coinType == 0 or not self.remove(amount // 10 + 1, coinType - 1):
                return False
            self.purse[coinType] += 10 * (amount // 10 + 1)
        self.purse[coinType] -= amount
        return True

    def get(self, coinType: CoinType):
        return self.purse[coinType.value]

    def getPurse(self):
        return self.purse

    def toString(self):
        return f'{self.purse[0]} PP, {self.purse[1]} GP, {self.purse[2]} SP, {self.purse[3]} CP'
