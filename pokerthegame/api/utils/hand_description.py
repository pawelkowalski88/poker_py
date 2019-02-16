from pokerthegame.api.utils import card_to_int
from pokerthegame.api.utils import JsonConvert

'''Card hand ranking.'''
hand_ranking = {
    "High card": 1,
    "Pair": 2,
    "Two pairs": 3,
    "Three of a kind": 4,
    "Straight": 5,
    "Flush": 6,
    "Full house": 7,
    "Four of a kind": 8,
    "Straight flush": 9}


@JsonConvert.register
class HandDescription:
    """Represents a poker hand value.
    """

    def __init__(self, hand_name="", value=""):
        """Initializes a new instance of the HandDescription class.

        :param hand_name: The name of the hand. For exapmle pair, two pair.
        :param value: The hand value. For pair of "7" the value is 7, for a three of a kind of aces the value is 14.
        """
        self.hand_name = hand_name
        self.value = value
        # self.returned_cards = returned_cards

    def __gt__(self, other):
        """Compares the current instance of the HandDescription class with another one.

        :param other: The other instance of the HandDescription class.
        :return: Returns true if the current instance is higher than the other instance.
        """
        if isinstance(other, HandDescription):
            if hand_ranking[self.hand_name] == hand_ranking[other.hand_name]:
                if not self.value or not other.value:
                    return False 
                return card_to_int(self.value) > card_to_int(other.value)
            return hand_ranking[self.hand_name] > hand_ranking[other.hand_name]
        return NotImplemented

    def __eq__(self, other):
        """Returns true if the two HandDescription objects are of equal value.

        :param other: The other instance of the HandDescription class.
        :return: Returns true if the two HandDescription objects are of equal value.
        """
        if isinstance(other, HandDescription):
            if hand_ranking[self.hand_name] == hand_ranking[other.hand_name]:
                if not self.value and not other.value:
                    return True
                if not self.value or not other.value:
                    return False
                return card_to_int(self.value) == card_to_int(other.value)
            return False
        return NotImplemented
    
    def as_values(self):
        """Returns the HandDescription's rank and value.

        :return: Returns an array of hand's rank and value.
        """
        return [hand_ranking[self.hand_name], self.value]

    def as_name_and_value(self):
        """Returns the hands name and value.

        :return:Returns the hands name and value.
        """
        if self.value:
            return {"name": self.hand_name, "value": str(self.value)}
        return {"name": self.hand_name, "value": ""}
