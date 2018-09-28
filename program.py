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
hand1 = Hand(table)
hand2 = Hand(table)

table.append(pick_a_card(carddeck))
table.append(pick_a_card(carddeck))
table.append(pick_a_card(carddeck))

hand1.cards.append(pick_a_card(carddeck))
hand1.cards.append(pick_a_card(carddeck))
hand2.cards.append(pick_a_card(carddeck))
hand2.cards.append(pick_a_card(carddeck))

print()
print("Hand 1")
print(hand1.print_cards())
print(list(map(lambda h: str(h.hand_name) + ' ' + str(h.value), hand1.find_hands())))
print()
print("Hand 2")
print(hand2.print_cards())
print(list(map(lambda h: str(h.hand_name) + ' ' + str(h.value), hand2.find_hands())))