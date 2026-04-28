import random

import pygame

from classes.circleshape import CircleShape
from classes.particle import Particle
from classes.shot import Shot
from util.constants import (
	LINE_WIDTH,
	PLAYER_ACCELERATION,
	PLAYER_DRAG,
	PLAYER_MAX_SPEED,
	PLAYER_RADIUS,
	PLAYER_RESPAWN_INVULN_SECONDS,
	PLAYER_SHOOT_COOLDOWN_SECONDS,
	PLAYER_SHOOT_SPEED,
	PLAYER_THRUST_PARTICLES,
	PLAYER_TURN_SPEED,
	SHOT_RADIUS,
)


class Player(CircleShape):
	def __init__(self, x, y):
		super().__init__(x, y, PLAYER_RADIUS)
		self.rotation = 0
		self.shot_cooldown = 0
		self.invulnerable_timer = 0

	# in the Player class
	def triangle(self):
		forward = pygame.Vector2(0, 1).rotate(self.rotation)
		right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
		a = self.position + forward * self.radius
		b = self.position - forward * self.radius - right
		c = self.position - forward * self.radius + right
		return [a, b, c]
	
	def draw(self, screen):
		if self.invulnerable_timer > 0:
			blink_on = int(self.invulnerable_timer * 10) % 2 == 0
			if not blink_on:
				return
		pygame.draw.polygon(screen, "white", self.triangle(), LINE_WIDTH)

	def rotate(self, dt):
		self.rotation += PLAYER_TURN_SPEED * dt

	def update(self, dt):
		keys = pygame.key.get_pressed()
		self.shot_cooldown -= dt
		self.invulnerable_timer = max(0, self.invulnerable_timer - dt)

		if keys[pygame.K_a]:
			self.rotate(-dt)
		if keys[pygame.K_d]:
			self.rotate(dt)
		if keys[pygame.K_w]:
			self.thrust(dt)
			self.emit_thrust_particles()
		if keys[pygame.K_s]:
			self.thrust(-dt * 0.6)
		if keys[pygame.K_SPACE]:
			self.shoot()

		self.velocity *= PLAYER_DRAG ** dt
		self.position += self.velocity * dt
		self.wrap_position()

	def thrust(self, dt):
		direction = pygame.Vector2(0, 1).rotate(self.rotation)
		self.velocity += direction * PLAYER_ACCELERATION * dt
		if self.velocity.length() > PLAYER_MAX_SPEED:
			self.velocity.scale_to_length(PLAYER_MAX_SPEED)

	def emit_thrust_particles(self):
		back_direction = pygame.Vector2(0, -1).rotate(self.rotation)
		flame_colors = ["orange", "yellow", "red", (255, 200, 50), (255, 150, 30)]
		for _ in range(PLAYER_THRUST_PARTICLES):
			spread_direction = back_direction.rotate(random.uniform(-20, 20))
			particle_velocity = spread_direction * random.uniform(50, 120) + self.velocity * 0.3
			Particle(
				position=self.position + back_direction * self.radius,
				velocity=particle_velocity,
				lifetime=random.uniform(0.15, 0.35),
				radius=random.uniform(1, 2.5),
				color=random.choice(flame_colors),
			)
	
	def shoot(self):
		if self.shot_cooldown > 0:
			return
		else:
			self.shot_cooldown = PLAYER_SHOOT_COOLDOWN_SECONDS
			shot = Shot(self.position.x, self.position.y, SHOT_RADIUS)
			shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED

	def is_vulnerable(self):
		return self.invulnerable_timer <= 0

	def respawn(self, position):
		self.position = pygame.Vector2(position)
		self.velocity = pygame.Vector2(0, 0)
		self.rotation = 0
		self.invulnerable_timer = PLAYER_RESPAWN_INVULN_SECONDS
