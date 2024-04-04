from data.Purse import CoinType


class Cost:

    def __init__(self, value: int, coinType: CoinType):
        self.value = value
        self.coinType = coinType
