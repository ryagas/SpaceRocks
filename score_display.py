import pygame
from util.constants import (
	SCORE_POSITION,
	SCORE_FONT_SIZE,
	SCORE_COLOR,
	COMBO_COLOR,
	COMBO_POSITION,
	HIGH_SCORE_COLOR,
	HIGH_SCORE_POSITION
	)

class ScoreDisplay:
	def __init__(self):
		pygame.font.init()
		self._text_color = SCORE_COLOR
		self._font_size = SCORE_FONT_SIZE
		self._position = SCORE_POSITION
		self._combo_position = COMBO_POSITION
		self._combo_color = COMBO_COLOR
		self._high_score_position = HIGH_SCORE_POSITION
		self._high_score_color = HIGH_SCORE_COLOR
		self._content = {
			'SCORE' : 0,
			'COMBO' : 1,
			'HIGH_SCORE' : 0
			}

	def update_score(self, value):
		self._content['SCORE'] = value

	def update_combo(self, value):
		self._content['COMBO'] = value

	def update_high_score(self, value):
		self._content['HIGH_SCORE'] = value

	def render_surface(self, screen):
		font = pygame.font.Font(None, self._font_size)
		score_text = f"SCORE: {self._content['SCORE']:,}"
		score_surface = font.render(score_text, True, self._text_color)
		screen.blit(score_surface, self._position)
		if self._content['COMBO'] >= 2:
			combo_text = f"COMBO: {self._content['COMBO']}"
			combo_surface = font.render(combo_text, True, self._combo_color)
			screen.blit(combo_surface, self._combo_position)
		high_score_text = f"HIGH SCORE: {self._content['HIGH_SCORE']:,}"
		high_score_surface = font.render(high_score_text, True, self._high_score_color)
		screen.blit(high_score_surface, self._high_score_position)
