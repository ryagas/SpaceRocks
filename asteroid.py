import random
import pygame
from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS, LINE_WIDTH
from logger import log_event


class Asteroid(CircleShape):
	def __init__(self, x, y, radius):
		super().__init__(x, y, radius)

	# draw the asteroid using pygame.draw.circle
	def draw(self, screen):
		pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)

	def update(self, dt):
		self.position += self.velocity * dt

	def split(self):
		self.kill()
		if self.radius <= ASTEROID_MIN_RADIUS:
			return
		log_event('asteroid_split')
		split_angle = random.uniform(20, 50)
		first_velocity = self.velocity.rotate(split_angle)
		second_velocity = self.velocity.rotate(-split_angle)
		new_radius = self.radius - ASTEROID_MIN_RADIUS
		child1 = Asteroid(self.position.x, self.position.y, new_radius)
		child2 = Asteroid(self.position.x, self.position.y, new_radius)
		child1.velocity = first_velocity * 1.2
		child2.velocity = second_velocity
