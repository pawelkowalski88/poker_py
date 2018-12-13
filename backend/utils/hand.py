# Represents a poker hand (Royal flush, straight flush, etc.)
from collections import Counter
from backend.utils.hand_description import HandDescription
from backend.utils.jsonconvert import JsonConvert


@JsonConvert.register
class Hand(object):
    """Represents a poker hand (Royal flush, straight flush, etc.).
    """
    def __init__(self, cards_on_table=None, cards=[], hands_list=[]):
        """Initializes a new instance of the Hand class. All the parameters are optional.

        :param cards_on_table: Reference to the collection of the common cards that are on the playing table.
        :param cards: Collection of the player's cards.
        :param hands_list: List of hands that can be put together form the available cards.
        """
        self.cards = cards
        self.cards_on_table = cards_on_table
        self.hands_list = hands_list

    def print_cards(self, all_cards=True):
        """Prints the cards from the Hand. Set all_cards to true to print also the cards from the table.

        :param all_cards: Set to true to print also the cards from the table.
        :return: Returns the list of cards as string for printing.
        """
        # print("Cards:")
        result = ""
        cards = self.cards
        if all_cards:
            cards += self.cards_on_table
        for c in cards:
            result += str(c)
        return result

    def find_hands(self):
        """Analyzes the table and player cards and updates the list of available hands as HandDescription.

        :return:
        """
        # hands = []
        if self.cards:
            all_cards = (self.cards+self.cards_on_table)

        self.pairs_threes_fours(self.hands_list, all_cards)
        self.find_flush(self.hands_list, all_cards)
        self.find_straight(self.hands_list, all_cards)

        hand_name_list = list(map(lambda h: h.hand_name, self.hands_list))

        hands_count = Counter(hand_name_list)
        for key, value in hands_count.items():
            if value == 2 and key == 'Pair':
                self.hands_list.append(HandDescription('Two pairs', None, None))

        if "Pair" in hand_name_list and "Three of a kind" in hand_name_list:
                self.hands_list.append(HandDescription('Full house', None, None))

        if "Flush" in hand_name_list and 'Straight' in hand_name_list:
                self.hands_list.append(HandDescription('Pokier', None, None))

        self.sort_my_hands()

    def pairs_threes_fours(self, hands_list, cards_list):
        """ Checks the collection of cards to find a pair, three of a kind or four of a kind.

        :param hands_list: A reference to the list of HandDescription objects.
        :param cards_list: A reference to the list of cards to check for hands.
        :return:
        """
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
        """Checks the collection of cards to find a flush (Five cards in the same color).

        :param hands_list: A reference to the list of HandDescription objects.
        :param cards_list: A reference to the list of cards to check for hands.
        :return:
        """
        card_color_counts = Counter(map(lambda c: c.color, cards_list))
        for value in card_color_counts.values():
            if value == 5:
                hands_list.append(HandDescription('Flush', None, None))

    def find_straight(self, hands_list, cards_list):
        """Checks the collection of cards to find a straight (Five cards in a row).
        BUGS!!! Does not work properly.

        :param hands_list: A reference to the list of HandDescription objects.
        :param cards_list: A reference to the list of cards to check for hands.
        :return:
        """
        card_values = list(map(lambda c: int(c), cards_list))
        card_values.sort(reverse=True)
        previous = -1
        for i, v in enumerate(card_values):
            if i > 0:
                if previous-v != 1:
                    break
            previous = v
        else:
            hands_list.append(HandDescription('Straight', card_values[0], None))

    def as_values(self):
        """Returns a list of HandDescription values only.

        :return: List of HandDescription values.
        """
        return [x for x in map(lambda h: h.as_values(), self.hands_list)]

    def sort_my_hands(self):
        """Sorts the HandDescription list. The highest HandDescriptions go first.

        :return:
        """
        self.hands_list.sort(reverse=True)

    def __gt__(self, other):
        """Compares the current instance of Hand with another instance of hand by comparing the HandDescription
        collections of both Hands.

        :param other: The other instance of the Hand class to be compared with the current instance.
        :return: Returns true if the current instance is higher.
        """
        if isinstance(other, Hand):
            return self.hands_list > other.hands_list
