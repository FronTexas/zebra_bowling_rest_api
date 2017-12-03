class Frame: 
	def __init__(self):
		self.is_first_throw = True
		self.first_throw_score = 0
		self.second_throw_score = 0
		self.extra_score = 0

	def update_score(self, score):
		self._add_to_the_correct_throw(score)

	def toggle_is_first_throw(self):
		self.is_first_throw = False

	def _add_to_the_correct_throw(self, score):
		if self.is_first_throw:
			self.first_throw_score += score 
		else:
			self.second_throw_score += score 

	def get_first_throw_score(self):
		return self.first_throw_score

	def get_second_throw_score(self):
		return self.second_throw_score

	def get_total_score(self):
		return self.first_throw_score + self.second_throw_score + self.extra_score

class Frames: 
	def __init__(self):
		self.frames = [Frame() for i in range(10)]

	def __getitem__(self, key):
		return self.frames[key]





