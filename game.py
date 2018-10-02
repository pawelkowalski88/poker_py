from card import Card
from hand import Hand
from hand_description import HandDescription
from player import Player
from itertools import groupby
import random

class Game():

    def __init__(self):
        self.table = []
        self.players = {}
        self.carddeck = self.generate_deck()
        self.finished = False

    def pick_a_card(self):
        card = self.carddeck[random.randint(0,len(self.carddeck)-1)]
        while card.taken == True:
            card = self.carddeck[random.randint(0,len(self.carddeck)-1)]
        card.taken = True
        return card

    def add_player(self, name):
        self.players[name] = Player(name)

    def get_player(self, name):
        return self.players[name]

    def print_table(self):
        result='\n'
        result+='Table\n'
        for c in self.table:
            result+=str(c)
        result+='\n'
        return result

    def generate_deck(self):
        carddeck = []
        for i in [2,3,4,5,6,7,8,9,"J","Q","K","A"]:
            for c in ['♠', '♣', '♥', '♦']:
                carddeck.append(Card(i, c))
        return carddeck

    def deal_cards_to_players(self):
        for k, p in self.players.items():
            p.cards = Hand(self.table)
            p.add_card(self.pick_a_card())
            p.add_card(self.pick_a_card())

    def create_default_players(self, number_of_players):
        player_tab = []
        for i in range(number_of_players):  
            player_tab.append(Player("Player " + str(i+1)))
        return player_tab

    def add_new_card_to_table(self):
        self.table.append(self.pick_a_card())
        if len(self.table)>2:
            self.finished = True

    def create_results_ranking(self, players_tab):
        for p in players_tab:
            p.find_hands()

    def print_results(self, players_tab):
        players_tab.sort(reverse=True)
        players_ranking = groupby(players_tab, key=lambda x: x.cards.as_values())
        for group, players in players_ranking:
            for p in players:
                print(p.name)
                print(p.cards.as_values())
                print(p.print_cards())
            print()
        print(list(map(lambda p: p.name, players_tab)))