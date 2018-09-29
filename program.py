from card import Card
from hand import Hand
from hand_description import HandDescription
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
hand1 = Hand(table)
hand2 = Hand(table)

# hand1.hands_list.append(HandDescription('Two pairs', None, None))
# hand1.hands_list.append(HandDescription('Pair', 2, None))
# hand1.hands_list.append(HandDescription('Pair', 4, None))
# hand1.hands_list.append(HandDescription('Pair', 6, None))
# hand2.hands_list.append(HandDescription('Pair', 3, None))
# hand2.hands_list.append(HandDescription('Two pairs', None, None))

# hand1.sort_my_hands()
# hand2.sort_my_hands()

table.append(pick_a_card(carddeck))
table.append(pick_a_card(carddeck))
table.append(pick_a_card(carddeck))

hand1.cards.append(pick_a_card(carddeck))
hand1.cards.append(pick_a_card(carddeck))
hand2.cards.append(pick_a_card(carddeck))
hand2.cards.append(pick_a_card(carddeck))

# table.append(Card(5, '♠'))
# table.append(Card('J', '♠'))
# table.append(Card('J', '♥'))

# hand1.cards.append(Card(5, '♥'))
# hand1.cards.append(Card(5, '♣'))
# hand2.cards.append(Card('J', '♣'))
# hand2.cards.append(Card(5, '♦'))

hand1.find_hands()
hand2.find_hands()

hand1.sort_my_hands()
hand2.sort_my_hands()

print()
print("Table")
print_table(table)
print()
print("Hand 1")
print(hand1.print_cards(False))
print(list(map(lambda h: str(h.hand_name) + ' ' + str(h.value), hand1.hands_list)))
print()
print("Hand 2")
print(hand2.print_cards(False))
print(list(map(lambda h: str(h.hand_name) + ' ' + str(h.value), hand2.hands_list)))