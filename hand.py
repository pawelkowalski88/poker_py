#Represents a poker hand (Royal flush, staright flush, etc.)
from card import Card
from hand_description import HandDescription
from collections import Counter
from jsonconvert import JsonConvert

@JsonConvert.register
class Hand(object):
    def __init__(self, cards_on_table=None, cards=[], hands_list=[]):
        self.cards = cards
        self.cards_on_table = cards_on_table
        self.hands_list = hands_list

    def print_cards(self, all=True):
        # print("Cards:")
        result = ""
        cards = self.cards
        if all:
            cards += self.cards_on_table
        for c in cards:
            result += str(c)
        return result

    def find_hands(self):
        # hands = []
        if self.cards:
            all_cards = (self.cards+self.cards_on_table)

        self.pairs_threes_fours(self.hands_list, all_cards)
        self.find_flush(self.hands_list,all_cards)
        self.find_straight(self.hands_list, all_cards)

        hand_name_list = list(map(lambda h: h.hand_name, self.hands_list))

        hands_count = Counter(hand_name_list)
        for key, value in hands_count.items():
            if value==2 and key=='Pair':
                self.hands_list.append(HandDescription('Two pairs', None, None))
            if value==3 and key=='Pair':
                self.hands_list.append(HandDescription('Two pairs', None, None))

        if "Pair" in hand_name_list and "Three of a kind" in hand_name_list:
                self.hands_list.append(HandDescription('Full house', None, None))

        if "Flush" in hand_name_list and 'Straight' in hand_name_list:
                self.hands_list.append(HandDescription('Pokier', None, None))

        self.sort_my_hands()
        #return hands

    def pairs_threes_fours(self, hands_list, cards_list):
        card_counts = Counter(map(lambda c: c.figure, cards_list))
        for key, value in card_counts.items():
            if value == 4:
                hands_list.append(HandDescription('Four of a kind', key, None))
            elif value == 3:
                hands_list.append(HandDescription('Three of a kind', key, None))
            elif value == 2:
                hands_list.append(HandDescription('Pair', key, None))
            elif value == 1:
                hands_list.append(HandDescription('High card', key, None))

    def find_flush(self, hands_list, cards_list):
        card_color_counts = Counter(map(lambda c: c.color, cards_list))
        for value in card_color_counts.values():
            if value == 5:
                hands_list.append(HandDescription('Flush', None, None))

    def find_straight(self, hands_list, cards_list):
        card_values = list(map(lambda c: int(c), cards_list))
        card_values.sort(reverse=True)
        previous = -1
        for i,v in enumerate(card_values):
            if i>0:
                if previous-v != 1:
                    break
            previous = v
        else:
            hands_list.append(HandDescription('Straight', card_values[0], None))

    def as_values(self):
        return [x for x in map(lambda h: h.as_values(), self.hands_list)]

    def sort_my_hands(self):
        self.hands_list.sort(reverse=True)

    def __gt__(self, other):
        if isinstance(other, Hand):
            return self.hands_list > other.hands_list



# table = [Card(10, '♠'), Card(6, '♠'), Card(7, '♠')]
# hand = Hand(table)
# hand.cards.append(Card(8, '♠'))
# hand.cards.append(Card(9, '♠'))

# print(hand.print_cards())

# print(list(map(lambda h: str(h.hand_name) + ' ' + str(h.value), hand.find_hands())))



            

        # all_cards.sort(key=lambda c: int(c), reverse=True)
        # all_cards_str = ''.join(list(map(lambda c: c.print_value(), all_cards)))
        # print(all_cards_str)

        # p = re.compile(r'(\w){3}')
        # print(p.findall(all_cards_str))


    # def high_card(self):
    #     all_cards = self.cards + self.cards_on_table
    #     return HandDescription('High card', max(all_cards).figure, self.print_cards([max(all_cards)]))

    # def pair_triple_quad(self):
    #     all_cards = self.cards + self.cards_on_table
    #     card_count = Counter(map(lambda c: c.figure, all_cards)).most_common(1)
        
    #     if (card_count[0][1] == 2):
    #         returned_cards = list(filter(lambda c: card_count[0][0] == c.figure, all_cards))
    #         return HandDescription('Pair', card_count[0][0], self.print_cards(returned_cards))
