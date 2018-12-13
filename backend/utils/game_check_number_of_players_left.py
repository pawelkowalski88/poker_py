import unittest
from backend.utils.game import Game
from backend.utils.player import Player


class TestClass(unittest.TestCase):

    def test_check_two_players_left_one_folded(self):

        game = Game()
        game.add_player(Player("Pawel"))
        game.add_player(Player("Karolina"))
        game.add_player(Player("Tyna"))

        game.players[1].folded = True

        result = game.check_number_of_players_left()
        self.assertEqual(result, 2)

    def test_check_one_player_left_one_inactive(self):

        game = Game()
        game.add_player(Player("Pawel"))
        game.add_player(Player("Karolina"))

        game.players[1].active = False

        result = game.check_number_of_players_left()
        self.assertEqual(result, 1)


if __name__ == '__main__':
    unittest.main()