import pygame


class Shockwave(pygame.sprite.Sprite):
    def __init__(self, position, max_radius, duration=0.3):
        super().__init__(self.containers)
        self.position = pygame.Vector2(position)
        self.max_radius = max_radius
        self.duration = duration
        self.elapsed = 0

    def update(self, dt):
        self.elapsed += dt
        if self.elapsed >= self.duration:
            self.kill()

    def draw(self, screen):
        progress = self.elapsed / self.duration
        current_radius = self.max_radius * progress
        line_width = max(1, int(2 * (1 - progress)))
        brightness = int(255 * (1 - progress))
        color = pygame.Color(brightness, brightness, brightness)
        pygame.draw.circle(screen, color, self.position, current_radius, line_width)
