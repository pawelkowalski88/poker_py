#Player class
from card import Card
from hand import Hand
from table import Table

class Player():

    def __init__(self, name):
        self.name = name
        self.balance = 0
        self.cards = Hand(None)

    def add_card(self, card):
        self.cards.cards.append(card)

    def find_hands(self):
        self.cards.find_hands()
        self.cards.sort_my_hands()

    def print_cards(self):
        return self.cards.print_cards(False)