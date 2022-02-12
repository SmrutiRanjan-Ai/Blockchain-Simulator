import imp


import random


class MinerWallet:
    def __init__(self, id, hashrate, balance):
        self.id = id
        self.hashRate = hashrate
        self.balance = balance
        self.bids = {}

    def addBalance(self, balance):
        self.balance += balance

    def debit(self, amount):
        if self.balance < amount:
            raise ValueError("Debit request exceeds the current balance")
        self.balance -= amount

    def bid(self):
        """Steps
        0. Check if you have balance to bid on
        1. Get the current block number X.
        2. You can bid for block X+900 to X+999
        3. Uniformly choose which block to bid until you find the block on which you have not bid on
        4. Choose amount of money you want to bid on the block.
        5. Send the bidding transaction
        """
        min_bid = 1
        # Aggressive bidder.
        if self.balance < min_bid:
            return
        block_number = 1000  # TODO: use method to get current block number.
        target = block_number + random.randint(900, 999)
        while target in self.bids.keys():
            target = block_number + random.randint(900, 999)
        amount = random.uniform(min_bid, self.balance)
        self.debit(amount)
        self.bids[target] = amount
        # TODO: Send bidding transaction
