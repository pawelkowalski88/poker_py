import unittest
from utils.available_action_helper import check_available, fold_available, call_available, bet_available, all_in_available
from utils.player import Player


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

    def test_bet_available_true(self):
        players = []
        players.append(Player("Pawel"))
        players.append(Player("Karolina"))

        result = bet_available(players, players[0])

        self.assertEqual(result, True)

    def test_bet_available_false(self):
        players = []
        players.append(Player("Pawel"))
        players.append(Player("Karolina"))

        players[1].bet = 1000

        result = bet_available(players, players[0])

        self.assertEqual(result, False)

    def test_call_available_true(self):
        players = []
        players.append(Player("Pawel"))
        players.append(Player("Karolina"))

        players[0].bet = 1000
        players[1].bet = 2000
        players[0].balance = 1200

        result = call_available(players, players[0])

        self.assertEqual(result, True)

    def test_call_available_to_little_balance_false(self):
        players = []
        players.append(Player("Pawel"))
        players.append(Player("Karolina"))

        players[0].bet = 1000
        players[1].bet = 2000
        players[0].balance = 200

        result = call_available(players, players[0])

        self.assertEqual(result, False)

    def test_call_available_higher_bet_false(self):
        players = []
        players.append(Player("Pawel"))
        players.append(Player("Karolina"))

        players[0].bet = 3000
        players[1].bet = 2000
        players[0].balance = 200

        result = call_available(players, players[0])

        self.assertEqual(result, False)

    def test_all_in_available_true(self):
        players = []
        players.append(Player("Pawel"))
        players.append(Player("Karolina"))

        players[1].bet = 3000
        players[0].bet = 1000
        players[0].balance = 200

        result = all_in_available(players, players[0])

        self.assertEqual(result, True)

    def test_all_in_available_false(self):
        players = []
        players.append(Player("Pawel"))
        players.append(Player("Karolina"))

        players[1].bet = 500
        players[0].bet = 1000
        players[0].balance = 200

        result = all_in_available(players, players[0])

        self.assertEqual(result, False)


if __name__ == '__main__':
    unittest.main()