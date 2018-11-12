from card import Card
from hand import Hand
from hand_description import HandDescription
from player import Player
from game_results import GameResults
from game_results_collection import GameResultsCollection
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
        self.game_results_rich = GameResultsCollection()
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
        if not self.current_player and not params['Action name'] == 'Confirm ready':
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
            result = self.set_player_ready(params["Player"])
            return result
            
        if result['result'] == 'OK':
            self.check_game_state()
            if self.round_finished:
                self.finish_round()
                # results = self.get_game_results()
                self.game_results_rich = self.get_game_results()
                # self.initialize_round()
                self.round_finished = False
        return result

    def check_game_state(self):
        if self.check_number_of_players_left() == 1 and self.started:
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

        while not (self.current_player and not self.current_player.folded and not self.current_player.all_in_state and self.current_player.active):
            if self.finished:
                return
            if not self.current_player:
                self.new_loop()
            self.current_player = self.get_next_player()

        self.initialization = False

#web-service-2
#            if not self.current_player:
#                self.new_loop()
#            self.current_player = self.get_next_player()
        return

    def get_current_available_actions(self, my_player):
        if self.current_player or my_player:
            my_player = self.get_player(my_player)
            if my_player:
                result = available_action_helper.get_available_actions(self.players, self.current_player, my_player)
                return result
        return None

    def set_player_ready(self, input_player):
        if isinstance(input_player,Player):
            player_name = input_player.name
        else:
            player_name = input_player
        player = list(filter(lambda p: p.name == player_name, self.players))[0]
        player.ready = True
        if all(map(lambda p: p.ready or not p.active, self.players)):
            self.initialize_round()
            self.round_finished = False
        return {'result':'OK'}


    def initialize_round(self):
        self.started = True
        self.dealer.collect_cards(self.players)
        self.table.clear()
        self.dealer.generate_deck()
        self.dealer.deal_cards_to_players(self.players)
        self.round_no = 0
        self.initialization = True
        self.current_player = self.players[self.no_playing]
        self.check_game_state()
        self.bet_blinds()
        self.check_game_state()

    def finish_round(self):
        self.current_player = None
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

        # for p in self.players:
        #     if p.balance == 0:
        #         self.players.remove(p)
        #         p.active = False
        active_players = list(filter(lambda p: p.balance > 0, self.players))
        if len(active_players) == 1:
            self.finished = True

        if self.no_starting < len(self.players) - 1:
            self.no_starting += 1 
        else:
            self.no_starting = 0

        self.no_playing = self.no_starting
        self.initialization = True
  
        self.started = False  


        
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
        results = GameResultsCollection([])
        for group in players_ranking:
            for p in group:
                # result = GameResults(p.name, 
                #                     list(map(lambda h: h.as_name_and_value(),p.cards.hands_list)), 
                #                     p.print_cards(), 
                #                     p.cards.hands_list[0].as_name_and_value())

                # results.results.append(result)
                results.results.append({"name": p.name,
                "hands": list(map(lambda h: h.as_name_and_value(),p.cards.hands_list)), 
                "cards": p.print_cards(),
                "best_hand": p.cards.hands_list[0].as_name_and_value()})    
        return results

    def create_results_ranking(self, players_tab):
        for p in players_tab:
            p.find_hands()


    def add_player(self, name):
        player = Player(name)
        self.players.append(player)
        return player

    def get_player(self, name):
        try:
            return list(filter(lambda p: p.name == name, self.players))[0]
        except:
            return None

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


    def get_players(self, my_player):
        result = []
        for p in self.players:
            new_p = Player(name=p.name, balance=p.balance, bet=p.bet, bet_placed=p.bet_placed,
                active=p.active, folded=p.folded, all_in_state=p.all_in_state, ready=p.ready)
            if p.name == my_player:
                new_p.cards = p.cards
            else:
                new_p.cards = Hand(cards=[Card(covered=True), Card(covered=True)])
            result.append(new_p)
        return result

