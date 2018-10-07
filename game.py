from card import Card
from hand import Hand
from hand_description import HandDescription
from player import Player
from collections import Counter
from itertools import groupby
import random

class Game():

    def __init__(self):
        self.table = []
        self.players = []
        self.players_gen = self.players_generator()
        self.carddeck = self.generate_deck()
        self.finished = False
        self.current_player = None
        self.round_no = 0

    def pick_a_card(self):
        card = self.carddeck[random.randint(0,len(self.carddeck)-1)]
        while card.taken == True:
            card = self.carddeck[random.randint(0,len(self.carddeck)-1)]
        card.taken = True
        return card

    def add_player(self, name):
        self.players.append(Player(name))

    def get_player(self, name):
        return list(filter(lambda p: p.name == name, self.players))[0]

    def print_table(self):
        result='\n'
        result+='Table\n'
        for c in self.table:
            result+=str(c)
        result+='\n'
        return result

    def generate_deck(self):
        carddeck = []
        figures = [2,3,4,5,6,7,8,9,"J","Q","K","A"]
        colors = ['♠', '♣', '♥', '♦']
        carddeck = [Card(f, c) for f in figures for c in colors]
        return carddeck

    def deal_cards_to_players(self):
        for p in self.players:
            p.cards = Hand(self.table)
            p.add_card(self.pick_a_card())
            p.add_card(self.pick_a_card())

    def create_default_players(self, number_of_players):
        players_tab = []
        players_tab = [Player("Player " + str(i+1)) for i in range(number_of_players)]
        return players_tab

    def add_new_card_to_table(self):
        if self.round_no > 3:
            self.finished = True
            return
        if self.round_no == 0:
            return
        if self.round_no == 1:
            self.table.append(self.pick_a_card())
            self.table.append(self.pick_a_card())
            self.table.append(self.pick_a_card())
        if self.round_no > 1:
            self.table.append(self.pick_a_card())

    def create_results_ranking(self, players_tab):
        for p in players_tab:
            p.find_hands()

    def players_generator(self):
        for p in self.players:
            yield p

    def get_current_player(self):
        return self.current_player

    def get_next_player(self):
        if self.finished:
            return None
        try:
            self.current_player = next(self.players_gen)
            return self.current_player
        except:
            return None

    def reset_round(self):
        self.players_gen=self.players_generator()
        self.round_no += 1
        self.add_new_card_to_table()

    def check_betting_fished(self):
        max_bet = max(map(lambda p: p.bet, self.players))
        for p in self.players:
            if not p.active or p.folded:
                continue
            if p.bet != max_bet or not p.bet_placed:
                return False
            
        return True

    # def print_results(self, players_tab):
    #     players_tab.sort(reverse=True)
    #     players_ranking = groupby(players_tab, key=lambda x: x.cards.as_values())
    #     for group, players in players_ranking:
    #         for p in players:
    #             print(p.name)
    #             print(p.cards.as_values())
    #             print(p.print_cards())
    #         print()
    #     print(list(map(lambda p: p.name, players_tab)))