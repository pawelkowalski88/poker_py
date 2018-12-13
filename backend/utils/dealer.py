from card import Card
from table import Table
from hand import Hand
import random



class Dealer():

    def __init__(self, table):
        self.carddeck = []
        self.generate_deck()
        self.table = table

    def generate_deck(self):
        self.carddeck = []
        figures = [2,3,4,5,6,7,8,9,10,"J","Q","K","A"]
        colors = ['♠', '♣', '♥', '♦']
        self.carddeck = [Card(f, c) for f in figures for c in colors]

    def deal_cards_to_players(self, players):
        for p in players:
            if p.balance == 0:
                players.remove(p)
                p.active = False
        for p in players:
            if p.active:
                p.cards = Hand(self.table, [], [])
                p.add_card(self.pick_a_card())
                p.add_card(self.pick_a_card())

    def collect_cards(self, players):
        for p in players:
            p.reset_player()

    def pick_a_card(self):
        card = self.carddeck[random.randint(0,len(self.carddeck)-1)]
        while card.taken == True:
            card = self.carddeck[random.randint(0,len(self.carddeck)-1)]
        card.taken = True
        return card

    def add_new_card_to_table(self, round_no):
        if round_no == 0 or round_no > 3:
            return
        if round_no == 1:
            self.table.append(self.pick_a_card())
            self.table.append(self.pick_a_card())
            self.table.append(self.pick_a_card())
        if round_no > 1:
            self.table.append(self.pick_a_card())