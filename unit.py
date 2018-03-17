from enum import Enum

import skill


class Color(Enum):
    RED = 0
    GREEN = 1
    BLUE = 2


class DamageType(Enum):
    PHYSICAL = 0
    MAGICAL = 1


class Unit(object):
    def __init__(self, index=0, team=0,
                 skill_a=skill.PassiveA.EMPTY,
                 skill_b=skill.PassiveB.EMPTY,
                 skill_c=skill.PassiveC.EMPTY,
                 skill_s=skill.PassiveS.EMPTY,
                 skill_weapon=skill.Weapon.EMPTY,
                 skill_support=skill.Support.EMPTY,
                 skill_special=skill.Special.EMPTY):
        self.index: int = index
        self.max_hp: int = 40
        self.cur_hp: int = self.max_hp
        self.atk: int = 30
        self.spd: int = 36
        self.defence: int = 25
        self.res: int = 26
        self.attack_range: int = 1
        self.damage_type = DamageType.PHYSICAL  # 0: physical, 1: magical
        self.weapon_type = skill.WeaponType.RED_SWORD
        self.move_range: int = 1
        self.is_dead: bool = 0
        self.color = Color.RED  # 0: red, 1: green, 2: blue
        self.team: int = team
        self.skill_a = skill_a
        self.skill_b = skill_b
        self.skill_c = skill_c
        self.skill_s = skill_s
        self.skill_weapon = skill_weapon
        self.skill_support = skill_support
        self.skill_special = skill_special
        return

    def get_attributes(self):
        return self.max_hp, self.cur_hp, self.atk, self.spd, self.defence, self.res, self.attack_range, self.move_range
