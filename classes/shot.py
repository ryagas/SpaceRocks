import pygame
from classes.circleshape import CircleShape
from util.constants import LINE_WIDTH, SHOT_RADIUS


class Shot(CircleShape):
	def __init__(self, x, y, radius):
		super().__init__(x, y, radius)

	def draw(self, screen):
		pygame.draw.circle(screen, "yellow", self.position, self.radius, LINE_WIDTH)

	def update(self, dt):
		self.position += self.velocity * dt
