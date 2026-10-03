import pygame

from classes.circleshape import CircleShape
from util.constants import (
	LINE_WIDTH,
	SHIELD_COLOR,
	SHIELD_POWERUP_LIFETIME_SECONDS,
	SHIELD_POWERUP_RADIUS,
	SHIELD_WARNING_SECONDS,
)


class ShieldPowerUp(CircleShape):
	def __init__(self, x, y):
		super().__init__(x, y, SHIELD_POWERUP_RADIUS)
		self.lifetime = SHIELD_POWERUP_LIFETIME_SECONDS

	def draw(self, screen):
		if self.lifetime < SHIELD_WARNING_SECONDS:
			blink_on = int(self.lifetime * 10) % 2 == 0
			if not blink_on:
				return
		pygame.draw.circle(screen, SHIELD_COLOR, self.position, self.radius, LINE_WIDTH)
		pygame.draw.circle(screen, SHIELD_COLOR, self.position, self.radius / 2, LINE_WIDTH)

	def update(self, dt):
		self.lifetime -= dt
		if self.lifetime <= 0:
			self.kill()

	def pick_up(self, player):
		player.activate_shield()
		self.kill()
