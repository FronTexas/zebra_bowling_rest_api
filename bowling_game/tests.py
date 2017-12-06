# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from mock import patch
from rest_framework import status
from rest_framework.test import APITestCase
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

	@patch(BOWLING_GAME_MODULE_PATH + '.get_score_for_current_throw', side_effect=[10, 10, 10, 5, 4])
	def test_to_see_if_multiple_strike_updates_the_frame_accordingly(self, mocked_function):
		bowling_game = BowlingGame.objects.create()
		bowling_game.throw_bowling_ball()
		bowling_game.throw_bowling_ball()
		bowling_game.throw_bowling_ball()
		bowling_game.throw_bowling_ball()
		bowling_game.throw_bowling_ball()
		self.assertEqual(bowling_game.frames.all()[0].get_total_score(), 30)
		self.assertEqual(bowling_game.frames.all()[1].get_total_score(), 25)
		self.assertEqual(bowling_game.frames.all()[2].get_total_score(), 19)
		self.assertEqual(bowling_game.frames.all()[3].get_total_score(), 9)

	@patch(BOWLING_GAME_MODULE_PATH + '.get_score_for_current_throw', side_effect=[10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 1, 2])
	def test_to_see_if_getting_a_strike_on_last_frame_updates_the_last_frame_accordingly(self, mocked_function):
		bowling_game = BowlingGame.objects.create()
		# throw 10 times, filling all 10 frames with last frame having a strike
		for i in range(10): bowling_game.throw_bowling_ball()

		bowling_game.throw_bowling_ball()
		bowling_game.throw_bowling_ball()

		self.assertEqual(bowling_game.frames.all()[9].get_total_score(), 13)

	@patch(BOWLING_GAME_MODULE_PATH + '.get_score_for_current_throw', side_effect=[10, 10, 10, 10, 10, 10, 10, 10, 10, 7, 3, 1])
	def test_to_see_if_getting_a_spare_on_last_frame_updates_the_last_frame_accordingly(self, mocked_function):
		bowling_game = BowlingGame.objects.create()
		
		# throw 9 times, filling all 9 frames with last frame having a strike
		for i in range(9): bowling_game.throw_bowling_ball()

		bowling_game.throw_bowling_ball()
		bowling_game.throw_bowling_ball()
		bowling_game.throw_bowling_ball()

		self.assertEqual(bowling_game.frames.all()[9].get_total_score(), 11)

class TestBowlingGameRestApi(APITestCase):

	def test_if_the_game_starts_with_empty_frames(self):
		url = ''
		empty_frames = {
			'0': {
				'first_throw_score':'',
				'second_throw_score':'',
				'third_throw_score':''
			}, 
			'1': {
				'first_throw_score':'',
				'second_throw_score':'',
				'third_throw_score':''
			}, 
			'2': {
				'first_throw_score':'',
				'second_throw_score':'',
				'third_throw_score':''
			}, 
			'3': {
				'first_throw_score':'',
				'second_throw_score':'',
				'third_throw_score':'' 
			}, 
			'4': {
				'first_throw_score':'',
				'second_throw_score':'',
				'third_throw_score':'' 
			}, 
			'5': {
				'first_throw_score':'',
				'second_throw_score':'',
				'third_throw_score':'' 
			}, 
			'6': {
				'first_throw_score':'',
				'second_throw_score':'',
				'third_throw_score':''
			}, 
			'7': {
				'first_throw_score':'',
				'second_throw_score':'',
				'third_throw_score':''
			}, 
			'8': {
				'first_throw_score':'',
				'second_throw_score':'',
				'third_throw_score':''
			}, 
			'9': {
				'first_throw_score':'',
				'second_throw_score':'',
				'third_throw_score':''
			}}
		response = self.client.get('/bowling_game/')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(json.loads(response.content), empty_frames)

	def test_if_POST_and_gets_an_open_frame_updates_the_frame_accordingly(self):
		url = ''
		expected_frames = {
			'0': {
				'first_throw_score':'',
				'second_throw_score':'',
				'third_throw_score':''
			}, 
			'1': {
				'first_throw_score':'',
				'second_throw_score':'',
				'third_throw_score':''
			}, 
			'2': {
				'first_throw_score':'',
				'second_throw_score':'',
				'third_throw_score':''
			}, 
			'3': {
				'first_throw_score':'',
				'second_throw_score':'',
				'third_throw_score':'' 
			}, 
			'4': {
				'first_throw_score':'',
				'second_throw_score':'',
				'third_throw_score':'' 
			}, 
			'5': {
				'first_throw_score':'',
				'second_throw_score':'',
				'third_throw_score':'' 
			}, 
			'6': {
				'first_throw_score':'',
				'second_throw_score':'',
				'third_throw_score':''
			}, 
			'7': {
				'first_throw_score':'',
				'second_throw_score':'',
				'third_throw_score':''
			}, 
			'8': {
				'first_throw_score':'',
				'second_throw_score':'',
				'third_throw_score':''
			}, 
			'9': {
				'first_throw_score':'',
				'second_throw_score':'',
				'third_throw_score':''
			}}
		expected_frames['0']['first_throw_score'] = '3'
		expected_frames['0']['second_throw_score'] = '2'
		self.client.post('/bowling_game/')
		response = self.client.get('/bowling_game/')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(json.loads(response.content), expected_frames)

	def test_if_POST_and_gets_a_strike_updates_the_frame_accordingly(self):
		url = ''
		expected_frames = {
			'0': {
				'first_throw_score':'',
				'second_throw_score':'',
				'third_throw_score':''
			}, 
			'1': {
				'first_throw_score':'',
				'second_throw_score':'',
				'third_throw_score':''
			}, 
			'2': {
				'first_throw_score':'',
				'second_throw_score':'',
				'third_throw_score':''
			}, 
			'3': {
				'first_throw_score':'',
				'second_throw_score':'',
				'third_throw_score':'' 
			}, 
			'4': {
				'first_throw_score':'',
				'second_throw_score':'',
				'third_throw_score':'' 
			}, 
			'5': {
				'first_throw_score':'',
				'second_throw_score':'',
				'third_throw_score':'' 
			}, 
			'6': {
				'first_throw_score':'',
				'second_throw_score':'',
				'third_throw_score':''
			}, 
			'7': {
				'first_throw_score':'',
				'second_throw_score':'',
				'third_throw_score':''
			}, 
			'8': {
				'first_throw_score':'',
				'second_throw_score':'',
				'third_throw_score':''
			}, 
			'9': {
				'first_throw_score':'',
				'second_throw_score':'',
				'third_throw_score':''
			}}
		expected_frames['0']['first_throw_score'] = 'X'
		self.client.post('/bowling_game/')
		response = self.client.get('/bowling_game/')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(json.loads(response.content), expected_frames)

	def test_if_POST_and_gets_a_spare_updates_the_frame_accordingly(self):
		url = ''
		expected_frames = {
			'0': {
				'first_throw_score':'',
				'second_throw_score':'',
				'third_throw_score':''
			}, 
			'1': {
				'first_throw_score':'',
				'second_throw_score':'',
				'third_throw_score':''
			}, 
			'2': {
				'first_throw_score':'',
				'second_throw_score':'',
				'third_throw_score':''
			}, 
			'3': {
				'first_throw_score':'',
				'second_throw_score':'',
				'third_throw_score':'' 
			}, 
			'4': {
				'first_throw_score':'',
				'second_throw_score':'',
				'third_throw_score':'' 
			}, 
			'5': {
				'first_throw_score':'',
				'second_throw_score':'',
				'third_throw_score':'' 
			}, 
			'6': {
				'first_throw_score':'',
				'second_throw_score':'',
				'third_throw_score':''
			}, 
			'7': {
				'first_throw_score':'',
				'second_throw_score':'',
				'third_throw_score':''
			}, 
			'8': {
				'first_throw_score':'',
				'second_throw_score':'',
				'third_throw_score':''
			}, 
			'9': {
				'first_throw_score':'',
				'second_throw_score':'',
				'third_throw_score':''
			}}
		expected_frames['0']['first_throw_score'] = '5'
		expected_frames['0']['first_throw_score'] = '/'
		self.client.post('/bowling_game/')
		response = self.client.get('/bowling_game/')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(json.loads(response.content), expected_frames)
