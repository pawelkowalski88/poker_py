# Playing card class
from colorama import Fore,Back, Style, init

init(convert=True)

class Card():

    def __init__(self, figure, color):
        self.figure = figure
        self.color = color
        self.covered = False
        self.taken = False


    def __str__(self):
        if self.covered:
            return '|??|'

        if self.color == '♠' or self.color == '♣':
            return '|'+Fore.WHITE+str(self.figure)+self.color+Style.RESET_ALL+'|'
        else:
            return '|'+Fore.RED+str(self.figure)+self.color+Style.RESET_ALL+'|'


    def __int__(self):
        if self.figure in range(2,11):
            return int(self.figure)
        if self.figure == 'J':
            return 11
        if self.figure == 'Q':
            return 12
        if self.figure == 'K':
            return 13
        if self.figure == 'A':
            return 14
        return ValueError


    def __gt__(self, other):
        if isinstance(other, Card):
            return int(self) > int(other)
        return NotImplemented

    def __eq__(self, other):
        if isinstance(other, Card):
            return int(self) == int(other)
        return NotImplemented

    def __hash__(self):
        return hash(self.figure)

    def print_value(self):
        if self.figure == 10:
            return 'X'
        else:
            return str(self.figure)
        
