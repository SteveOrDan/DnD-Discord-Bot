from unittest import TestCase

from CampaignMember import AdvClass
from data.Purse import Purse, CoinType, enum_from_str


class Testing(TestCase):

    purse = Purse([0, 50, 0, 0])

    def test_remove(self):
        self.purse.add(25, CoinType.CP.value)
        print(self.purse.getPurse())
