from BowlingGame import BowlingGame
from Frames import Frames



# testing handle spare 
bowling_game = BowlingGame()
bowling_game.frames[0].first_throw_score = 5
bowling_game.frames[0].second_throw_score = 5
bowling_game.spare_queue = [0]
bowling_game.handle_spare(1)
print bowling_game.frames[0].get_total_score() == 11
print len(bowling_game.spare_queue) == 0


# testing strike
bowling_game = BowlingGame()
bowling_game.frames[0].first_throw_score = 10 
bowling_game.strike_queue = [0]
bowling_game.handle_strike(5)
print bowling_game.frames[0].get_total_score() == 15 

bowling_game.handle_strike(5)
print bowling_game.frames[0].get_total_score() == 20
