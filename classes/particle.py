import pygame

from util.constants import SCREEN_WIDTH, SCREEN_HEIGHT


class Particle(pygame.sprite.Sprite):
    def __init__(self, position, velocity, lifetime, radius=1.5, color="white"):
        super().__init__(self.containers)
        self.position = pygame.Vector2(position)
        self.velocity = pygame.Vector2(velocity)
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.radius = radius
        self.color = color

    def update(self, dt):
        self.position += self.velocity * dt
        self.wrap_position()
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.kill()

    def wrap_position(self):
        # Wrap x position
        if self.position.x < -self.radius:
            self.position.x = SCREEN_WIDTH + self.radius
        elif self.position.x > SCREEN_WIDTH + self.radius:
            self.position.x = -self.radius
        
        # Wrap y position
        if self.position.y < -self.radius:
            self.position.y = SCREEN_HEIGHT + self.radius
        elif self.position.y > SCREEN_HEIGHT + self.radius:
            self.position.y = -self.radius

    def draw(self, screen):
        fade_ratio = max(0, self.lifetime / self.max_lifetime)
        if isinstance(self.color, str):
            base_color = pygame.Color(self.color)
        elif isinstance(self.color, pygame.Color):
            base_color = self.color
        else:
            base_color = pygame.Color(*self.color)
        faded_color = pygame.Color(
            int(base_color.r * fade_ratio),
            int(base_color.g * fade_ratio),
            int(base_color.b * fade_ratio),
        )
        pygame.draw.circle(screen, faded_color, self.position, self.radius)
