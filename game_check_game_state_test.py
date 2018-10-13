import unittest
from player import Player
from game import Game

class TestClass(unittest.TestCase):

    def test_bypass_player_all_in(self):
        game = Game()
        game.add_player("Pawel")
        game.add_player("Karolina")
        game.add_player("Tyna")

        game.players[1].all_in_state = True
        game.current_player = game.players[0]

        game.check_game_state()

        self.assertEqual(game.current_player, game.players[2])

    def test_bypass_player_folded(self):
        game = Game()
        game.add_player("Pawel")
        game.add_player("Karolina")
        game.add_player("Tyna")

        game.current_player = game.players[0]
        game.players[1].folded = True

        game.check_game_state()

        self.assertEqual(game.current_player.name, game.players[2].name)


if __name__ == '__main__':
    unittest.main()