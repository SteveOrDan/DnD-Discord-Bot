from data.Cost import Cost
from data.Dice import D4, D6, D8
from data.Items.Items import Weapon, WeaponType, WeaponProperty, ArmorType, Armor, ArmorStr, DamageType
from data.Purse import CoinType

weapons = {
    "club": Weapon(WeaponType.SIMPLE_MELEE, "club", Cost(1, CoinType.SP), D4(), 1, DamageType.BLUDGEONING, 2, [WeaponProperty.LIGHT]),
    "dagger": Weapon(WeaponType.SIMPLE_MELEE, "dagger", Cost(2, CoinType.GP), D4(), 1, DamageType.PIERCING, 1, [WeaponProperty.FINESSE, WeaponProperty.LIGHT, WeaponProperty.THROWN_20_60]),

    "shortbow": Weapon(WeaponType.SIMPLE_RANGED, "shortbow", Cost(25, CoinType.GP), D6(), 1, DamageType.PIERCING, 2, [WeaponProperty.AMMUNITION_80_320, WeaponProperty.TWO_HANDED]),
    "dart": Weapon(WeaponType.SIMPLE_RANGED, "dart", Cost(5, CoinType.CP), D4(), 1, DamageType.PIERCING, 0.25, [WeaponProperty.FINESSE, WeaponProperty.THROWN_20_60]),

    "battleaxe": Weapon(WeaponType.MARTIAL_MELEE, "battleaxe", Cost(10, CoinType.GP), D8(), 1, DamageType.SLASHING, 4, [WeaponProperty.VERSATILE]),
    "flail": Weapon(WeaponType.MARTIAL_MELEE, "flail", Cost(10, CoinType.GP), D8(), 1, DamageType.BLUDGEONING, 2, []),

    "crossbow hand": Weapon(WeaponType.MARTIAL_RANGED, "crossbow hand", Cost(75, CoinType.GP), D6(), 1, DamageType.PIERCING, 3, [WeaponProperty.AMMUNITION_30_120, WeaponProperty.LIGHT, WeaponProperty.LOADING]),
    "longbow": Weapon(WeaponType.MARTIAL_RANGED, "longbow", Cost(50, CoinType.GP), D8(), 1, DamageType.PIERCING, 2, [WeaponProperty.AMMUNITION_150_600, WeaponProperty.HEAVY, WeaponProperty.TWO_HANDED]),
}

armors = {
    "padded": Armor(ArmorType.LIGHT, "padded", Cost(5, CoinType.GP), 11, 8),
    "leather": Armor(ArmorType.LIGHT, "leather", Cost(10, CoinType.GP), 11, 10),
    "studded leather": Armor(ArmorType.LIGHT, "studded leather", Cost(45, CoinType.GP), 12, 13),

    "hide": Armor(ArmorType.MEDIUM, "hide", Cost(10, CoinType.GP), 12, 12),
    "chain shirt": Armor(ArmorType.MEDIUM, "chain shirt", Cost(50, CoinType.GP), 13, 20),
    "scale mail": Armor(ArmorType.MEDIUM, "scale mail", Cost(50, CoinType.GP), 14, 45),
    "breastplate": Armor(ArmorType.MEDIUM, "breastplate", Cost(400, CoinType.GP), 14, 20),
    "half plate": Armor(ArmorType.MEDIUM, "half plate", Cost(750, CoinType.GP), 15, 40),

    "ring mail": Armor(ArmorType.HEAVY, "ring mail", Cost(30, CoinType.GP), 14, 40),
    "chain mail": Armor(ArmorType.HEAVY, "chain mail", Cost(75, CoinType.GP), 16, 55, ArmorStr.STR13),
    "splint": Armor(ArmorType.HEAVY, "splint", Cost(200, CoinType.GP), 17, 60, ArmorStr.STR15),
    "plate": Armor(ArmorType.HEAVY, "plate", Cost(1500, CoinType.GP), 18, 65, ArmorStr.STR15),
}

shield = Armor(ArmorType.SHIELD, "shield", Cost(10, CoinType.GP), 2, 6)


def get_item(item_name: str) -> Weapon | Armor | None:
    item_name = item_name.lower()

    item = weapons.get(item_name) or armors.get(item_name)

    if item is None and item_name != shield.name:
        return None

    return item or shield
