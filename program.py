from card import Card
from hand import Hand
from hand_description import HandDescription
from player import Player
from itertools import groupby
import random

table = []
players_table = []

def pick_a_card(carddeck):
    card = carddeck[random.randint(0,len(carddeck)-1)]
    while card.taken == True:
        card = carddeck[random.randint(0,len(carddeck)-1)]
    card.taken = True
    return card

def print_table(cards):
    print()
    print("Table")
    result=''
    for c in cards:
        result += str(c)
    print(result)
    print()

def generate_deck():
    carddeck = []
    for i in [2,3,4,5,6,7,8,9,"J","Q","K","A"]:
        for c in ['♠', '♣', '♥', '♦']:
            carddeck.append(Card(i, c))
    return carddeck

def deal_cards_to_players(players):
    for p in players:
        p.cards = Hand(table)
        p.add_card(pick_a_card(carddeck))
        p.add_card(pick_a_card(carddeck))

def create_default_players(number_of_players):
    player_tab = []
    for i in range(number_of_players):  
        player_tab.append(Player("Player " + str(i+1)))
    return player_tab

def add_new_card_to_table(tab):
    tab.append(pick_a_card(carddeck))

def create_results_ranking(players_tab):
    for p in players_tab:
        p.find_hands()

carddeck = generate_deck()
players_table = create_default_players(4)
deal_cards_to_players(players_table)

add_new_card_to_table(table)
add_new_card_to_table(table)
add_new_card_to_table(table)


print_table(table)

players_table.sort(reverse=True)
players_ranking = groupby(players_table, key=lambda x: x.cards.as_values())
for group, players in players_ranking:
    for p in players:
        print(p.name)
        print(p.cards.as_values())
        print(p.print_cards())
    print()

players_table.sort(reverse=True)

print(list(map(lambda p: p.name, players_table)))