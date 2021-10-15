import sys

import global_function as gf

COM = gf.COMMISSION_LIMIT


class Txn:
    """Transaction objects"""

    def __init__(self, sender, receiver, amount, commission):
        self.id = self.get_id()  # Unique transaction Id
        self.sender = sender  # Id_x
        self.receiver = receiver  # Id_y
        self.amount = amount  # C_coins
        self.commission = commission  # max(0.05,(random.random()*COM).round(2))

    def get_id(self):
        id = gf.get_trans_id()
        return id

    def __str__(self):
        return "(" + str(self.sender) + ' pays ' + str(self.receiver) + " " + str(self.amount) + ")"
