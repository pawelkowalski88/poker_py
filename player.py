#Player class
from card import Card
from hand import Hand
from table import Table
from jsonconvert import JsonConvert

@JsonConvert.register
class Player(object):

    def __init__(self, name:str = "", balance=5000, cards=None, bet=0, bet_placed=False, 
                active=True, folded=False, all_in_state=False, ready=True):
            self.name = name
            self.balance = balance
            self.cards = cards
            self.bet = bet
            self.bet_placed = bet_placed
            self.active = active
            self.folded = folded
            self.all_in_state = all_in_state
            self.ready = ready

    # def __init__(self, name:str = ""):
    #         self.name = name
    #         self.balance = 5000
    #         self.cards = None
    #         self.bet = 0
    #         self.bet_placed = False
    #         self.active = True
    #         self.folded = False
    #         self.all_in_state = False
    #         self.ready = True

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
            return {'result': 'OK'}
        else:
            return {'result': 'ERROR', 'error_message': 'UPS, not enough funds to bet'}

    def fold(self):
        self.folded = True
        return {'result': 'OK'}

    def call(self, max_bet):
        bet_diff = max_bet - self.bet
        if self.balance >= bet_diff:
            self.place_bet(bet_diff)
            return {'result': 'OK'}
        else:
            return {'result': 'ERROR', 'error_message': 'UPS, not enough funds to call, go all in instead'}
    
    
    def all_in(self):
        if self.balance > 0:
            self.place_bet(self.balance)
            self.all_in_state = True
            return {'result': 'OK'}
        else:
            return {'result': 'ERROR', 'error_message': 'UPS, not enough funds to bet'}


    def check(self):
        self.bet_placed = True
        return {'result': 'OK'}

    def raise_bet(self, raise_amount):
        return self.place_bet(raise_amount)        

    def print_cards(self):
        return self.cards.print_cards(False)

    def reset_player(self):
        self.cards = Hand(None)
        self.bet = 0
        self.bet_placed = False
        self.active = True
        self.folded = False
        self.all_in_state = False
        self.ready = False

    def __gt__(self,other):
        if isinstance(other, Player):
            return self.cards > other.cards

    def __str__(self):
        result = self.name + " " + str(self.balance) + " " + self.print_cards() + " bet: " + str(self.bet) + " folded: " + str(self.folded)
        if self.all_in_state:
            result += " ALL IN"
        return result

    