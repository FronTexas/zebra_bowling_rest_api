# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from random import randint
from django.contrib import admin

class Frame(models.Model): 
	is_first_throw = models.BooleanField(default=True)
	first_throw_score = models.IntegerField(default=0)
	second_throw_score = models.IntegerField(default=0)
	extra_score = models.IntegerField(default=0)
	bowling_game = models.ForeignKey('BowlingGame', on_delete=models.CASCADE, related_name='frames')

	def update_score(self, score):
		self._add_to_the_correct_throw(score)
		self.save()

	def add_extra_score(self, score):
		self.extra_score += score
		self.save()

	def toggle_is_first_throw(self):
		self.is_first_throw = False
		self.save()

	def _add_to_the_correct_throw(self, score):
		if self.is_first_throw:
			self.first_throw_score += score 
		else:
			self.second_throw_score += score 
		self.save()

	def get_first_throw_score(self):
		return self.first_throw_score

	def get_second_throw_score(self):
		return self.second_throw_score

	def get_total_score(self):
		return self.first_throw_score + self.second_throw_score + self.extra_score

class StrikedFrame(models.Model):
	index = models.IntegerField(default=0)
	update_count = models.IntegerField(default=0)
	bowling_game = models.ForeignKey('BowlingGame', on_delete=models.CASCADE, related_name='striked_frames')

class BowlingGame(models.Model):
	frame_index_of_the_game = models.IntegerField(default=0)
	throw_index_of_the_game = models.IntegerField(default=0)
	spare_index = models.IntegerField(default= -1)

	def __init__(self):
		models.Model.__init__(self)

	def add_new_striked_frame(self, frame_index_of_the_throw):
		striked_frame = StrikedFrame(index = frame_index_of_the_throw, bowling_game=self)
		self.striked_frames.add(striked_frame, bulk=False)
		self.save()

	def handle_strike(self, score):
		if len(self.striked_frames.all()) == 0: return 

		for i, striked_frame in enumerate(self.striked_frames.all()):
			if abs(striked_frame.index - self.throw_index_of_the_game) <= 2: 
				self.frames.all()[striked_frame.index].add_extra_score(score)
				striked_frame.update_count += 1 
		self.save()

	def handle_spare(self, score):
		if self.spare_index == -1: return

		self.frames.all()[self.spare_index].add_extra_score(score)
		self.spare_index = -1
		self.save()

	def get_score_for_current_throw(self, frame_index_of_the_throw):
		score = 0
		if self.frames.all()[frame_index_of_the_throw].is_first_throw:
			score = randint(0, 10)
		else: 
			# if it's a second throw, the score range is 0 to 10 - (how many pins the player knocked down in first throw)
			score = randint(0, 10 - self.frames.all()[frame_index_of_the_throw].get_first_throw_score())
		return score

	def update_frame_index_of_the_game_if_necessary(self, is_a_strike, frame_index_of_the_throw):
		# strike, go to next index
		if is_a_strike:
			self.frame_index_of_the_game += 1
		
		# second throw already, go to next index
		if not self.frames.all()[frame_index_of_the_throw].is_first_throw:
			self.frame_index_of_the_game += 1
		self.save()

	def update_score_for_current_frame(self, frame_index, score):
		self.frames.all()[frame_index].update_score(score)
		self.save()

	def update_spare_index(self, frame_index_of_the_throw):
		self.spare_index = frame_index_of_the_throw
		self.save()

	def update_frames(self, score, frame_index_of_the_throw):
		self.update_score_for_current_frame(frame_index_of_the_throw, score)

		is_a_strike = score == 10
		is_a_spare = not is_a_strike and (self.frames.all()[frame_index_of_the_throw].get_first_throw_score() + self.frames.all()[frame_index_of_the_throw].get_second_throw_score() == 10)

		self.update_frame_index_of_the_game_if_necessary(is_a_strike, frame_index_of_the_throw)		

		self.handle_strike(score)
		self.handle_spare(score)

		if is_a_strike:
			self.add_new_striked_frame(frame_index_of_the_throw)
		if is_a_spare:
			self.update_spare_index(frame_index_of_the_throw)
		
		# mark that the player just did a first throw	
		if self.frames.all()[frame_index_of_the_throw].is_first_throw:
			self.frames.all()[frame_index_of_the_throw].toggle_is_first_throw()
		self.save()

	def throw_bowling_ball(self):
		frame_index_of_the_throw = self.frame_index_of_the_game
		score_of_the_throw = self.get_score_for_current_throw(frame_index_of_the_throw)
		self.update_frames(score_of_the_throw, frame_index_of_the_throw)
		self.throw_index_of_the_game += 1
		self.save()

