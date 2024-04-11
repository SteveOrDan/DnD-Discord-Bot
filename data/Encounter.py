from data import MonstersDataBase


class Encounter:
    monsters: dict

    def __init__(self, enc: str):
        enc = enc.split(", ")

        new_enc = {}

        for elem in enc:
            new_elem = elem.split(":")
            new_enc.update({new_elem[0]: MonstersDataBase.get_monster(new_elem[1])})

        self.monsters = new_enc

    def get_by_id(self, monster_id: str) -> MonstersDataBase.Monster | None:
        return self.monsters.get(monster_id)

    def toString(self) -> str:
        res: str = ""
        for key in self.monsters.keys():
            res += f"{key}: {self.monsters.get(key).name} => HP: {self.monsters.get(key).HP}\n"

        return res
