
from data.Cost import Cost
from data.Dice import D4, D6, D8
from data.Items.Armor import Armor, ArmorType
from data.Items.Weapon import Weapon, WeaponType, WeaponProperty
from data.Purse import CoinType

weapons = {
    "Club": Weapon(WeaponType.SIMPLE_MELEE, "Club", Cost(1, CoinType.SP), D4(), [WeaponProperty.LIGHT]),
    "Dagger": Weapon(WeaponType.SIMPLE_MELEE, "Dagger", Cost(2, CoinType.GP), D4(), [WeaponProperty.FINESSE, WeaponProperty.LIGHT, WeaponProperty.THROWN_20_60]),

    "Shortbow": Weapon(WeaponType.SIMPLE_RANGED, "Shortbow", Cost(25, CoinType.GP), D6(), [WeaponProperty.AMMUNITION_80_320, WeaponProperty.TWO_HANDED]),
    "Dart": Weapon(WeaponType.SIMPLE_RANGED, "Dart", Cost(5, CoinType.CP), D4(), [WeaponProperty.FINESSE, WeaponProperty.THROWN_20_60]),

    "Battleaxe": Weapon(WeaponType.MARTIAL_MELEE, "Battleaxe", Cost(10, CoinType.GP), D8(), [WeaponProperty.VERSATILE]),
    "Flail": Weapon(WeaponType.MARTIAL_MELEE, "Flail", Cost(10, CoinType.GP), D8(), []),

    "Crossbow(hand)": Weapon(WeaponType.MARTIAL_RANGED, "Crossbow(hand)", Cost(75, CoinType.GP), D6(), [WeaponProperty.AMMUNITION_30_120, WeaponProperty.LIGHT, WeaponProperty.LOADING]),
    "Longbow": Weapon(WeaponType.MARTIAL_RANGED, "Longbow", Cost(50, CoinType.GP), D8(), [WeaponProperty.AMMUNITION_150_600, WeaponProperty.HEAVY, WeaponProperty.TWO_HANDED]),
}

armors = {
    "Padded": Armor(ArmorType.LIGHT, "Padded", Cost(5, CoinType.GP), 11),
    "Leather": Armor(ArmorType.LIGHT, "Leather", Cost(10, CoinType.GP), 11),
    "Studded leather": Armor(ArmorType.LIGHT, "Studded leather", Cost(45, CoinType.GP), 12),

    "Hide": Armor(ArmorType.MEDIUM, "Hide", Cost(10, CoinType.GP), 12),
    "Chain shirt": Armor(ArmorType.MEDIUM, "Chain shirt", Cost(50, CoinType.GP), 13),
    "Scale mail": Armor(ArmorType.MEDIUM, "Scale mail", Cost(50, CoinType.GP), 14),

    "Ring mail": Armor(ArmorType.HEAVY, "Ring mail", Cost(30, CoinType.GP), 14),
    "Chain mail": Armor(ArmorType.HEAVY, "Chain mail", Cost(75, CoinType.GP), 16),
    "Plate": Armor(ArmorType.HEAVY, "Plate", Cost(1500, CoinType.GP), 18),
}

shield = Armor(ArmorType.SHIELD, "Shield", Cost(10, CoinType.GP), 2)
