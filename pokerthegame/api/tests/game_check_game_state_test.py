import unittest
from pokerthegame.api.utils import Game


class TestClass(unittest.TestCase):

    def test_bypass_player_all_in(self):
        game = Game()
        game.add_player("Pawel")
        game.add_player("Karolina")
        game.add_player("Tyna")
        game.check_game_state()
        game.players[1].all_in_state = True

        game.check_game_state()

        self.assertEqual(game.current_player, game.players[2])

    def test_bypass_player_folded(self):
        game = Game()
        game.add_player("Pawel")
        game.add_player("Karolina")
        game.add_player("Tyna")

        game.check_game_state()
        game.players[1].folded = True

        game.check_game_state()

        self.assertEqual(game.current_player.name, game.players[2].name)

    def test_bypass_next_player(self):
        game = Game()
        game.add_player("Pawel")
        game.add_player("Karolina")
        game.add_player("Tyna")

        game.check_game_state()

        game.check_game_state()

        self.assertEqual(game.current_player.name, game.players[1].name)


if __name__ == '__main__':
    unittest.main()