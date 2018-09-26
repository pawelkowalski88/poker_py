#Player class
from card import Card
class Player():

    def __init__(self, name):
        self.name = name
        self.score = 0
        self.cards = []

#napisac test
    def calculate_score(self):
        self.score = 0
        for c in self.cards:
            if not c.covered:
                if int(c) == 11:
                    if self.score > 10:
                        self.score += 1
                    else:
                        self.score += 11
                else:
                    self.score += int(c)
    
    def reveal_cards(self):
        for c in self.cards:
            c.covered = False

    def print_cards(self):
        result = ''
        for c in self.cards:
            result += str(c)
        return result