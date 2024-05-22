from CampaignMember import *
from data import MonstersDataBase
from data.Dice import D20
import operator


class Encounter:

    monsters: dict = {}

    initiative_order: list = []

    curr_index = 0

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

        # Create the initiative order
        initiatives = {}

        for user in costants.curr_campaign.campaign_member_list:
            if user.isAdventurer:
                initiative = D20().throw() + user.stats_modifiers[StatTypeEnum.DEX.value]

                initiatives.update({user: initiative})

        for monster in self.monsters.keys():
            initiative = D20().throw() + self.monsters.get(monster).stats_modifiers[StatTypeEnum.DEX.value]
            initiatives.update({monster: initiative})

        sorted_initiatives = sorted(initiatives, key=initiatives.get)

        queue = ""

        # Create the queue of initiatives
        for key in sorted_initiatives:
            self.initiative_order.append(key)

    def get_by_id(self, monster_id: str) -> MonstersDataBase.Monster | None:
        return self.monsters.get(monster_id)

    def get_first_in_order(self) -> str:
        return self.initiative_order[0]

    def get_next_in_order(self) -> str:
        self.curr_index += 1

        if self.curr_index >= len(self.initiative_order):
            self.curr_index = 0

        res = self.initiative_order[self.curr_index]

        return res
    
    def damage(self, monster_id: str, damage: int):
        monster = self.monsters.get(monster_id)

        if monster is None:
            return "Monster not found or already dead."

        monsterHP = monster.take_damage(damage)

        ret_val = ""

        if monsterHP <= 0:
            costants.curr_campaign.curr_encounter.remove(monster_id)
            ret_val += f"{monster.name} has been defeated."
        else:
            ret_val += f"{monster.name} took {damage} damage. Remaining hit points: {monsterHP}."

        return ret_val

    def check_if_encounter_over(self) -> bool:
        for monster in self.monsters:
            if self.monsters.get(monster).HP > 0:
                return False
        return True

    def toString(self) -> str:
        res: str = ""
        for key in self.monsters.keys():
            res += f"{key}: {self.monsters.get(key).name} => HP: {self.monsters.get(key).HP}\n"

        return res

    def initiative_order_to_string(self) -> str:
        res: str = "Initiative order:\n"
        i = 1
        for key in self.initiative_order:
            if isinstance(key, CampaignMember):
                res += f"{i}. {key.member.display_name}\n"
            else:
                res += f"{i}. {key}\n"
            i += 1

        return res

    def remove(self, monster_id: str):
        self.monsters.pop(monster_id)
