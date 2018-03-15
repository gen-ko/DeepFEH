from enum import Enum, auto

class WeaponType(Enum):
    RED_SWORD = auto()
    BLUE_LANCE = auto()
    GREEN_AXE = auto()
    COLORLESS_DAGGER = auto()
    COLORLESS_BOW = auto()
    RED_TOME = auto()
    RED_BREATH = auto()
    BLUE_TOME = auto()
    BLUE_BREATH = auto()
    GREEN_TOME = auto()
    GREEN_BREATH = auto()
    COLORLESS_STAFF = auto()


class PassiveA(Enum):
    EMPTY = auto()
    TRIANGLE_ADEPT_1 = auto()
    TRIANGLE_ADEPT_2 = auto()
    TRIANGLE_ADEPT_3 = auto()


class PassiveB(Enum):
    EMPTY = auto()


class PassiveC(Enum):
    EMPTY = auto()


class PassiveS(Enum):
    EMPTY = auto()


class Special(Enum):
    EMPTY = auto()


class Support(Enum):
    EMPTY = auto()


class Weapon(Enum):
    EMPTY = auto()
    RUBY_SWORD = auto()