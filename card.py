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
        try:
            return int(self.figure)
        except:
            if self.figure in ['J', 'Q', 'K']:
                return 10
            if self.figure == 'A':
                return 11