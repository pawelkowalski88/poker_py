# Playing card class
from colorama import Fore, Style, init
from backend.utils.jsonconvert import JsonConvert

init(convert=True)


def card_to_int(val):
    """Converts card figure (2-10, J, Q, K, A) into an integer representation.
    :param val: Card figure to be converted.
    :return: Integer representation of the card value.
    """
    if val in range(2, 11):
        return int(val)
    if val == 'J':
        return 11
    if val == 'Q':
        return 12
    if val == 'K':
        return 13
    if val == 'A':
        return 14
    return ValueError


@JsonConvert.register
class Card(object):
    """Represents a playing card.
    """

    def __init__(self, figure: str = "", color: str = "", covered=False, taken=False):
        """Initializes a new instance of the Card class with the given figure and color.
        Optionally the card card can be set as covered or taken.

        :param figure: The desired card figure (2-10, J, Q, K, A).
        :param color: The desired card color.
        :param covered: Set to true if the card is to be shown face down. Default: false.
        :param taken: Set to true if the card is to be considered as dealt. Default: false.
        """
        self.figure = figure
        self.color = color

        # Consider removing
        self.covered = covered
        self.taken = taken

    def __str__(self):
        """Provides a string representation of the current Card instance.

        :return: The string representation of the card.
        """
        if self.covered:
            return '|??|'

        if self.color == '♠' or self.color == '♣':
            return '|'+Fore.WHITE+str(self.figure)+self.color+Style.RESET_ALL+'|'
        else:
            return '|'+Fore.RED+str(self.figure)+self.color+Style.RESET_ALL+'|'

    def __int__(self):
        """Overloads the magic function and provides an int representation of the current Card instance for comparisons.

        :return: Integer representation of the card value.
        """
        return card_to_int(self.figure)

    def __gt__(self, other):
        """Overloads the __gt__ magic function. Compares the current Card instance with another
        to establish which one is higher.

        :param other: The instance of the Card class to be compared with the current instance.
        :return: Returns true if the current Card instance is higher.
        """
        if isinstance(other, Card):
            return int(self) > int(other)
        return NotImplemented

    def __eq__(self, other):
        """Overloads the __eq__ magic function. Returns true if the compared Card instances are of equal value.

        :param other:  The instance of the Card class to be compared with the current instance.
        :return: Returns true if the compared Card instances are of equal value.
        """
        if isinstance(other, Card):
            return int(self) == int(other)
        return NotImplemented
