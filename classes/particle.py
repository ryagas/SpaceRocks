import pygame


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
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.kill()

    def draw(self, screen):
        fade_ratio = max(0, self.lifetime / self.max_lifetime)
        brightness = int(40 + 215 * fade_ratio)
        color = pygame.Color(brightness, brightness, brightness)
        pygame.draw.circle(screen, color, self.position, self.radius)
