import random
import pygame
from classes.circleshape import CircleShape
from classes.explosion import create_explosion
from util.constants import ASTEROID_LUMPINESS, ASTEROID_MIN_RADIUS, ASTEROID_VERTICES, LINE_WIDTH
from util.logger import log_event


class Asteroid(CircleShape):
	def __init__(self, x, y, radius):
		super().__init__(x, y, radius)
		# Outline stays inside the collision circle so screen wrapping never clips it
		self.vertex_scales = [random.uniform(1 - ASTEROID_LUMPINESS, 1) for _ in range(ASTEROID_VERTICES)]

	def outline(self):
		step = 360 / len(self.vertex_scales)
		return [
			self.position + pygame.Vector2(0, self.radius * scale).rotate(i * step)
			for i, scale in enumerate(self.vertex_scales)
		]

	def draw(self, screen):
		pygame.draw.polygon(screen, "white", self.outline(), LINE_WIDTH)

	def update(self, dt):
		self.position += self.velocity * dt
		self.wrap_position()

	def split(self):
		self.kill()
		create_explosion(self.position, self.radius)
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
