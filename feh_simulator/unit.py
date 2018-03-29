from feh_simulator import skill


class Unit(object):
    cnt = 1

    def __init__(self,
                 index=0,
                 team=0,
                 x: int = 0,
                 y: int = 0,
                 unit_file: str = './unit_data/unit_default.txt'):
        self.id = Unit.cnt
        Unit.cnt += 1
        self.x = x
        self.y = y
        self.index: int = index

        with open(unit_file) as f:
            content = f.readlines()

        for i in range(13):
            tmp = content[i].split(sep=' ')
            if i == 0:
                if tmp[0] != "max_hp":
                    raise ValueError('Invalid unit data file: invalid property')
                if tmp[1] != "=":
                    raise ValueError('Invalid unit data file: invalid syntax')
                self.max_hp: int = int(tmp[2])
            elif i == 1:
                if tmp[0] != "atk":
                    raise ValueError('Invalid unit data file: invalid property')
                if tmp[1] != "=":
                    raise ValueError('Invalid unit data file: invalid syntax')
                self.atk: int = int(tmp[2])
            elif i == 2:
                if tmp[0] != "spd":
                    raise ValueError('Invalid unit data file: invalid property')
                if tmp[1] != "=":
                    raise ValueError('Invalid unit data file: invalid syntax')
                self.spd: int = int(tmp[2])
            elif i == 3:
                if tmp[0] != "def":
                    raise ValueError('Invalid unit data file: invalid property')
                if tmp[1] != "=":
                    raise ValueError('Invalid unit data file: invalid syntax')
                self.defence: int = int(tmp[2])
            elif i == 4:
                if tmp[0] != "res":
                    raise ValueError('Invalid unit data file: invalid property')
                if tmp[1] != "=":
                    raise ValueError('Invalid unit data file: invalid syntax')
                self.res: int = int(tmp[2])
            elif i == 5:
                if tmp[0] != "movement_type":
                    raise ValueError('Invalid unit data file: invalid property')
                if tmp[1] != "=":
                    raise ValueError('Invalid unit data file: invalid syntax')
                self.movement_type = skill.MovementType.str2enum(tmp[2].rstrip())
            elif i == 6:
                if tmp[0] != "weapon":
                    raise ValueError('Invalid unit data file: invalid property')
                if tmp[1] != "=":
                    raise ValueError('Invalid unit data file: invalid syntax')
                self.weapon = skill.Weapon.str2enum(tmp[2].rstrip())
            elif i == 7:
                if tmp[0] != "support":
                    raise ValueError('Invalid unit data file: invalid property')
                if tmp[1] != "=":
                    raise ValueError('Invalid unit data file: invalid syntax')
                self.support = skill.Weapon.str2enum(tmp[2].rstrip())
            elif i == 8:
                if tmp[0] != "special":
                    raise ValueError('Invalid unit data file: invalid property')
                if tmp[1] != "=":
                    raise ValueError('Invalid unit data file: invalid syntax')
                self.special = skill.Special.str2enum(tmp[2].rstrip())
            elif i == 9:
                if tmp[0] != "passive_a":
                    raise ValueError('Invalid unit data file: invalid property')
                if tmp[1] != "=":
                    raise ValueError('Invalid unit data file: invalid syntax')
                self.passive_a = skill.PassiveA.str2enum(tmp[2].rstrip())
            elif i == 10:
                if tmp[0] != "passive_b":
                    raise ValueError('Invalid unit data file: invalid property')
                if tmp[1] != "=":
                    raise ValueError('Invalid unit data file: invalid syntax')
                self.passive_b = skill.PassiveB.str2enum(tmp[2].rstrip())
            elif i == 11:
                if tmp[0] != "passive_c":
                    raise ValueError('Invalid unit data file: invalid property')
                if tmp[1] != "=":
                    raise ValueError('Invalid unit data file: invalid syntax')
                self.passive_c = skill.PassiveC.str2enum(tmp[2].rstrip())
            elif i == 12:
                if tmp[0] != "passive_s":
                    raise ValueError('Invalid unit data file: invalid property')
                if tmp[1] != "=":
                    raise ValueError('Invalid unit data file: invalid syntax')
                self.passive_s = skill.PassiveS.str2enum(tmp[2].rstrip())

        self.cur_hp: int = self.max_hp

        self.weapon_type = skill.WEAPON_TO_WEAPON_TYPE[self.weapon]
        self.color = skill.WEAPON_TYPE_TO_COLOR[self.weapon_type]
        self.attack_range = skill.WEAPON_TYPE_TO_ATTACK_RANGE[self.weapon_type]
        self.damage_type = skill.WEAPON_TYPE_TO_DAMAGE_TYPE[self.weapon_type]
        self.movement_range = skill.MOVEMENT_TYPE_TO_MOVEMENT_RANGE[self.movement_type]

        self.is_dead: bool = False
        self.team: int = team
        return

    def get_movement_range(self, surrounding_units: set) -> int:
        """
        return the current movement range of this unit without considering the terrain types
        :param map: the map of current session
        :return:
        """
        # TODO: Currently complex movement type not implemented
        return skill.MOVEMENT_TYPE_TO_MOVEMENT_RANGE[self.movement_type]

    def get_attributes(self):
        return self.max_hp, self.cur_hp, self.atk, self.spd, self.defence, self.res, self.attack_range, self.movement_range

    def render(self):
        print("unit id :", self.id)
        print("location: ", self.x, self.y)
        print("max_hp :", self.max_hp)
        print("current_hp :", self.cur_hp)
        print("atk :", self.atk)
        print("spd :", self.spd)
        print("def :", self.defence)
        print("res :", self.res)
        print("weapon :", self.weapon._name_)
        print("support :", self.support._name_)
        print("special :", self.special._name_)
        print("passive_a :", self.passive_a._name_)
        print("passive_b :", self.passive_b._name_)
        print("passive_c :", self.passive_c._name_)
        print("passive_s :", self.passive_s._name_)
        return
