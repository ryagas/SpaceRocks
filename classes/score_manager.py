import json
import os
from util.constants import (
	ASTEROID_MAX_RADIUS,
	ASTEROID_MIN_RADIUS,
	SCORE_SMALL_ASTEROID,
	SCORE_MEDIUM_ASTEROID,
	SCORE_LARGE_ASTEROID,
	SCORE_MAX,
	HIGH_SCORE_FILE
)

class ScoreManager():
	def __init__(self):
		self.__current_score = 0
		self.__combo_multiplier = 1
		self.__combo_timer= 0.0
		self.__high_score = self._load_high_score()

	def add_score(self, asteroid_radius):
		self.__current_score += self._calculate_base_points(asteroid_radius) * self.get_combo_multiplier()
		self._update_combo()
		if self.__current_score > SCORE_MAX:
			self.__current_score = SCORE_MAX
		return
	
	def update(self, dt):
		self.__combo_timer -= dt
		if self.__combo_timer < 0.0:
			self.__combo_timer = 0.0
			self._reset_combo()

	
	def reset(self):
			self.__init__()
	
	def _update_combo(self):
		self.__combo_multiplier += 1
		self.__combo_timer = 2.0

	def _reset_combo(self):
		self.__combo_multiplier = 1
		self.__combo_timer = 0.0

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

	def get_high_score(self):
		return self.__high_score

	def check_and_save_high_score(self):
		"""Check if current score is a new high score and save if it is."""
		if self.__current_score > self.__high_score:
			self.__high_score = self.__current_score
			self._save_high_score()
			return True
		return False

	def _load_high_score(self):
		"""Load high score from file, return 0 if file doesn't exist."""
		if os.path.exists(HIGH_SCORE_FILE):
			try:
				with open(HIGH_SCORE_FILE, 'r') as f:
					data = json.load(f)
					return data.get('high_score', 0)
			except (json.JSONDecodeError, IOError):
				return 0
		return 0

	def _save_high_score(self):
		"""Save high score to file."""
		try:
			with open(HIGH_SCORE_FILE, 'w') as f:
				json.dump({'high_score': self.__high_score}, f)
		except IOError:
			pass  # Silently fail if we can't save


