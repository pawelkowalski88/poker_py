#Represents a poker hand (Royal flush, staright flush, etc.)
from card import Card
from hand_description import HandDescription
from collections import Counter

class Hand():
    def __init__(self, cards_on_table):
        self.cards = []
        self.cards_on_table = cards_on_table

    def high_card(self):
        all_cards = self.cards + self.cards_on_table
        return HandDescription('High card', max(all_cards))

    def pair(self):
        all_cards = self.cards + self.cards_on_table
        card_count = Counter(map(lambda c: int(c), all_cards))
        for c, n in card_count.items():
            print(str(c) + " " + str(n))


table = [Card(2, '♠'), Card(5, '♠')]
hand = Hand(table)

hand.cards.append(Card(4, '♠'))
hand.cards.append(Card('A', '♥'))
hand.cards.append(Card('A', '♠'))

print(str(hand.high_card().hand_name) + " " + str(hand.high_card().value))

hand.pair()