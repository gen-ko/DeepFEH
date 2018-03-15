

class Unit(object):
    def __init__(self):
        self.max_hp: int = 40
        self.cur_hp: int = self.max_hp
        self.atk: int = 30
        self.spd: int = 36
        self.defence: int = 25
        self.res: int = 26
        self.attack_range: int = 1
        self.attack_type: bool = 0  # 0: physical, 1: magical
        self.move_range: int = 1
        self.is_dead: bool = 0
        return
