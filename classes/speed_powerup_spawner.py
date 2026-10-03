import random

import pygame

from classes.speed_powerup import SpeedPowerUp
from util.constants import (
	SCREEN_HEIGHT,
	SCREEN_WIDTH,
	SPEED_POWERUP_SPAWN_INTERVAL_SECONDS,
	SPEED_POWERUP_SPAWN_MARGIN,
)


class SpeedPowerUpSpawner(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self, self.containers)
		self.spawn_timer = 0.0

	def update(self, dt):
		self.spawn_timer += dt
		if self.spawn_timer >= SPEED_POWERUP_SPAWN_INTERVAL_SECONDS:
			self.spawn_timer = 0.0
			x = random.uniform(SPEED_POWERUP_SPAWN_MARGIN, SCREEN_WIDTH - SPEED_POWERUP_SPAWN_MARGIN)
			y = random.uniform(SPEED_POWERUP_SPAWN_MARGIN, SCREEN_HEIGHT - SPEED_POWERUP_SPAWN_MARGIN)
			SpeedPowerUp(x, y)
