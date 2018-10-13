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
        self.all_in_state = False

    def add_card(self, card):
        self.cards.cards.append(card)

    def find_hands(self):
        self.cards.find_hands()
        self.cards.sort_my_hands()

    def place_bet(self, amount):
        if self.balance >= amount:
            self.bet += amount
            self.balance -= amount
            self.bet_placed = True

    def fold(self):
        self.folded = True

    def call(self, max_bet):
        bet_diff = max_bet - self.bet
        if self.balance >= bet_diff:
            self.place_bet(bet_diff)
    
    def all_in(self):
        if self.balance > 0:
            self.place_bet(self.balance)
        else:
            self.check()
        self.all_in_state = True


    def check(self):
        self.bet_placed = True

    def raise_bet(self, raise_amount):
        self.place_bet(raise_amount)        

    def print_cards(self):
        return self.cards.print_cards(False)

    def __gt__(self,other):
        if isinstance(other, Player):
            return self.cards > other.cards

    def __str__(self):
        return self.name + " " + str(self.balance) + " " + self.print_cards() + " bet: " + str(self.bet)

    