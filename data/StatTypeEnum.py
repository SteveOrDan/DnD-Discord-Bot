from enum import Enum


class StatTypeEnum(Enum):

    NONE = -1, "NONE"
    STR = 0, "STR"
    DEX = 1, "DEX"
    CON = 2, "CON"
    INT = 3, "INT"
    WIS = 4, "WIS"
    CHA = 5, "CHA"

    def __new__(cls, value, name):
        member = object.__new__(cls)
        member._value_ = value
        member.fullname = name
        return member

    def __int__(self):
        return self.value
