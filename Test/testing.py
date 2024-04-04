from unittest import TestCase

from data.Purse import Purse, CoinType


class Testing(TestCase):

    purse = Purse([0, 3, 0, 0])

    def test_remove(self):

        self.purse.remove(CoinType.CP.value, 1)
        self.purse.getPurse()
