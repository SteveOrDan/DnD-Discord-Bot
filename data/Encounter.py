from data import MonstersDataBase


class Encounter:
    monsters: dict

    def __init__(self, enc: str):
        enc = enc.split(", ")

        new_enc = {}

        for elem in enc:
            new_elem = elem.split(":")

            monster_name = new_elem[0]
            monster_count = int(new_elem[1])

            for i in range(monster_count):
                new_enc.update({f"{monster_name}{i + 1}": MonstersDataBase.get_monster(monster_name)})

        self.monsters = new_enc

    def get_by_id(self, monster_id: str) -> MonstersDataBase.Monster | None:
        return self.monsters.get(monster_id)

    def toString(self) -> str:
        res: str = ""
        for key in self.monsters.keys():
            res += f"{key}: {self.monsters.get(key).name} => HP: {self.monsters.get(key).HP}\n"

        return res

    def remove(self, monster_id: str):
        self.monsters.pop(monster_id)
