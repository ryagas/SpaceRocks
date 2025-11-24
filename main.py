import sys
import pygame
from classes.asteroid import Asteroid
from classes.asteroidfield import AsteroidField
from score_display import ScoreDisplay
from util.logger import log_event, log_score_added, log_state
from util.constants import SCREEN_WIDTH, SCREEN_HEIGHT
from classes.player import Player
from classes.shot import Shot
from classes.score_manager import ScoreManager

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
    shots = pygame.sprite.Group()

    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = updatable
    Player.containers = (updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    
    asteroid_field = AsteroidField()
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    score_manager = ScoreManager()
    score_display = ScoreDisplay()
    
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
            for shot in shots:
                if rock.collides_with(shot):
                    log_event('asteroid_shot')
                    shot.kill()
                    rock.split()
                    score_manager.add_score(rock.radius)
                    current_score = score_manager.get_current_score()
                    combo = score_manager.get_combo_multiplier()
                    score_display.update_score(current_score)
                    score_display.update_combo(combo)
                    log_score_added(
                        current_score, combo
                    )

        score_display.render_surface(screen)
        old_combo = score_manager.get_combo_multiplier()
        score_manager.update(dt)
        new_combo = score_manager.get_combo_multiplier()
        if old_combo != new_combo:
            score_display.update_combo(new_combo)

        pygame.display.flip()
        dt = clock.tick(60) / 1000  # Convert milliseconds to seconds


if __name__ == "__main__":
    main()
