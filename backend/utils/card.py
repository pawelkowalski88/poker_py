# Playing card class
from colorama import Fore,Back, Style, init
from jsonconvert import JsonConvert

init(convert=True)

def card_to_int(val):
    if val in range(2,11):
        
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

def from_dict(self, source):
        return Card(source["figure"], source["color"])

@JsonConvert.register
class Card(object):

    def __init__(self, figure:str="", color:str="", covered = False, taken = False):
        self.figure = figure
        self.color = color
        self.covered = covered
        self.taken = taken

    def __str__(self):
        if self.covered:
            return '|??|'

        if self.color == '♠' or self.color == '♣':
            return '|'+Fore.WHITE+str(self.figure)+self.color+Style.RESET_ALL+'|'
        else:
            return '|'+Fore.RED+str(self.figure)+self.color+Style.RESET_ALL+'|'


    def __int__(self):
        return card_to_int(self.figure)


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
        
