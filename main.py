import sys
import pygame
from asteroid import Asteroid
from asteroidfield import AsteroidField
from logger import log_event, log_state
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from player import Player

def main():
    print("Starting Asteroids with pygame version: ", pygame.version.ver)
    print(f'Screen width: {SCREEN_WIDTH}, Screen height: {SCREEN_HEIGHT}')

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()

    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = updatable
    Player.containers = (updatable, drawable)

    asteroid_field = AsteroidField()
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        screen.fill("black")
        for entity in updatable:
            entity.update(dt)
        for entity in drawable:
            entity.draw(screen)
        for rock in asteroids:
            if rock.collides_with(player):
                log_event('player_hit')
                print('Game over!')
                sys.exit()
        pygame.display.flip()
        dt = clock.tick(60) / 1000  # Convert milliseconds to seconds


if __name__ == "__main__":
    main()
