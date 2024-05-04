import random


class InsertionAtkHeuristics:
    def __init__(self):
        pass

    def get_transactions(self):
        r = random.choice([0, 1])

        if r == 0:
            return []
        else:
            return [{
                'transaction': {
                    'hash': 123
                }
            }]
