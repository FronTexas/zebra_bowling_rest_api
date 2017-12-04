import unittest 
from mock import patch
from BowlingGame import BowlingGame

class TestBowlingGame(unittest.TestCase):

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

		# throwing a strike on first frame
		bowling_game.throw_bowling_ball()
		
		# throwing a 3
		bowling_game.throw_bowling_ball()

		# throwing a 2
		bowling_game.throw_bowling_ball()

		self.assertEqual(bowling_game.frames[0].get_total_score(), 15)

	@patch('BowlingGame.BowlingGame.get_score_for_current_throw', side_effect=[3, 2])
	def test_to_see_if_frames_index_updated_accordingly_when_the_player_get_open_frame(self, mocked_function):
		bowling_game = BowlingGame()
		bowling_game.throw_bowling_ball()
		bowling_game.throw_bowling_ball()
		self.assertEqual(bowling_game.current_frame_index, 1)

	@patch('BowlingGame.BowlingGame.get_score_for_current_throw', side_effect=[5, 5, 3, 7, 4])
	def test_to_see_if_multiple_spare_updates_the_frame_accordingly(self, mocked_function):
		bowling_game = BowlingGame()
		bowling_game.throw_bowling_ball()
		bowling_game.throw_bowling_ball()
		bowling_game.throw_bowling_ball()
		bowling_game.throw_bowling_ball()
		bowling_game.throw_bowling_ball()
		self.assertEqual(bowling_game.frames[0].get_total_score(), 13)
		self.assertEqual(bowling_game.frames[1].get_total_score(), 14)
		self.assertEqual(bowling_game.frames[2].get_total_score(), 4)

	@patch('BowlingGame.BowlingGame.get_score_for_current_throw', side_effect=[10, 10, 10, 5, 2])
	def test_to_see_if_multiple_strike_updates_the_frame_accordingly(self, mocked_function):
		bowling_game = BowlingGame()
		bowling_game.throw_bowling_ball()
		bowling_game.throw_bowling_ball()
		bowling_game.throw_bowling_ball()
		bowling_game.throw_bowling_ball()
		bowling_game.throw_bowling_ball()
		self.assertEqual(bowling_game.frames[0].get_total_score(), 30)
		self.assertEqual(bowling_game.frames[1].get_total_score(), 25)
		self.assertEqual(bowling_game.frames[2].get_total_score(), 17)
		self.assertEqual(bowling_game.frames[3].get_total_score(), 7)


if __name__ == '__main__':
	unittest.main()


