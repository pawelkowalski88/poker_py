#Player class
from card import Card
from hand import Hand
from table import Table

class Player():

    def __init__(self, name):
        self.name = name
        self.balance = 5000
        self.cards = Hand(None)
        self.bet = 0
        self.bet_placed = False
        self.active = True
        self.folded = False

    def add_card(self, card):
        self.cards.cards.append(card)

    def find_hands(self):
        self.cards.find_hands()
        self.cards.sort_my_hands()

    def place_bet(self, amount):
        if self.balance >= amount:
            self.bet = amount
            self.balance -= amount
            self.bet_placed = True

    def print_cards(self):
        return self.cards.print_cards(False)

    def __gt__(self,other):
        if isinstance(other, Player):
            return self.cards > other.cards

    def __str__(self):
        return self.name + " " + str(self.balance) + " " + self.print_cards()

    