import unittest
from game import Game
from player import Player


# game_service = GameService()

# game_service.perform_action("Add player", {"player name": "Pawel"})
# game_service.perform_action("Add player", {"player name": "Karolina"})

# game_service.perform_action("Start game", None)

# game_state = get_game_state(game_service)
# print_game_state(game_state)


class TestPlayerActions(unittest.TestCase):

    def test_place_bet_correct(self):
        player = Player('Tyna')
        player.balance = 5000
        
        res = player.place_bet(200)
        com = (res ==  {'result': 'OK'})

        self.assertEqual(com, True)

    def test_place_bet_incorect(self):
        player = Player('Tyna')
        player.balance = 100
        
        res = player.place_bet(200)
        res = res['result']

        self.assertEqual(res, 'ERROR')

    def test_game(self):
        game = Game()
        player = Player("tyna")
        player2 = Player("pawel")
        game.players = [player, player2]
        game.current_player = player
        game.player_action({'Action name': 'Bet', 'Amount':200})


if __name__ == '__main__':
    unittest.main()

