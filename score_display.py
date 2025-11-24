import pygame
from util.constants import ( 
	SCORE_POSITION,
	SCORE_FONT_SIZE,
	SCORE_COLOR,
	)

class ScoreDisplay:
	def __init__(self):
		pygame.font.init()
		self._text_color = SCORE_COLOR
		self._font_size = SCORE_FONT_SIZE
		self._position = SCORE_POSITION
		self._content = { 'SCORE' : 0 }

	def update_score(self, value):
		self._content['SCORE'] = value

	def render_surface(self, screen):
		font = pygame.font.Font(None, self._font_size)
		score_text = f"SCORE: {self._content['SCORE']:,}"
		surface = font.render(score_text, True, self._text_color)
		screen.blit(surface, self._position)
