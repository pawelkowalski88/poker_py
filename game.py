from card import Card
from hand import Hand
from hand_description import HandDescription
from player import Player
from collections import Counter
from itertools import groupby
from table import Table
from dealer import Dealer
import random

class Game():

    def __init__(self):
        self.table = []
        self.players = []
        self.players_gen = self.players_generator()
        self.dealer = Dealer(self.table)
        self.finished = False
        self.current_player = None
        self.round_no = 0
        self.game_results = []
        self.small_blind = 5
        self.big_bling = 10
        self.max_bet = 0


    def player_action(self, params):
        if params['Action name'] == 'Bet':
            self.current_player.place_bet(int(params['Amount']))
        if params['Action name'] == 'Call':
            self.current_player.call(params['Max bet'])
        if params['Action name'] == 'Raise':
            self.current_player.raise_bet(params['Max bet'], int(params['Amount']))
        self.check_game_state()

    def check_game_state(self):
        if self.check_betting_fished():
            self.reset_round()
            self.current_player = self.get_next_player()         
            print("Game finished: " + str(self.finished))
            return
        self.current_player = self.get_next_player()
        if not self.current_player:
            self.new_loop()
            self.current_player = self.get_next_player()
            return


    def initialize_game(self):
        self.dealer.deal_cards_to_players(self.players)
        self.check_game_state()
        
    def check_betting_fished(self):
        max_bet = max(map(lambda p: p.bet, self.players))
        self.max_bet = max_bet
        for p in self.players:
            if not p.active or p.folded:
                continue
            if p.bet != max_bet or not p.bet_placed:
                return False
        return True

    def get_game_results(self):
        for p in self.players:
            p.find_hands()
        self.players.sort(reverse=True)
        players_ranking = groupby(self.players, key=lambda x: x.cards.as_values())
        for group, players in players_ranking:
            for p in players:
                self.game_results.append({"Name": p.name,
                "Hands": list(map(lambda h: h.as_name_and_value(),p.cards.hands_list)), 
                "Cards": p.print_cards(),
                "Best hand": p.cards.hands_list[0].as_name_and_value()})
        return self.game_results

    def create_results_ranking(self, players_tab):
        for p in players_tab:
            p.find_hands()


    def add_player(self, name):
        self.players.append(Player(name))

    def get_player(self, name):
        return list(filter(lambda p: p.name == name, self.players))[0]

    def create_default_players(self, number_of_players):
        players_tab = []
        players_tab = [Player("Player " + str(i+1)) for i in range(number_of_players)]
        return players_tab

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


    def new_loop(self):
        self.players_gen=self.players_generator()

    def reset_round(self):
        self.new_loop()
        self.round_no += 1
        self.max_bet = 0
        if self.round_no > 3:
            self.finished = True
        self.dealer.add_new_card_to_table(self.round_no)
        for p in self.players:
            p.bet = 0
            p.bet_placed = False