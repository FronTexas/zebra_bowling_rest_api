from random import randint
from Frames import Frames

class StrikedFrame:
	def __init__(self, index):
		self.index = index 
		self.update_count = 0

class BowlingGame:
	def __init__(self):
		self.frames = Frames()
		self.current_frame_index = 0
		self.current_throw_index = 0
		self.spare_queue = []
		self.strike_queue = []

	def handle_spare(self, score):
		if len(self.spare_queue) == 0: return 

		peek = self.spare_queue[0]
		del self.spare_queue[0]

		self.frames[peek].extra_score += score


	def get_score_for_current_throw(self, frame_index_for_this_throw):
		score = 0
		if self.frames[frame_index_for_this_throw].is_first_throw:
			score = randint(0, 10)
		else: 
			# if it's a second throw, the score range is 0 to 10 - (how many pins the player knocked down in first throw)
			score = randint(0, 10 - self.frames[frame_index_for_this_throw].get_first_throw_score())
		return score

	def update_current_frame_index_if_necessary(self, is_having_a_strike, frame_index_for_this_throw):
		# strike, go to next index
		if is_having_a_strike:
			self.current_frame_index += 1
		
		# second throw already, go to next index
		if not self.frames[frame_index_for_this_throw].is_first_throw:
			self.current_frame_index += 1

	def handle_strike(self, score):
		if len(self.strike_queue) == 0: return 

		for i, striked_frame in enumerate(self.strike_queue):
			if abs(striked_frame.index - self.current_throw_index) <= 2: 
				self.frames[striked_frame.index].extra_score += score
				striked_frame.update_count += 1 

	def throw_bowling_ball(self):
		frame_index_for_this_throw = self.current_frame_index
		score = self.get_score_for_current_throw(frame_index_for_this_throw)

		self.frames[frame_index_for_this_throw].update_score(score)


		is_having_a_strike = score == 10 and self.frames[frame_index_for_this_throw].is_first_throw
		is_having_a_spare = not is_having_a_strike and (self.frames[frame_index_for_this_throw].get_first_throw_score() + self.frames[frame_index_for_this_throw].get_second_throw_score() == 10)
		
		self.update_current_frame_index_if_necessary(is_having_a_strike, frame_index_for_this_throw)		

		self.handle_strike(score)
		self.handle_spare(score)

		if is_having_a_strike:
			self.strike_queue.append(StrikedFrame(frame_index_for_this_throw))
		if is_having_a_spare:
			self.spare_queue.append(frame_index_for_this_throw)
		
		# mark that the player just did a first throw	
		if self.frames[frame_index_for_this_throw].is_first_throw:
			self.frames[frame_index_for_this_throw].toggle_is_first_throw()

		self.current_throw_index += 1

