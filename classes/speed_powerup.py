import pygame

from classes.circleshape import CircleShape
from util.constants import (
	LINE_WIDTH,
	SPEED_POWERUP_COLOR,
	SPEED_POWERUP_LIFETIME_SECONDS,
	SPEED_POWERUP_RADIUS,
)


class SpeedPowerUp(CircleShape):
	# Lightning bolt points, in units of the power-up radius around its center
	bolt_shape = [(0.25, -0.75), (-0.35, 0.1), (0, 0.1), (-0.25, 0.75), (0.35, -0.1), (0, -0.1)]

	def __init__(self, x, y):
		super().__init__(x, y, SPEED_POWERUP_RADIUS)
		self.lifetime = SPEED_POWERUP_LIFETIME_SECONDS

	def draw(self, screen):
		pygame.draw.circle(screen, SPEED_POWERUP_COLOR, self.position, self.radius, LINE_WIDTH)
		bolt = [self.position + pygame.Vector2(x, y) * self.radius for x, y in self.bolt_shape]
		pygame.draw.polygon(screen, SPEED_POWERUP_COLOR, bolt)

	def update(self, dt):
		self.lifetime -= dt
		if self.lifetime <= 0:
			self.kill()

	def collect(self, player):
		self.kill()
		player.apply_speed_boost()
