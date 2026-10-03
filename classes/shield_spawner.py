import random

import pygame

from classes.shield_powerup import ShieldPowerUp
from util.constants import (
	SCREEN_HEIGHT,
	SCREEN_WIDTH,
	SHIELD_POWERUP_RADIUS,
	SHIELD_POWERUP_SPAWN_SECONDS,
)


class ShieldSpawner(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self, self.containers)
		self.spawn_timer = 0.0

	def update(self, dt):
		self.spawn_timer += dt
		if self.spawn_timer > SHIELD_POWERUP_SPAWN_SECONDS:
			self.spawn_timer = 0
			x = random.uniform(SHIELD_POWERUP_RADIUS, SCREEN_WIDTH - SHIELD_POWERUP_RADIUS)
			y = random.uniform(SHIELD_POWERUP_RADIUS, SCREEN_HEIGHT - SHIELD_POWERUP_RADIUS)
			ShieldPowerUp(x, y)
