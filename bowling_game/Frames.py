class Frame: 
	def __init__(self):
		self.is_first_throw = True
		self.first_throw_score = 0
		self.second_throw_score = 0
		self.is_spare = False
		self.is_strike = False

	def update_score(self, score):
		_add_to_the_correct_throw(score)
		self.is_first_throw = False
		if _is_strike_on_first_throw(): self.is_strike = True 
		if _is_spare_after_second_throw(): self.is_spare = True

	def _add_to_the_correct_throw(self, score):
		if self.is_first_throw:
			self.first_throw_score += score 
		else:
			self.second_throw_score += score 

	def _is_strike_on_first_throw():
		return self.first_throw_score == 10

	def _is_spare_after_second_throw():
		return self.first_throw_score + self.second_throw_score == 10

	def is_strike(self):
		return self.is_strike

	def is_spare(self):
		return self.is_spare 

	def make_it_strike(self):
		self.is_strike = True 

	def make_it_spare(self):
		self.is_spare = True

	def get_first_throw__score(self):
		return self.first_throw_score

	def get_second_throw_score(self):
		return self.get_second_throw_score

	def get_total_score(self):
		return self.first_throw_score + self.second_throw_score

class Frames: 
	def __init__(self):
		self.frames = [Frame() for i in range(10)]
	




