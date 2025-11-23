from util.constants import (
	ASTEROID_MAX_RADIUS,
	ASTEROID_MIN_RADIUS,
	SCORE_SMALL_ASTEROID,
	SCORE_MEDIUM_ASTEROID,
	SCORE_LARGE_ASTEROID,
	SCORE_MAX
)

class ScoreManager():
	def __init__(self):
		self.__current_score = 0
		self.__combo_multiplier = 1
		self.__combo_timer= 0.0

	def add_score(self, asteroid_radius):
		self.__current_score += self._calculate_base_points(asteroid_radius) * self.get_combo_multiplier()
		if self.__current_score > SCORE_MAX:
			self.__current_score = SCORE_MAX
		return 
	
	def update(self, dt):
		# update combo timer each frame
		self.__combo_timer -= dt
		if self.__combo_timer < 0.0:
			self.__combo_timer = 0.0
			self._reset_combo()

	
	def reset(self):
			self.__init__()
	
	def _update_combo(self):
		self.__combo_multiplier += 1

	def _reset_combo(self):
		self.__combo_multiplier = 1

	def _calculate_base_points(self, radius):
		if radius == ASTEROID_MAX_RADIUS:
			return SCORE_LARGE_ASTEROID
		elif radius == ASTEROID_MIN_RADIUS:
			return SCORE_SMALL_ASTEROID
		else:
			return SCORE_MEDIUM_ASTEROID

	def get_current_score(self):
		return self.__current_score

	def get_combo_multiplier(self):
		return self.__combo_multiplier


