import numpy as np


class Action:
    def __init__(self, src_unit, destination, des_unit):
        self.src_unit = src_unit
        self.destination = destination
        self.des_unit = des_unit

    def get_values(self):
        return np.array([self.src_unit.id,
                         self.destination[0],
                         self.destination[1],
                         self.des_unit if self.des_unit is not None else -1])

    def __repr__(self):
        return "src_Id is {}, destination is {}, attack Id is {} \n".format(self.src_unit.id, self.destination,
                                                                         self.des_unit.id if self.des_unit else None)

    def __str__(self):
        return "src_Id is {}, destination is {}, attack Id is {} \n".format(self.src_unit.id, self.destination,
                                                                         self.des_unit.id if self.des_unit else None)
