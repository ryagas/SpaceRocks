import random
import pygame
from classes.particle import Particle
from classes.shockwave import Shockwave


def create_explosion(position, radius):
    count = int(radius * 0.8)
    for _ in range(count):
        angle = random.uniform(0, 360)
        speed = random.uniform(30, 150) * (radius / 40)
        velocity = pygame.Vector2(speed, 0).rotate(angle)
        offset_distance = random.uniform(0, radius * 0.3)
        offset = pygame.Vector2(offset_distance, 0).rotate(angle)
        particle_position = pygame.Vector2(position) + offset
        lifetime = random.uniform(0.3, 0.8)
        particle_radius = random.uniform(1, 2.5)
        Particle(particle_position, velocity, lifetime, particle_radius)
    Shockwave(position, max_radius=radius * 1.5, duration=0.25)
