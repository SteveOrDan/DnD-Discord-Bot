import enum


class MonsterState(enum.Enum):
    ALIVE = 0
    DEAD = 1


class Monster:
    def __init__(self, name: str, AC: int, HP: int, challenge: float, xp: int):
        self.name = name
        self.AC = AC
        self.HP = HP
        self.challenge = challenge
        self.xp = xp

    def take_damage(self, damage) -> MonsterState:
        self.HP -= damage
        if self.HP <= 0:
            return MonsterState.DEAD
        else:
            return MonsterState.ALIVE


monsters = {
    "frog": Monster("frog", 11, 1, 0, 0),
    "scorpion": Monster("scorpion", 11, 1, 0, 10),
    "bandit": Monster("bandit", 12, 11, 0.125, 25),
    "goblin": Monster("goblin", 15, 7, 0.25, 50),
    "orc": Monster("orc", 13, 15, 0.5, 100),
    "ghoul": Monster("ghoul", 12, 22, 1, 200),
    "ogre": Monster("ogre", 11, 59, 2, 450),
    "doppelganger": Monster("doppelganger", 14, 52, 3, 700),
    "young green dragon": Monster("young green dragon", 18, 136, 8, 3900),
    "adult red dragon": Monster("adult red dragon", 19, 256, 17, 18000),
}


def get_monster(monster_name: str) -> Monster | None:
    monster = monsters.get(monster_name.lower())
    if monster is None:
        return None
    return monster
