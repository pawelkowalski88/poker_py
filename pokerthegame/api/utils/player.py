# Player class
from pokerthegame.api.utils import Hand
from pokerthegame.api.utils import JsonConvert


@JsonConvert.register
class Player(object):
    """Represents a poker player.
    """

    def __init__(self, name: str = "", balance=5000, cards=None, bet=0, bet_placed=False,
                 active=True, folded=False, all_in_state=False, ready=False):
        """Initializes a new instance of the Player class.

        :param name: The player display name.
        :param balance: The amount of money that the player currently has.
        :param cards: The player's own cards. An instance of the Hand class.
        :param bet: The bet the player has placed.
        :param bet_placed: True when the player has already made a bet (call action is counted as well).
        :param active: True if the player is still active (has funds).
        :param folded: True if the player has folded in this or previous betting round.
        :param all_in_state: True if the player has made an all-in bet.
        :param ready: True if the player is ready to begin the game.
        """
        self.name = name
        self.balance = balance

        # The name needs to be changed.
        self.cards = cards
        self.bet = bet
        self.bet_placed = bet_placed
        self.active = active
        self.folded = folded
        self.all_in_state = all_in_state
        self.ready = ready

    # def __init__(self, name:str = ""):
    #         self.name = name
    #         self.balance = 5000
    #         self.cards = None
    #         self.bet = 0
    #         self.bet_placed = False
    #         self.active = True
    #         self.folded = False
    #         self.all_in_state = False
    #         self.ready = True

    def add_card(self, card):
        """Adds a card to the player's hand.

        :param card: The card object to be added.
        :return:
        """
        self.cards.cards.append(card)

    def find_hands(self):
        """Checks the cards to find the ranking of the hands of the current player - for comparison with the others.

        :return:
        """
        self.cards.find_hands()
        self.cards.sort_my_hands()

    def place_bet(self, amount):
        """Places the bet with the player's money. The balance is reduced of the bet amount.

        :param amount: The amount to be bet.
        :return: Returns OK response if the bet was successful and returns an error object if the balance was to small.
        """
        if self.balance >= amount:
            self.bet += amount
            self.balance -= amount
            self.bet_placed = True
            return {'result': 'OK'}
        else:
            return {'result': 'ERROR', 'error_message': 'UPS, not enough funds to bet'}

    def fold(self):
        """Folds the cards of the current player. The folded flag is set to true.

        :return:
        """
        self.folded = True
        return {'result': 'OK'}

    def call(self, max_bet):
        """Equalizes the highest bet on the table.

        :param max_bet: The current maximum bet on the table.
        :return: Returns OK response if the bet was successful and returns an error object if the balance was to small.
        """
        bet_diff = max_bet - self.bet
        if self.balance >= bet_diff:
            self.place_bet(bet_diff)
            return {'result': 'OK'}
        else:
            return {'result': 'ERROR', 'error_message': 'UPS, not enough funds to call, go all in instead'}

    def all_in(self):
        """Makes an all-in bet.

        :return: Returns OK response if the bet was successful and returns an error object if the balance was to small.
        """
        if self.balance > 0:
            self.place_bet(self.balance)
            self.all_in_state = True
            return {'result': 'OK'}
        else:
            return {'result': 'ERROR', 'error_message': 'UPS, not enough funds to bet'}

    def check(self):
        """Makes the check move. The balance is not reduced.

        :return: Returns OK response.
        """
        self.bet_placed = True
        return {'result': 'OK'}

    def raise_bet(self, raise_amount):
        """Places the bet higher than the current highest bet on the table.

        :param raise_amount: The amount of the total bet after the raise.
        :return: Returns OK response if the bet was successful and returns an error object if the balance was to small.
        """
        return self.place_bet(raise_amount)        

    def print_cards(self):
        """Prints the carts that belong to the player.

        :return: The player's cards string representation.
        """
        if self.cards:
            return self.cards.print_cards(False)
        return ""

    def reset_player(self):
        """Puts all the properties of the player into the initial state.

        :return:
        """
        self.cards = Hand(None)
        self.bet = 0
        self.bet_placed = False
        # self.active = True
        self.folded = False
        self.all_in_state = False
        self.ready = True

    def __gt__(self, other):
        """Compares the players by their hands.

        :param other: The second instance of the Player class for comparison.
        :return:Returns true if the current instance of the Player class has better hand.
        """
        if isinstance(other, Player):
            return self.cards > other.cards

    def __str__(self):
        """Returns a string representation of the Player object.

        :return: Returns a string representation of the Player object.
        """
        
        result = self.name + " " + str(self.balance) + " " + self.print_cards() + " bet: " + str(self.bet) + \
            " folded: " + str(self.folded)
        if self.all_in_state:
            result += " ALL IN"
        return result
