from enum import Enum, auto

class Color(Enum):
    RED = auto()
    GREEN = auto()
    BLUE = auto()
    COLORLESS = auto()

class MovementType(Enum):
    INFANTRY = auto()
    ARMORED = auto()
    CAVALRY = auto()
    FLYING = auto()
    def str2enum(s: str):
        for i in MovementType:
            if i.__dict__['_name_'] == s:
                return i
        raise ValueError('Invalid movement_type name: ', s)

class DamageType(Enum):
    PHYSICAL = auto()
    MAGICAL = auto()

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
    DISTANT_COUNTER = auto()
    @staticmethod
    def str2enum(s: str):
        for i in PassiveA:
            if i.__dict__['_name_'] == s:
                return i
        raise ValueError('Invalid passive_c name:', s)


class PassiveB(Enum):
    EMPTY = auto()
    CANCEL_AFFINITY_1 = auto()
    CANCEL_AFFINITY_2 = auto()
    CANCEL_AFFINITY_3 = auto()
    @staticmethod
    def str2enum(s: str):
        for i in PassiveB:
            if i.__dict__['_name_'] == s:
                return i
        raise ValueError('Invalid passive_b name:', s)


class PassiveC(Enum):
    EMPTY = auto()
    @staticmethod
    def str2enum(s: str):
        for i in PassiveC:
            if i.__dict__['_name_'] == s:
                return i
        raise ValueError('Invalid passive_c name:', s)

class PassiveS(Enum):
    EMPTY = auto()
    @staticmethod
    def str2enum(s: str):
        for i in PassiveS:
            if i.__dict__['_name_'] == s:
                return i
        raise ValueError('Invalid passive_s name')


class Special(Enum):
    EMPTY = auto()
    @staticmethod
    def str2enum(s: str):
        for i in Special:
            if i.__dict__['_name_'] == s:
                return i
        raise ValueError('Invalid special name')



class Support(Enum):
    EMPTY = auto()
    @staticmethod
    def str2enum(s: str):
        for i in Support:
            if i.__dict__['_name_'] == s:
                return i
        raise ValueError('Invalid support name')


class Weapon(Enum):
    EMPTY = auto()

    RUBY_SWORD_PLUS = auto()
    RAUTHRRAVEN_PLUS = auto()

    EMERALD_AXE_PLUS = auto()
    GRONNRAVEN_PLUS = auto()

    SAPPHIRE_LANCE_PLUS = auto()
    BLARRAVEN_PLUS = auto()

    BRAVE_LANCE_PLUS = auto()

    SILVER_DAGGER_PLUS = auto()
    @staticmethod
    def str2enum(s: str):
        for i in Weapon:
            if i.__dict__['_name_'] == s:
                return i
        raise ValueError('Invalid weapon name')
    @staticmethod
    def get_atk(weapon):
        if weapon == Weapon.SILVER_DAGGER_PLUS:
            return 10


WEAPON_TO_WEAPON_TYPE = {
    Weapon.EMPTY: WeaponType.COLORLESS_STAFF,
    Weapon.RUBY_SWORD_PLUS: WeaponType.RED_SWORD,
    Weapon.RAUTHRRAVEN_PLUS: WeaponType.RED_TOME,
    Weapon.EMERALD_AXE_PLUS: WeaponType.GREEN_AXE,
    Weapon.GRONNRAVEN_PLUS: WeaponType.GREEN_TOME,
    Weapon.SAPPHIRE_LANCE_PLUS: WeaponType.BLUE_LANCE,
    Weapon.BLARRAVEN_PLUS: WeaponType.GREEN_TOME
}

WEAPON_TYPE_TO_COLOR = {
    WeaponType.RED_SWORD: Color.RED,
    WeaponType.RED_TOME: Color.RED,
    WeaponType.RED_BREATH: Color.RED,
    WeaponType.GREEN_AXE: Color.GREEN,
    WeaponType.GREEN_TOME: Color.GREEN,
    WeaponType.GREEN_BREATH: Color.GREEN,
    WeaponType.BLUE_LANCE: Color.BLUE,
    WeaponType.BLUE_TOME: Color.BLUE,
    WeaponType.BLUE_BREATH: Color.BLUE,
    WeaponType.COLORLESS_BOW: Color.COLORLESS,
    WeaponType.COLORLESS_DAGGER: Color.COLORLESS,
    WeaponType.COLORLESS_STAFF: Color.COLORLESS
}

WEAPON_TYPE_TO_DAMAGE_TYPE = {
    WeaponType.RED_SWORD: DamageType.PHYSICAL,
    WeaponType.GREEN_AXE: DamageType.PHYSICAL,
    WeaponType.BLUE_LANCE: DamageType.PHYSICAL,
    WeaponType.RED_TOME: DamageType.MAGICAL,
    WeaponType.GREEN_TOME: DamageType.MAGICAL,
    WeaponType.BLUE_TOME: DamageType.MAGICAL,
    WeaponType.RED_BREATH: DamageType.MAGICAL,
    WeaponType.GREEN_BREATH: DamageType.MAGICAL,
    WeaponType.BLUE_BREATH: DamageType.MAGICAL,
    WeaponType.COLORLESS_BOW: DamageType.PHYSICAL,
    WeaponType.COLORLESS_DAGGER: DamageType.PHYSICAL,
    WeaponType.COLORLESS_STAFF: DamageType.MAGICAL
}

WEAPON_TYPE_TO_ATTACK_RANGE = {
    WeaponType.RED_SWORD: 1,
    WeaponType.GREEN_AXE: 1,
    WeaponType.BLUE_LANCE: 1,
    WeaponType.RED_TOME: 2,
    WeaponType.GREEN_TOME: 2,
    WeaponType.BLUE_TOME: 2,
    WeaponType.RED_BREATH: 1,
    WeaponType.GREEN_BREATH: 1,
    WeaponType.BLUE_BREATH: 1,
    WeaponType.COLORLESS_BOW: 2,
    WeaponType.COLORLESS_DAGGER: 2,
    WeaponType.COLORLESS_STAFF: 2
}

MOVEMENT_TYPE_TO_MOVEMENT_RANGE = {
    MovementType.INFANTRY: 2,
    MovementType.CAVALRY: 3,
    MovementType.ARMORED: 1,
    MovementType.FLYING: 2
}

COLOR_ADVANTAGE = {
    (Color.RED, Color.RED): 0.0,
    (Color.RED, Color.GREEN): 0.2,
    (Color.RED, Color.BLUE): -0.2,
    (Color.RED, Color.COLORLESS): 0.0,
    (Color.GREEN, Color.RED): -0.2,
    (Color.GREEN, Color.GREEN): 0.0,
    (Color.GREEN, Color.BLUE): 0.2,
    (Color.GREEN, Color.COLORLESS): 0.0,
    (Color.BLUE, Color.RED): 0.2,
    (Color.BLUE, Color.GREEN): -0.2,
    (Color.BLUE, Color.BLUE): 0.0,
    (Color.BLUE, Color.COLORLESS): 0.0,
    (Color.COLORLESS, Color.RED): 0.0,
    (Color.COLORLESS, Color.GREEN): 0.0,
    (Color.COLORLESS, Color.BLUE): 0.0,
    (Color.COLORLESS, Color.COLORLESS): 0.0
}

RAVEN_TOMES = {
    Weapon.BLARRAVEN_PLUS,
    Weapon.GRONNRAVEN_PLUS,
    Weapon.RAUTHRRAVEN_PLUS
}