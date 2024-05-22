from CampaignMember import *
from data.Dice import D4


class Light:
    def __init__(self):
        self.name = "Light"
        self.level = 0
        self.cast_time = "1 action"
        self.cast_range = "Touch"
        self.components = "V, M (a firefly or phosphorescent moss)"
        self.duration = "1 hour"
        self.description = "You touch one object that is no larger than 10 feet in any dimension. " \
                           "Until the spell ends, the object sheds bright light in a 20-foot radius and dim light for an additional 20 feet. " \
                           "The light can be colored as you like. Completely covering the object with something opaque blocks the light. " \
                           "The spell ends if you cast it again or dismiss it as an action."

    @staticmethod
    def cast(caster: CampaignMember, params: str):
        if params is None or params == "":
            return "You need to specify an object to cast Light on."
        return f"Success! You cast Light on {params}."

    def __str__(self):
        return f"Name: {self.name}\n" \
               f"Level: {self.level}\n" \
               f"Cast time: {self.cast_time}\n" \
               f"Cast range: {self.cast_range}\n" \
               f"Components: {self.components}\n" \
               f"Duration: {self.duration}\n" \
               f"Description: {self.description}\n"


class Resistance:
    def __init__(self):
        self.name = "Resistance"
        self.level = 0
        self.cast_time = "1 action"
        self.cast_range = "Touch"
        self.components = "V, S, M (a miniature cloak)"
        self.duration = "1 round"
        self.description = "You touch one willing creature. Once before the spell ends, the target can roll a d4 and add the number rolled to one saving throw of its choice. It can roll the die before or after making the saving throw. The spell then ends."

    @staticmethod
    def cast(caster: CampaignMember, params: str):
        roll = D4().throw()
        return f"Success! You cast Resistance on {params}. {params} can roll a d4 and add the number rolled to one saving throw of its choice. It can roll the die before or after making the saving throw. The spell then ends. You rolled a {roll}."

    def __str__(self):
        return f"Name: {self.name}\n" \
               f"Level: {self.level}\n" \
               f"Cast time: {self.cast_time}\n" \
               f"Cast range: {self.cast_range}\n" \
               f"Components: {self.components}\n" \
               f"Duration: {self.duration}\n" \
               f"Description: {self.description}\n"


class MageHand:
    def __init__(self):
        self.name = "Mage hand"
        self.level = 0
        self.cast_time = "1 action"
        self.cast_range = "30 feet"
        self.components = "V, S"
        self.duration = "1 minute"
        self.description = "A spectral, floating hand appears at a point you choose within range. " \
                           "The hand lasts for the duration or until you dismiss it as an action. " \
                           "The hand vanishes if it is ever more than 30 feet away from you or if you cast this spell again. " \
                           "You can use your action to control the hand. You can use the hand to manipulate an object, open an unlocked door or container, stow or retrieve an item from an open container, or pour the contents out of a vial. " \
                           "You can move the hand up to 30 feet each time you use it. " \
                           "The hand can't attack, activate magic items, or carry more than 10 pounds."

    @staticmethod
    def cast(caster: CampaignMember, params: str):
        return "You successfully cast Mage hand."

    def __str__(self):
        return f"Name: {self.name}\n" \
               f"Level: {self.level}\n" \
               f"Cast time: {self.cast_time}\n" \
               f"Cast range: {self.cast_range}\n" \
               f"Components: {self.components}\n" \
               f"Duration: {self.duration}\n" \
               f"Description: {self.description}\n"


class SpareTheDying:
    def __init__(self):
        self.name = "Spare the dying"
        self.level = 0
        self.cast_time = "1 action"
        self.cast_range = "Touch"
        self.components = "V, S"
        self.duration = "Instantaneous"
        self.description = ("You touch a living creature that has 0 hit points. The creature becomes stable. "
                            "This spell has no effect on undead or constructs.")

    @staticmethod
    def cast(caster: CampaignMember, params: str):
        if params is None or params == "":
            return "You need to specify an object to cast \"Spare the dying\" on."

        # caster.prepared_spells.remove("Spare the dying")

        return f"You successfully cast Spare the dying on {params}."

    def __str__(self):
        return f"Name: {self.name}\n" \
               f"Level: {self.level}\n" \
               f"Cast time: {self.cast_time}\n" \
               f"Cast range: {self.cast_range}\n" \
               f"Components: {self.components}\n" \
               f"Duration: {self.duration}\n" \
               f"Description: {self.description}\n"


class DetectMagic:
    def __init__(self):
        self.name = "Detect magic"
        self.level = 1
        self.cast_time = "1 action"
        self.cast_range = "Self"
        self.components = "V, S"
        self.duration = "Up to 10 minutes"
        self.description = "For the duration, you sense the presence of magic within 30 feet of you. " \
                           "If you sense magic in this way, you can use your action to see a faint aura around any visible " \
                           "creature or object in the area that bears magic, and you learn its school of magic, if any. " \
                           "The spell can penetrate most barriers, but it is blocked by 1 foot of stone, 1 inch of common metal, " \
                           "a thin sheet of lead, or 3 feet of wood or dirt."

    @staticmethod
    def cast(caster: CampaignMember, params: str):
        caster.curr_spell_slots -= 1

        return "You successfully cast Detect magic."

    def __str__(self):
        return f"Name: {self.name}\n" \
               f"Level: {self.level}\n" \
               f"Cast time: {self.cast_time}\n" \
               f"Cast range: {self.cast_range}\n" \
               f"Components: {self.components}\n" \
               f"Duration: {self.duration}\n" \
               f"Description: {self.description}\n"


class HealingWord:
    def __init__(self):
        self.name = "Healing word"
        self.level = 1
        self.cast_time = "1 bonus action"
        self.cast_range = "60 feet"
        self.components = "V"
        self.duration = "Instantaneous"
        self.description = (
            "A creature of your choice that you can see within range regains hit points equal to 1d4 + your "
            "spellcasting ability modifier. This spell has no effect on undead or constructs.")

    @staticmethod
    def cast(caster: CampaignMember, params: str):
        curr_user = None
        for user in costants.curr_campaign.campaign_member_list:
            if user.member.display_name == params:
                curr_user = user

        if curr_user is None:
            return "You need to specify a valid player to cast Healing word on."

        heal = D4().throw() + curr_user.stats_modifiers[StatTypeEnum.WIS.value]

        curr_user.heal(heal)

        caster.curr_spell_slots -= 1

        return f"You successfully cast Healing word on {params}. {params} healed for {heal} HP."

    def __str__(self):
        return f"Name: {self.name}\n" \
               f"Level: {self.level}\n" \
               f"Cast time: {self.cast_time}\n" \
               f"Cast range: {self.cast_range}\n" \
               f"Components: {self.components}\n" \
               f"Duration: {self.duration}\n" \
               f"Description: {self.description}\n"


class Prestidigitation:
    def __init__(self):
        self.name = "Prestidigitation"
        self.level = 1
        self.cast_time = "1 action"
        self.cast_range = "10 feet"
        self.components = "V, S"
        self.duration = "Up to 1 hour"
        self.effect1 = "You create an instantaneous, harmless sensory effect, such as a shower of sparks, a puff of wind, faint musical notes, or an odd odor."
        self.effect2 = "You instantaneously light or snuff out a candle, a torch, or a small campfire."
        self.effect3 = "You instantaneously clean or soil an object no larger than 1 cubic foot."
        self.effect4 = "You chill, warm, or flavor up to 1 cubic foot of nonliving material for 1 hour."
        self.effect5 = "You make a color, a small mark, or a symbol appear on an object or a surface for 1 hour."
        self.effect6 = "You create a nonmagical trinket or an illusory image that can fit in your hand and that lasts until the end of your next turn."
        self.description = "This spell is a minor magical trick that novice spellcasters use for practice. You create one of the following magical effects within range: " \
                           f"\n1. {self.effect1}" \
                           f"\n2. {self.effect2}" \
                           f"\n3. {self.effect3}" \
                           f"\n4. {self.effect4}" \
                           f"\n5. {self.effect5}" \
                           f"\n6. {self.effect6}"

    @staticmethod
    def cast(caster: CampaignMember, params: str):
        choices_dict = {
            "1": "You create an instantaneous, harmless sensory effect, such as a shower of sparks, a puff of wind, faint musical notes, or an odd odor.",
            "2": "You instantaneously light or snuff out a candle, a torch, or a small campfire.",
            "3": "You instantaneously clean or soil an object no larger than 1 cubic foot.",
            "4": "You chill, warm, or flavor up to 1 cubic foot of nonliving material for 1 hour.",
            "5": "You make a color, a small mark, or a symbol appear on an object or a surface for 1 hour.",
            "6": "You create a nonmagical trinket or an illusory image that can fit in your hand and that lasts until the end of your next turn."
        }

        caster.curr_spell_slots -= 1

        return choices_dict.get(params, "Unable to cast Prestidigitation without a set choice. (Choose from 1 to 6)")

    def __str__(self):
        return f"Name: {self.name}\n" \
               f"Level: {self.level}\n" \
               f"Cast time: {self.cast_time}\n" \
               f"Cast range: {self.cast_range}\n" \
               f"Components: {self.components}\n" \
               f"Duration: {self.duration}\n" \
               f"Description: {self.description}\n"


class MagicMissile:
    def __init__(self):
        self.name = "Magic missile"
        self.level = 1
        self.cast_time = "1 action"
        self.cast_range = "120 feet"
        self.components = "V, S"
        self.duration = "Instantaneous"
        self.description = ("You create three glowing darts of magical force. Each dart hits a creature of your choice that "
                            "you can see within range. A dart deals 1d4 + 1 force damage to its target. The darts all strike "
                            "simultaneously, and you can direct them to hit one creature or several.")

    @staticmethod
    def cast(caster: CampaignMember, params: str):
        targets = params.split(", ")
        if len(targets) != 3:
            return "You need to specify 3 targets to cast Magic missile on."

        caster.curr_spell_slots -= 1

        if costants.curr_campaign.curr_encounter is None:
            return "You cast Magic missile, but there are no monsters to target."
        else:
            ret_str = ""

            for target in targets:
                damage = D4().throw() + 1

                ret_str += costants.curr_campaign.curr_encounter.damage(target, damage) + "\n"

                if costants.curr_campaign.curr_encounter.check_if_encounter_over():
                    ret_str += "The encounter has been cleared"
                    break

            if not costants.curr_campaign.curr_encounter.check_if_encounter_over():
                ret_str += "It's " + costants.curr_campaign.curr_encounter.get_next_in_order() + "'s turn."

            return ret_str

    def __str__(self):
        return f"Name: {self.name}\n" \
               f"Level: {self.level}\n" \
               f"Cast time: {self.cast_time}\n" \
               f"Cast range: {self.cast_range}\n" \
               f"Components: {self.components}\n" \
               f"Duration: {self.duration}\n" \
               f"Description: {self.description}\n"


spell_dic = {
    # level 0
    "light": Light(),
    "resistance": Resistance(),
    "mage hand": MageHand(),
    # level 1
    "spare the dying": SpareTheDying(),
    "detect magic": DetectMagic(),
    "healing word": HealingWord(),
    "prestidigitation": Prestidigitation(),
    "magic missile": MagicMissile()
}


def get_spell(spell_name: str) -> Light | Resistance | MageHand | SpareTheDying | DetectMagic | HealingWord | Prestidigitation | MagicMissile | None:
    spell_name = spell_name.lower()

    return spell_dic.get(spell_name)
