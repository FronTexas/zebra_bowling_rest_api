from random import randint
from Frames import Frames

class BowlingGame:
	def __init__(self):
		self.frames = Frames()
		self.current_frame_index = 0
		self.spare_queue = []
		self.strike_queue = []

	def handle_spare(self, score):
		if len(self.spare_queue) == 0: return 

		peek = self.spare_queue[0]
		del self.spare_queue[0]

		self.frames[peek].extra_score += score

	def handle_strike(self, score):
		if len(self.strike_queue) == 0: return 

		peek = self.strike_queue[0]

		self.frames[peek].extra_score += score

		

	def throw_bowling_ball(self):
		if self.frames[self.current_frame_index].is_first_throw:
			score = randint(0, 10)
		else: 
			score = randint(0, 10 - self.frames[self.current_frame_index].get_first_throw_score())

		# second throw already, go to next index
		if not self.frames[self.current_frame_index].is_first_throw:
			self.current_frame_index += 1

		# strike
		if score == 10 and self.frames[self.current_frame_index].is_first_throw:
			self.current_frame_index += 1

		self.frames[self.current_frame_index].update_score(score)

		if self.frames[self.current_frame_index].get_first_throw_score() + self.frames[self.current_frame_index].get_first_throw_score() == 10: 
			self.handle_spare(score)

		if self.frames[self.current_frame_index].get_first_throw_score() == 10: 
			self.handle_strike(score)




		













