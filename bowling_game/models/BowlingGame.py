# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from random import randint
from Frame import Frame

class StrikedFrame:
	def __init__(self, index):
		self.index = index 
		self.update_count = 0

class BowlingGame(models.Model):
	frame_index_of_the_game = models.IntegerField(default=0)
	throw_index_of_the_game = models.IntegerField(default=0)
	spare_index = models.IntegerField(default= -1)

	def __init__(self):
		models.Model.__init__(self)
		self.frames = [Frame() for i in range(10)]
		self.strike_queue = []

	def handle_strike(self, score):
		if len(self.strike_queue) == 0: return 

		for i, striked_frame in enumerate(self.strike_queue):
			if abs(striked_frame.index - self.throw_index_of_the_game) <= 2: 
				self.frames[striked_frame.index].extra_score += score
				striked_frame.update_count += 1 

	def handle_spare(self, score):
		if self.spare_index == -1: return

		self.frames[self.spare_index].extra_score += score
		self.spare_index = -1
		self.save()

	def get_score_for_current_throw(self, frame_index_of_the_throw):
		score = 0
		if self.frames[frame_index_of_the_throw].is_first_throw:
			score = randint(0, 10)
		else: 
			# if it's a second throw, the score range is 0 to 10 - (how many pins the player knocked down in first throw)
			score = randint(0, 10 - self.frames[frame_index_of_the_throw].get_first_throw_score())
		return score

	def update_frame_index_of_the_game_if_necessary(self, is_a_strike, frame_index_of_the_throw):
		# strike, go to next index
		if is_a_strike:
			self.frame_index_of_the_game += 1
		
		# second throw already, go to next index
		if not self.frames[frame_index_of_the_throw].is_first_throw:
			self.frame_index_of_the_game += 1

	def update_score_for_current_frame(self, frame_index, score):
		self.frames[frame_index].update_score(score)

	def update_spare_index(self, frame_index_of_the_throw):
		self.spare_index = frame_index_of_the_throw
		self.save()

	def update_frames(self, score, frame_index_of_the_throw):
		self.update_score_for_current_frame(frame_index_of_the_throw, score)

		is_a_strike = score == 10
		is_a_spare = not is_a_strike and (self.frames[frame_index_of_the_throw].get_first_throw_score() + self.frames[frame_index_of_the_throw].get_second_throw_score() == 10)
		
		self.update_frame_index_of_the_game_if_necessary(is_a_strike, frame_index_of_the_throw)		

		self.handle_strike(score)
		self.handle_spare(score)

		if is_a_strike:
			self.strike_queue.append(StrikedFrame(frame_index_of_the_throw))
		if is_a_spare:
			self.update_spare_index(frame_index_of_the_throw)
			
		
		# mark that the player just did a first throw	
		if self.frames[frame_index_of_the_throw].is_first_throw:
			self.frames[frame_index_of_the_throw].toggle_is_first_throw()

	def throw_bowling_ball(self):
		frame_index_of_the_throw = self.frame_index_of_the_game
		score_of_the_throw = self.get_score_for_current_throw(frame_index_of_the_throw)


		self.update_frames(score_of_the_throw, frame_index_of_the_throw)
		self.throw_index_of_the_game += 1

