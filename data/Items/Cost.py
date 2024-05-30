from data.Purse import CoinType


class Cost:

    def __init__(self, value: int, coinType: CoinType):
        self.value = value
        self.coinType = coinType

    def __str__(self):
        return f'{self.value} {self.coinType.name}'

    def times(self, times: int):
        return Cost(self.value * times, self.coinType)
