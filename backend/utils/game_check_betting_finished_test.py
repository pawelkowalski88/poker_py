import unittest
from backend.utils.game import Game
from backend.utils.player import Player


class TestGame(unittest.TestCase):

    def test_check_betting_fished_all_200_true(self):
        # Arrange
        game = Game()
        game.add_player(Player("Pawel"))
        game.add_player(Player("Karolina"))
        game.players[0].bet = 200
        game.players[1].bet = 200
        game.players[0].bet_placed = True
        game.players[1].bet_placed = True

        # Act(?)
        result = game.check_betting_fished()

        # Assert
        self.assertEqual(result, True)

    def test_check_betting_fished_false(self):
        game = Game()
        game.add_player(Player("Pawel"))
        game.add_player(Player("Karolina"))
        game.players[0].bet = 220
        game.players[1].bet = 200
        game.players[0].bet_placed = True
        game.players[1].bet_placed = True

        result = game.check_betting_fished()

        self.assertEqual(result, False)

    def test_check_betting_fished_false_betting_not_ended(self):
        game = Game()
        game.add_player(Player("Pawel"))
        game.add_player(Player("Karolina"))
        game.players[0].bet = 0
        game.players[1].bet = 0
        game.players[0].bet_placed = True
        game.players[1].bet_placed = False

        result = game.check_betting_fished()

        self.assertEqual(result, False)

    def test_check_betting_fished_true_players_inactive(self):
        game = Game()
        game.add_player(Player("Pawel"))
        game.add_player(Player("Karolina"))
        game.add_player(Player("Tyna"))
        game.players[0].bet = 220
        game.players[1].bet = 220
        game.players[2].bet = 0
        game.players[0].bet_placed = True
        game.players[1].bet_placed = True
        game.players[2].active = False

        result = game.check_betting_fished()

        self.assertEqual(result, True)

    def test_check_betting_fished_true_player_folded(self):
        game = Game()
        game.add_player(Player("Pawel"))
        game.add_player(Player("Karolina"))
        game.add_player(Player("Tyna"))
        game.players[0].bet = 220
        game.players[1].bet = 220
        game.players[2].bet = 100
        game.players[0].bet_placed = True
        game.players[1].bet_placed = True
        game.players[2].bet_placed = True
        game.players[2].folded = True

        result = game.check_betting_fished()

        self.assertEqual(result, True)

    def test_check_betting_fished_true_player_all_in(self):
        game = Game()
        game.add_player(Player("Pawel"))
        game.add_player(Player("Karolina"))
        game.players[0].bet = 0
        game.players[1].bet = 0
        game.players[0].all_in_state = True

        result = game.check_betting_fished()

        self.assertEqual(result, True)

if __name__ == '__main__':
    unittest.main()