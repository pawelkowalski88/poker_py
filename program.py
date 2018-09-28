from card import Card
from hand import Hand
import random


def pick_a_card(carddeck):
    card = carddeck[random.randint(0,len(carddeck)-1)]
    while card.taken == True:
        card = carddeck[random.randint(0,len(carddeck)-1)]
    card.taken = True
    return card

carddeck = []

for i in [2,3,4,5,6,7,8,9,"J","Q","K","A"]:
    for c in ['♠', '♣', '♥', '♦']:
        carddeck.append(Card(i, c))

table = []
hand = Hand(table)

table.append(pick_a_card(carddeck))
table.append(pick_a_card(carddeck))
table.append(pick_a_card(carddeck))

hand.cards.append(pick_a_card(carddeck))
hand.cards.append(pick_a_card(carddeck))

print(hand.print_cards())
print(list(map(lambda h: str(h.hand_name) + ' ' + str(h.value), hand.find_hands())))