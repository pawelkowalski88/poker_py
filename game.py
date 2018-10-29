from card import Card
from hand import Hand
from hand_description import HandDescription
from player import Player
from collections import Counter
from itertools import groupby
from table import Table
from dealer import Dealer
import available_action_helper
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
        self.game_results_rich = {}
        self.small_blind = 5
        self.big_blind = 10
        self.pot = 0
        self.max_bet = 0
        self.started = False
        self.round_finished = False
        self.no_playing = 0
        self.no_starting = 0
        self.initialization = False


    def player_action(self, params):
        if not self.current_player.ready and not params['Action name'] == 'Confirm ready':
            return {'result': 'ERROR', 'error_message': 'The game has not yet started'}

        result = {}
        if params['Action name'] == 'Bet':
            result = self.current_player.place_bet(int(params['Value']))
        if params['Action name'] == 'Call':
            result = self.current_player.call(self.max_bet)
        if params['Action name'] == 'Check':
            result = self.current_player.check()
        if params['Action name'] == 'Fold':
            result = self.current_player.fold()
        if params['Action name'] == 'Raise':
            result = self.current_player.raise_bet(int(params['Value']))
        if params['Action name'] == 'All in':
            result = self.current_player.all_in()        
        if params['Action name'] == 'Confirm ready':
            result = self.set_player_ready()
            

        if result['result'] == 'OK':
            self.check_game_state()
            if self.round_finished:
                self.finish_round()
                self.game_results_rich = self.get_game_results()
                self.initialize_round()
                self.round_finished = False
        return result

    def check_game_state(self):
        if self.check_number_of_players_left() == 1:
            self.round_finished = True
            return

        if self.check_betting_fished():
            self.reset_betting_round()
            #goes through all the round till the end in case there is one player still betting (the rest either folded or went all-in)
            while self.check_betting_fished():
                self.reset_betting_round()
                if self.finished or self.round_finished:
                    return
        if not self.initialization:
            self.current_player = self.get_next_player()

        while not (self.current_player and not self.current_player.folded and not self.current_player.all_in_state):
            if self.finished:
                return
            #if not self.current_player:
            self.new_loop()

        self.initialization = False
        return

    def get_current_available_actions(self):
        if self.current_player:
            return available_action_helper.get_available_actions(self.players, self.current_player)
        return None

    def set_player_ready(self):
        self.current_player.ready = True
        return {'result':'OK'}


    def initialize_round(self):
        self.dealer.collect_cards(self.players)
        self.table.clear()
        self.dealer.generate_deck()
        self.dealer.deal_cards_to_players(self.players)
        self.round_no = 0
        self.initialization = True
        self.check_game_state()
        self.bet_blinds()
        self.check_game_state()

    def finish_round(self):
        for p in self.players:
            self.pot += p.bet
            p.bet = 0
            p.ready = False
        results_groups  = self.check_game_results()
        self.game_results = []
        for key, group in results_groups:
            self.game_results.append(list(group))
        winner = self.game_results[0][0]
        print(winner.name)
        winner.balance += self.pot
        self.pot = 0 

        if self.no_starting < len(self.players) - 1:
            self.no_starting += 1 
        else:
            self.no_starting = 0

        self.no_playing = self.no_starting
        self.current_player = self.players[self.no_playing]
        self.initialization = True

        
    def check_betting_fished(self):
        max_bet = max(map(lambda p: p.bet, self.players))
        self.max_bet = max_bet

        if len(list(filter(lambda p: not p.all_in_state, self.players))) < 2:
            return len(list(filter(lambda p: not p.all_in_state, self.players)))

        for p in self.players:
            if not p.active or p.folded or p.all_in_state:
                continue
            if p.bet != max_bet or not p.bet_placed:
                return False

        return True

    def check_number_of_players_left(self):
        result = len(list(filter(lambda p: p.folded == False and p.active == True, self.players)))
        return result

    def check_game_results(self):
        for p in self.players:
            p.find_hands()

        players_finished = list(filter(lambda p: p.active and not p.folded, self.players))
        players_finished.sort(reverse=True)
        return groupby(players_finished, key=lambda x: x.cards.as_values())

    def get_game_results(self):
        players_ranking = self.game_results
        result = []
        for group in players_ranking:
            for p in group:
                result.append({"Name": p.name,
                "Hands": list(map(lambda h: h.as_name_and_value(),p.cards.hands_list)), 
                "Cards": p.print_cards(),
                "Best hand": p.cards.hands_list[0].as_name_and_value()})    
        return result

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
        elif self.no_playing < len(self.players) - 1:
            self.no_playing += 1
            self.current_player = self.players[self.no_playing]
            return self.current_player
        else:
            self.no_playing = 0
            self.current_player = self.players[self.no_playing]
            return self.current_player


    def new_loop(self):
        self.no_playing = self.no_starting
        self.current_player = self.players[self.no_playing]

    def reset_betting_round(self):
        self.new_loop()
        self.initialization = True
        self.round_no += 1
        self.max_bet = 0
        if self.round_no > 3:
            self.round_finished = True
            return
        self.dealer.add_new_card_to_table(self.round_no)
        for p in self.players:
            self.pot += p.bet
            p.bet = 0
            p.bet_placed = False

    def bet_blinds(self):
        result = None
        result = self.current_player.place_bet(self.small_blind) 
        if result['result'] == 'ERROR':
            result = self.current_player.all_in()
        if result['result'] == 'ERROR':
            print("ERROR: " + result['error_message'])
        self.get_next_player()
        result = self.current_player.place_bet(self.big_blind) 
        if result['result'] == 'ERROR':
            result = self.current_player.all_in()
        if result['result'] == 'ERROR':
            print("ERROR: " + result['error_message'])
        self.get_next_player()
        self.initialization = True

