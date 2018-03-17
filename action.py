class Action:
    def __init__(self, src_unit, destination, des_unit):
        self.src_unit = src_unit
        self.destination = destination
        self.des_unit = des_unit

    def __repr__(self):
        return "src_Id is {}, destination is {}, attack Id is {}".format(self.src_unit.index, self.destination,
                                                                         self.des_unit.index if self.des_unit else None)

    def __str__(self):
        return "src_Id is {}, destination is {}, attack Id is {}".format(self.src_unit.index, self.destination,
                                                                         self.des_unit.index if self.des_unit else None)
