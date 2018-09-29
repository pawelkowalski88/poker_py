from card import Card
from hand import Hand
from hand_description import HandDescription
from player import Player
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
player1 = Player("Pawel")
player1.cards = Hand(table)
player2 = Player("Karolina")
player2.cards = Hand(table)

table.append(pick_a_card(carddeck))
table.append(pick_a_card(carddeck))
table.append(pick_a_card(carddeck))

player1.add_card(pick_a_card(carddeck))
player1.add_card(pick_a_card(carddeck))
player2.add_card(pick_a_card(carddeck))
player2.add_card(pick_a_card(carddeck))

player1.find_hands()
player2.find_hands()

print()
print("Table")
print_table(table)
print()
print("Hand 1")
print(player1.print_cards())
print(list(map(lambda h: str(h.hand_name) + ' ' + str(h.value), player1.cards.hands_list)))
print()
print("Hand 2")
print(player2.print_cards())
print(list(map(lambda h: str(h.hand_name) + ' ' + str(h.value), player2.cards.hands_list)))

print(player1.cards > player2.cards)