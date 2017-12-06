# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from random import randint
from django.contrib import admin
from django.db.models.signals import post_save


class Frame(models.Model): 
	throw_index = models.IntegerField(default=0)
	first_throw_score = models.IntegerField(default=0)
	second_throw_score = models.IntegerField(default=0)
	third_throw_score = models.IntegerField(default=0)
	extra_score = models.IntegerField(default=0)
	bowling_game = models.ForeignKey('BowlingGame', on_delete=models.CASCADE, related_name='frames')

	def update_scores(self, score):
		FIRST_THROW = 0
		SECOND_THROW = 1
		THIRD_THROW = 2

		if self.throw_index == FIRST_THROW:
			self.first_throw_score = score 
		elif self.throw_index == SECOND_THROW: 
			self.second_throw_score = score 
		elif self.throw_index == THIRD_THROW:
			self.third_throw_score = score 

		self.throw_index += 1
		self.save()

	def add_extra_score(self, score):
		self.extra_score += score
		self.save()

	def get_first_throw_score(self):
		return self.first_throw_score

	def get_second_throw_score(self):
		return self.second_throw_score

	def get_third_throw_score(self):
		return self.third_throw_score

	def get_total_score(self):
		return self.first_throw_score + self.second_throw_score + self.third_throw_score + self.extra_score

class StrikedFrame(models.Model):
	index = models.IntegerField(default=0)
	bowling_game = models.ForeignKey('BowlingGame', on_delete=models.CASCADE, related_name='striked_frames')

class BowlingGame(models.Model):
	LAST_FRAME = 9
	frame_index_of_the_game = models.IntegerField(default=0)
	throw_index_of_the_game = models.IntegerField(default=0)
	current_number_of_pins = models.IntegerField(default=10)
	is_second_throw = models.BooleanField(default=False)
	

	spare_index = models.IntegerField(default= -1)

	@classmethod
	def post_create(cls, sender, instance, created, *args, **kwargs):
		if not created:
			return
		
		def initialized_frames_for_the_bowling_game_instance(instance):
			for i in range(10):
				frame = Frame()
				instance.frames.add(frame, bulk=False)

		initialized_frames_for_the_bowling_game_instance(instance)

	def throw_bowling_ball(self):
		frame_index_of_the_throw = self.frame_index_of_the_game
		score_of_the_throw = self.get_score_for_current_throw()
		self.current_number_of_pins -= score_of_the_throw
		self.update_frames(score_of_the_throw, frame_index_of_the_throw)
		self.reset_number_of_pins_if_necessary(score_of_the_throw, frame_index_of_the_throw)
		self.update_is_second_throw(score_of_the_throw)
		self.throw_index_of_the_game += 1
		self.save()

	def get_score_for_current_throw(self):
		return randint(0, self.current_number_of_pins)

	def update_frames(self, score, frame_index_of_the_throw):
		self.update_score_for_current_frame(frame_index_of_the_throw, score)

		is_a_strike = score == 10
		is_a_spare = not is_a_strike and self.current_number_of_pins == 0

		self.update_frame_index_of_the_game_if_necessary(is_a_strike, frame_index_of_the_throw)		

		if frame_index_of_the_throw != self.LAST_FRAME:
			self.handle_strike(score)
			self.handle_spare(score)

		if is_a_strike:
			self.add_new_striked_frame(frame_index_of_the_throw)
		if is_a_spare:
			self.set_spare_index(frame_index_of_the_throw)
		
		self.save()

	def update_score_for_current_frame(self, frame_index, score):
		self.frames.all()[frame_index].update_scores(score)
		self.save()

	def update_frame_index_of_the_game_if_necessary(self, is_a_strike, frame_index_of_the_throw):
		if self.frame_index_of_the_game == self.LAST_FRAME: return
		
		if is_a_strike or self.is_second_throw:
			self.frame_index_of_the_game += 1

		self.save()

	def handle_strike(self, score):
		if len(self.striked_frames.all()) == 0: return 

		for i, striked_frame in enumerate(self.striked_frames.all()):
			the_throw_is_two_away = abs(striked_frame.index - self.throw_index_of_the_game) <= 2
			if the_throw_is_two_away: 
				self.frames.all()[striked_frame.index].add_extra_score(score)
		self.save()

	def handle_spare(self, score):
		if self.spare_index == -1: return
		self.frames.all()[self.spare_index].add_extra_score(score)
		self.spare_index = -1
		self.save()

	def add_new_striked_frame(self, frame_index_of_the_throw):
		striked_frame = StrikedFrame(index = frame_index_of_the_throw, bowling_game=self)
		self.striked_frames.add(striked_frame, bulk=False)
		self.save()

	def set_spare_index(self, frame_index_of_the_throw):
		self.spare_index = frame_index_of_the_throw
		self.save()

	def reset_number_of_pins_if_necessary(self, score_of_the_throw, frame_index_of_the_throw):
		is_a_strike = score_of_the_throw == 10 
		the_game_has_move_to_next_frame = self.frame_index_of_the_game > frame_index_of_the_throw
		if is_a_strike or the_game_has_move_to_next_frame :
			self.current_number_of_pins = 10
		self.save()

	def update_is_second_throw(self, score_of_the_throw):
		is_strike = score_of_the_throw == 10

		# if it's a strike, the is_second_throw must reset to False
		if is_strike:
			self.is_second_throw = False 
		else:
			self.is_second_throw = not self.is_second_throw

post_save.connect(BowlingGame.post_create, sender=BowlingGame)