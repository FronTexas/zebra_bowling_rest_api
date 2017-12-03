from BowlingGame import BowlingGame
from Frames import Frames


bowling_game = BowlingGame()

# testing handle spare 
bowling_game.frames[0].first_throw_score = 5
bowling_game.frames[0].second_throw_score = 5
bowling_game.spare_queue = [0]
bowling_game.handle_spare(1)
print bowling_game.frames[0].get_total_score() == 11
