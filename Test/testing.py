from unittest import TestCase

from RaceView import RaceTypeEnum
from data.Purse import Purse, CoinType


class Testing(TestCase):

    purse = Purse([0, 50, 0, 0])

    def test_remove(self):

        self.purse.add(25, CoinType.CP.value)
        self.purse.getPurse()
