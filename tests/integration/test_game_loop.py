import os
os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
os.environ.setdefault('SDL_AUDIODRIVER', 'dummy')

from collections import defaultdict
from unittest.mock import patch

import pygame
import pytest
from classes.asteroid import Asteroid
from classes.asteroidfield import AsteroidField
from classes.player import Player
from classes.shot import Shot
from classes.score_manager import ScoreManager
from classes.particle import Particle
from classes.shockwave import Shockwave
from classes.shield_powerup import ShieldPowerUp
from classes.shield_spawner import ShieldSpawner
from classes.speed_powerup import SpeedPowerUp
from classes.speed_powerup_spawner import SpeedPowerUpSpawner
from score_display import ScoreDisplay
from util.constants import (
    ASTEROID_MIN_RADIUS,
    COMBO_WINDOW_SECONDS,
    PLAYER_LIVES,
    PLAYER_SHOOT_SPEED,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    SHIELD_BREAK_INVULN_SECONDS,
    SHIELD_COLOR,
    SHIELD_DURATION_SECONDS,
    SHIELD_POWERUP_SPAWN_SECONDS,
    SHOT_RADIUS,
    SPEED_POWERUP_DURATION_SECONDS,
    SPEED_POWERUP_MULTIPLIER,
    SPEED_POWERUP_SPAWN_INTERVAL_SECONDS,
)


class TestGameLoop:
    def setup_method(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.NOFRAME)

        self.updatable = pygame.sprite.Group()
        self.drawable = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()
        self.shots = pygame.sprite.Group()
        self.shield_powerups = pygame.sprite.Group()
        self.speed_powerups = pygame.sprite.Group()

        Asteroid.containers = (self.asteroids, self.updatable, self.drawable)
        AsteroidField.containers = self.updatable
        Player.containers = (self.updatable, self.drawable)
        Shot.containers = (self.shots, self.updatable, self.drawable)
        Particle.containers = (self.updatable, self.drawable)
        Shockwave.containers = (self.updatable, self.drawable)
        ShieldPowerUp.containers = (self.shield_powerups, self.updatable, self.drawable)
        ShieldSpawner.containers = self.updatable
        SpeedPowerUp.containers = (self.speed_powerups, self.updatable, self.drawable)
        SpeedPowerUpSpawner.containers = self.updatable

        self.asteroid_field = AsteroidField()
        self.shield_spawner = ShieldSpawner()
        self.speed_powerup_spawner = SpeedPowerUpSpawner()
        self.player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.score_manager = ScoreManager()
        self.score_display = ScoreDisplay()
        self.score_display.update_high_score(self.score_manager.get_high_score())
        self.score_display.update_lives(PLAYER_LIVES)

    def teardown_method(self):
        for group in (self.updatable, self.drawable, self.asteroids, self.shots, self.shield_powerups, self.speed_powerups):
            group.empty()
        pygame.quit()

    def test_sixty_ticks_player_survives(self):
        dt = 1 / 60
        for _ in range(60):
            for entity in self.updatable:
                entity.update(dt)
            self.score_manager.update(dt)

        assert self.player.alive()
        assert self.score_manager.get_current_score() == 0
        assert self.score_manager.get_high_score() >= 0

    def test_shot_kills_asteroid_and_increments_score(self):
        asteroid = Asteroid(400, 300, ASTEROID_MIN_RADIUS)
        asteroid.velocity = pygame.Vector2(0, 0)

        shot = Shot(100, 300, SHOT_RADIUS)
        shot.velocity = pygame.Vector2(PLAYER_SHOOT_SPEED, 0)

        dt = 1 / 60
        collided = False
        # Shot travels ~300px at 500px/s -> ~36 ticks. Budget allows headroom.
        for _ in range(120):
            for entity in self.updatable:
                entity.update(dt)
            if asteroid.collides_with(shot):
                # Mirror main.py's shot/asteroid collision resolution.
                shot.kill()
                asteroid.split()
                self.score_manager.add_score(asteroid.radius)
                collided = True
                break

        assert collided, "shot never reached asteroid within tick budget"
        assert not asteroid.alive()
        assert self.score_manager.get_current_score() > 0

    def test_player_hit_decrements_lives(self):
        lives = PLAYER_LIVES
        asteroid = Asteroid(self.player.position.x, self.player.position.y, ASTEROID_MIN_RADIUS)
        asteroid.velocity = pygame.Vector2(0, 0)
        self.player.invulnerable_timer = 0

        dt = 1 / 60
        for entity in self.updatable:
            entity.update(dt)

        assert self.player.is_vulnerable()
        assert asteroid.collides_with(self.player)

        # Same gate as main.py:55 -- vulnerable + collision -> lives decrement.
        if self.player.is_vulnerable() and asteroid.collides_with(self.player):
            lives -= 1
        assert lives == PLAYER_LIVES - 1

    def test_respawn_grants_invulnerability(self):
        self.player.invulnerable_timer = 0
        assert self.player.is_vulnerable()

        self.player.respawn((100, 100))
        assert not self.player.is_vulnerable()

    def test_combo_resets_after_window(self):
        initial_multiplier = self.score_manager.get_combo_multiplier()

        self.score_manager.add_score(ASTEROID_MIN_RADIUS)
        self.score_manager.add_score(ASTEROID_MIN_RADIUS)
        assert self.score_manager.get_combo_multiplier() > initial_multiplier

        dt = 1 / 60
        elapsed = 0.0
        while elapsed <= COMBO_WINDOW_SECONDS:
            self.score_manager.update(dt)
            elapsed += dt

        assert self.score_manager.get_combo_multiplier() == 1

    def tick(self, seconds):
        dt = 1 / 60
        for _ in range(round(seconds / dt)):
            for entity in self.updatable:
                entity.update(dt)

    def resolve_shield_pickups(self):
        # Mirror main.py's shield pickup resolution.
        for shield_powerup in self.shield_powerups:
            if shield_powerup.collides_with(self.player):
                shield_powerup.pick_up(self.player)

    def resolve_asteroid_hit(self, asteroid, lives):
        # Mirror main.py's player/asteroid gate: an active shield absorbs the hit instead of a life.
        if self.player.is_vulnerable() and asteroid.collides_with(self.player):
            if not self.player.absorb_hit():
                lives -= 1
        return lives

    def test_shield_spawner_puts_visible_powerup_in_play(self):
        self.tick(SHIELD_POWERUP_SPAWN_SECONDS + 0.1)

        assert len(self.shield_powerups) == 1
        powerup = next(iter(self.shield_powerups))
        assert powerup in self.updatable
        assert powerup in self.drawable

        self.screen.fill("black")
        for entity in self.drawable:
            entity.draw(self.screen)
        shield_pixels = pygame.mask.from_threshold(self.screen, SHIELD_COLOR, (1, 1, 1, 255)).count()
        assert shield_pixels > 0

    def test_picked_up_shield_absorbs_asteroid_hit(self):
        lives = PLAYER_LIVES
        ShieldPowerUp(self.player.position.x, self.player.position.y)
        self.tick(1 / 60)
        self.resolve_shield_pickups()

        assert self.player.has_shield()
        assert len(self.shield_powerups) == 0

        asteroid = Asteroid(self.player.position.x, self.player.position.y, ASTEROID_MIN_RADIUS)
        asteroid.velocity = pygame.Vector2(0, 0)
        self.tick(1 / 60)
        lives = self.resolve_asteroid_hit(asteroid, lives)

        assert lives == PLAYER_LIVES
        assert not self.player.has_shield()
        assert not self.player.is_vulnerable()

    def test_hit_after_shield_breaks_costs_a_life(self):
        lives = PLAYER_LIVES
        self.player.activate_shield()
        asteroid = Asteroid(self.player.position.x, self.player.position.y, ASTEROID_MIN_RADIUS)
        asteroid.velocity = pygame.Vector2(0, 0)

        lives = self.resolve_asteroid_hit(asteroid, lives)
        assert lives == PLAYER_LIVES

        self.tick(SHIELD_BREAK_INVULN_SECONDS + 0.1)
        assert asteroid.collides_with(self.player)
        lives = self.resolve_asteroid_hit(asteroid, lives)
        assert lives == PLAYER_LIVES - 1

    def test_shield_expires_and_hits_cost_lives_again(self):
        lives = PLAYER_LIVES
        ShieldPowerUp(self.player.position.x, self.player.position.y)
        self.tick(1 / 60)
        self.resolve_shield_pickups()
        assert self.player.has_shield()

        self.tick(SHIELD_DURATION_SECONDS + 0.1)
        assert not self.player.has_shield()

        asteroid = Asteroid(self.player.position.x, self.player.position.y, ASTEROID_MIN_RADIUS)
        asteroid.velocity = pygame.Vector2(0, 0)
        lives = self.resolve_asteroid_hit(asteroid, lives)
        assert lives == PLAYER_LIVES - 1

    def test_speed_powerup_spawns_during_play(self):
        dt = 1 / 60
        # One tick past the interval so float accumulation can't land just short of it.
        for _ in range(round(SPEED_POWERUP_SPAWN_INTERVAL_SECONDS / dt) + 1):
            for entity in self.updatable:
                entity.update(dt)

        assert len(self.speed_powerups) == 1

    def test_collecting_speed_powerup_boosts_player_until_expiry(self):
        powerup = SpeedPowerUp(self.player.position.x, self.player.position.y)
        dt = 1 / 60

        def tick():
            for entity in self.updatable:
                entity.update(dt)
            # Mirror main.py's speed power-up pickup resolution.
            for speed_powerup in self.speed_powerups:
                if speed_powerup.collides_with(self.player):
                    speed_powerup.collect(self.player)

        tick()
        assert not powerup.alive()
        assert self.player.is_speed_boosted()

        boost_ticks = round(SPEED_POWERUP_DURATION_SECONDS / dt)
        for _ in range(boost_ticks - 1):
            tick()
        assert self.player.is_speed_boosted()

        for _ in range(2):
            tick()
        assert not self.player.is_speed_boosted()

    def test_speed_boost_makes_thrusting_ship_faster(self):
        dt = 1 / 60
        thrust_held = defaultdict(bool, {pygame.K_w: True})

        def speed_after_one_second_of_thrust():
            self.player.velocity = pygame.Vector2(0, 0)
            with patch('pygame.key.get_pressed', return_value=thrust_held):
                for _ in range(60):
                    for entity in self.updatable:
                        entity.update(dt)
            return self.player.velocity.length()

        normal_speed = speed_after_one_second_of_thrust()
        self.player.apply_speed_boost()
        boosted_speed = speed_after_one_second_of_thrust()

        assert normal_speed > 0
        assert boosted_speed == pytest.approx(normal_speed * SPEED_POWERUP_MULTIPLIER)

    def test_shield_absorbs_hit_without_ending_speed_boost(self):
        lives = PLAYER_LIVES
        ShieldPowerUp(self.player.position.x, self.player.position.y)
        SpeedPowerUp(self.player.position.x, self.player.position.y)
        self.tick(1 / 60)
        self.resolve_shield_pickups()
        # Mirror main.py's speed power-up pickup resolution.
        for speed_powerup in self.speed_powerups:
            if speed_powerup.collides_with(self.player):
                speed_powerup.collect(self.player)

        assert self.player.has_shield()
        assert self.player.is_speed_boosted()

        asteroid = Asteroid(self.player.position.x, self.player.position.y, ASTEROID_MIN_RADIUS)
        asteroid.velocity = pygame.Vector2(0, 0)
        lives = self.resolve_asteroid_hit(asteroid, lives)

        assert lives == PLAYER_LIVES
        assert not self.player.has_shield()
        assert self.player.is_speed_boosted()
