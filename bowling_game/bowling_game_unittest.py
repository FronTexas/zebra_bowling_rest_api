import unittest 
from mock import patch
from BowlingGame import BowlingGame

class TestBowlingGame(unittest.TestCase):
	def setUp(self):
		pass

	@patch('BowlingGame.BowlingGame.get_score_for_current_throw', return_value=5)
	def test_to_see_if_first_throw_score_updated_accordingly_when_the_player_get_open_frame(self, mocked_function):
		bowling_game = BowlingGame()
		bowling_game.throw_bowling_ball()
		self.assertEqual(bowling_game.frames[0].get_first_throw_score(), 5)
	
	@patch('BowlingGame.BowlingGame.get_score_for_current_throw', return_value=3)
	def test_to_see_if_second_throw_score_updated_accordingly_when_the_player_get_open_frame(self, mocked_function):
		bowling_game = BowlingGame()
		bowling_game.throw_bowling_ball()
		bowling_game.throw_bowling_ball()
		self.assertEqual(bowling_game.frames[0].get_second_throw_score(), 3)

	@patch('BowlingGame.BowlingGame.get_score_for_current_throw', return_value=5)
	def test_to_see_if_spared_frame_updated_accordingly_when_the_player_get_open_frame(self, mocked_function):
		bowling_game = BowlingGame()
		bowling_game.throw_bowling_ball()
		bowling_game.throw_bowling_ball()
		bowling_game.throw_bowling_ball()
		self.assertEqual(bowling_game.frames[0].get_total_score(), 15)

	@patch('BowlingGame.BowlingGame.get_score_for_current_throw', side_effect=[10, 3, 2])
	def test_to_see_if_striked_frame_updated_accordingly_when_the_player_get_open_frame(self, mocked_function):
		bowling_game = BowlingGame()
		bowling_game.throw_bowling_ball()
		bowling_game.throw_bowling_ball()
		bowling_game.throw_bowling_ball()
		self.assertEqual(bowling_game.frames[0].get_total_score(), 15)

	@patch('BowlingGame.BowlingGame.get_score_for_current_throw', side_effect=[3, 2])
	def test_to_see_if_frames_index_updated_accordingly_when_the_player_get_open_frame(self, mocked_function):
		bowling_game = BowlingGame()
		bowling_game.throw_bowling_ball()
		bowling_game.throw_bowling_ball()
		self.assertEqual(bowling_game.current_frame_index, 1)

	# testing having a spare 

	# testing having a strike 

	# testing having consecutive spare 

	# testing having consecutive strike 

	# testing having a spare and then open frame 

	# testing having a spare and then strike 

	# testing having a strike and then open frame 

	# testing having a strike and then spare 

if __name__ == '__main__':
	unittest.main()


