import random
from utils.card import Card
from utils.hand import Hand


class Dealer:
    """Represents a dealer responsible for dealing and collecting cards.

    """

    def __init__(self, table):
        """Initializes a new instance of the Dealer class with a reference to the main table.

        :param table: The main table containing the cards.
        """
        self.carddeck = []
        self.generate_deck()
        self.table = table

    def generate_deck(self):
        """Generates a new fresh deck of cards from 2 to A, four colors, no jokers.

        :return:
        """
        self.carddeck = []
        figures = [2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K", "A"]
        colors = ['♠', '♣', '♥', '♦']
        self.carddeck = [Card(f, c) for f in figures for c in colors]

    def deal_cards_to_players(self, players):
        """Gives each player two random cards from the deck.

        :param players: The players collection.
        :return:
        """
        for p in players:
            if p.balance == 0:
                players.remove(p)
                p.active = False
        for p in players:
            if p.active:
                p.cards = Hand(self.table, [], [])
                p.add_card(self.pick_a_card())
                p.add_card(self.pick_a_card())

    def collect_cards(self, players):
        """Collects the cards from the players.

        :param players: The players collection.
        :return:
        """
        for p in players:
            p.reset_player()

    def pick_a_card(self):
        """Randomly selects a card from the deck.

        :return: Returns the selected card.
        """
        card = self.carddeck[random.randint(0, len(self.carddeck)-1)]
        while card.taken:
            card = self.carddeck[random.randint(0, len(self.carddeck)-1)]
        card.taken = True
        return card

    def add_new_card_to_table(self, round_no):
        """Puts cards on the table at the beginning of every betting round (flop, turn and river).

        :param round_no: The current round number.
        :return:
        """
        if round_no == 0 or round_no > 3:
            return
        if round_no == 1:
            self.table.append(self.pick_a_card())
            self.table.append(self.pick_a_card())
            self.table.append(self.pick_a_card())
        if round_no > 1:
            self.table.append(self.pick_a_card())
