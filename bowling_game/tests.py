# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from mock import patch

from .models import BowlingGame
from .models import Frame

BOWLING_GAME_MODULE_PATH = 'bowling_game.models.BowlingGame'

class TestBowlingGame(TestCase):

	@patch(BOWLING_GAME_MODULE_PATH + '.get_score_for_current_throw', return_value=5)
	def test_to_see_if_first_throw_score_updated_accordingly_when_the_player_get_open_frame(self, mocked_function):
		bowling_game = BowlingGame.objects.create()
		bowling_game.throw_bowling_ball()
		self.assertEqual(bowling_game.frames.all()[0].get_first_throw_score(), 5)
	
	@patch(BOWLING_GAME_MODULE_PATH + '.get_score_for_current_throw', return_value=3)
	def test_to_see_if_second_throw_score_updated_accordingly_when_the_player_get_open_frame(self, mocked_function):
		bowling_game = BowlingGame.objects.create()
		bowling_game.throw_bowling_ball()
		bowling_game.throw_bowling_ball()
		self.assertEqual(bowling_game.frames.all()[0].get_second_throw_score(), 3)

	@patch(BOWLING_GAME_MODULE_PATH + '.get_score_for_current_throw', return_value=5)
	def test_to_see_if_spared_frame_updated_accordingly_when_the_player_get_open_frame(self, mocked_function):
		bowling_game = BowlingGame.objects.create()
		bowling_game.throw_bowling_ball()
		bowling_game.throw_bowling_ball()
		bowling_game.throw_bowling_ball()
		self.assertEqual(bowling_game.frames.all()[0].get_total_score(), 15)

	@patch(BOWLING_GAME_MODULE_PATH + '.get_score_for_current_throw', side_effect=[10, 3, 2])
	def test_to_see_if_striked_frame_updated_accordingly_when_the_player_get_open_frame(self, mocked_function):
		bowling_game = BowlingGame.objects.create()

		# throwing a strike on first frame
		bowling_game.throw_bowling_ball()
		
		# throwing a 3
		bowling_game.throw_bowling_ball()

		# throwing a 2
		bowling_game.throw_bowling_ball()

		self.assertEqual(bowling_game.frames.all()[0].get_total_score(), 15)

	@patch(BOWLING_GAME_MODULE_PATH + '.get_score_for_current_throw', side_effect=[3, 2])
	def test_to_see_if_frames_index_updated_accordingly_when_the_player_get_open_frame(self, mocked_function):
		bowling_game = BowlingGame.objects.create()
		bowling_game.throw_bowling_ball()
		bowling_game.throw_bowling_ball()
		self.assertEqual(bowling_game.frame_index_of_the_game, 1)

	@patch(BOWLING_GAME_MODULE_PATH + '.get_score_for_current_throw', side_effect=[5, 5, 3, 7, 4])
	def test_to_see_if_multiple_spare_updates_the_frame_accordingly(self, mocked_function):
		bowling_game = BowlingGame.objects.create()
		bowling_game.throw_bowling_ball()
		bowling_game.throw_bowling_ball()
		bowling_game.throw_bowling_ball()
		bowling_game.throw_bowling_ball()
		bowling_game.throw_bowling_ball()
		self.assertEqual(bowling_game.frames.all()[0].get_total_score(), 13)
		self.assertEqual(bowling_game.frames.all()[1].get_total_score(), 14)
		self.assertEqual(bowling_game.frames.all()[2].get_total_score(), 4)

	@patch(BOWLING_GAME_MODULE_PATH + '.get_score_for_current_throw', side_effect=[10, 10, 10, 5, 2])
	def test_to_see_if_multiple_strike_updates_the_frame_accordingly(self, mocked_function):
		bowling_game = BowlingGame.objects.create()
		bowling_game.throw_bowling_ball()
		bowling_game.throw_bowling_ball()
		bowling_game.throw_bowling_ball()
		bowling_game.throw_bowling_ball()
		bowling_game.throw_bowling_ball()
		self.assertEqual(bowling_game.frames.all()[0].get_total_score(), 30)
		self.assertEqual(bowling_game.frames.all()[1].get_total_score(), 25)
		self.assertEqual(bowling_game.frames.all()[2].get_total_score(), 17)
		self.assertEqual(bowling_game.frames.all()[3].get_total_score(), 7)

	@patch(BOWLING_GAME_MODULE_PATH + '.get_score_for_current_throw', side_effect=[10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 1, 2])
	def test_to_see_if_getting_a_strike_on_last_frame_updates_the_last_frame_accordingly(self, mocked_function):
		bowling_game = BowlingGame.objects.create()
		# throw 10 times, filling all 10 frames with last frame having a strike
		for i in range(10): bowling_game.throw_bowling_ball()

		bowling_game.throw_bowling_ball()
		bowling_game.throw_bowling_ball()

		self.assertEqual(bowling_game.frames.all()[9].get_total_score(), 13)
