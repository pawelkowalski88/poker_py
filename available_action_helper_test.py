import unittest
from available_action_helper import check_available
from player import Player
from game import Game

class TestClass(unittest.TestCase):
    def test_check_available_true(self):
        players = []
        players.append(Player("Pawel"))
        players.append(Player("Karolina"))

        result = check_available(players, players[0])

        self.assertEqual(result, True)

    def test_check_available_false(self):
        players = []
        players.append(Player("Pawel"))
        players.append(Player("Karolina"))

        players[1].bet = 1000

        result = check_available(players, players[0])

        self.assertEqual(result, False)

if __name__ == '__main__':
    unittest.main()