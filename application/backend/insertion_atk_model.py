import random


class InsertionAtkModel:
    def __init__(self, web3):
        self.web3 = web3
        pass

    def prepare_features(self, transaction_hash):
        pass


    def predict(self):
        return random.choice([0, 1])
