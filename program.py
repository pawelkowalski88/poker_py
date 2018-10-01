from card import Card
from hand import Hand
from hand_description import HandDescription
from player import Player
from itertools import groupby
import random


def pick_a_card(carddeck):
    card = carddeck[random.randint(0,len(carddeck)-1)]
    while card.taken == True:
        card = carddeck[random.randint(0,len(carddeck)-1)]
    card.taken = True
    return card

def print_table(cards):
    result=''
    for c in cards:
        result += str(c)
    print(result)

carddeck = []

for i in [2,3,4,5,6,7,8,9,"J","Q","K","A"]:
    for c in ['♠', '♣', '♥', '♦']:
        carddeck.append(Card(i, c))

table = []

players_table = []

for i in range(8):
    players_table.append(Player("Player " + str(i+1)))

for p in players_table:
    p.cards = Hand(table)
    p.add_card(pick_a_card(carddeck))
    p.add_card(pick_a_card(carddeck))

table.append(pick_a_card(carddeck))
table.append(pick_a_card(carddeck))
table.append(pick_a_card(carddeck))

for p in players_table:
    p.find_hands()

print()
print("Table")
print_table(table)
print()

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