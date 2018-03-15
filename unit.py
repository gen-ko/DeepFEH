class Unit(object):
    def __init__(self, team=0, unitId=0):
        self.unitId = unitId
        self.max_hp: int = 40
        self.cur_hp: int = self.max_hp
        self.atk: int = 30
        self.spd: int = 36
        self.defence: int = 25
        self.res: int = 26
        self.attack_range: int = 5
        self.attack_type: bool = 0  # 0: physical, 1: magical
        self.move_range: int = 3
        self.is_dead: bool = 0
        self.color: int = 0  # 0: red, 1: green, 2: blue
        self.team: int = team
