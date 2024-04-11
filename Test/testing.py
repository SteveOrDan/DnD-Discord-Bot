from unittest import TestCase

from CampaignMember import AdvClass
from data.Purse import Purse, CoinType


class Testing(TestCase):

    purse = Purse([0, 50, 0, 0])

    def test_remove(self):

        print(AdvClass.CLERIC.get_name())

        print(4//4)

        self.purse.add(25, CoinType.CP.value)
        self.purse.getPurse()
