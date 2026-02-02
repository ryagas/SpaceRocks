import pygame
from classes.circleshape import CircleShape
from util.constants import LINE_WIDTH, PLAYER_RADIUS, PLAYER_RESPAWN_INVULN_SECONDS, PLAYER_SHOOT_COOLDOWN_SECONDS, PLAYER_SHOOT_SPEED, PLAYER_SPEED, PLAYER_TURN_SPEED, SHOT_RADIUS
from classes.shot import Shot


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
			self.move(dt)
		if keys[pygame.K_s]:
			self.move(-dt)
		if keys[pygame.K_SPACE]:
			self.shoot()

	def move(self, dt):
		unit_vector = pygame.Vector2(0, 1)
		rotated_vector = unit_vector.rotate(self.rotation)
		rotated_with_speed_vector = rotated_vector * PLAYER_SPEED * dt
		self.position += rotated_with_speed_vector
	
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
