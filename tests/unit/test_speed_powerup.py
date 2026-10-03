import unittest
from unittest.mock import patch
import pygame
from classes.player import Player
from classes.speed_powerup import SpeedPowerUp
from classes.speed_powerup_spawner import SpeedPowerUpSpawner
from util.constants import (
    PLAYER_RADIUS,
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    SPEED_POWERUP_DURATION_SECONDS,
    SPEED_POWERUP_LIFETIME_SECONDS,
    SPEED_POWERUP_RADIUS,
    SPEED_POWERUP_SPAWN_INTERVAL_SECONDS,
    SPEED_POWERUP_SPAWN_MARGIN,
)


class TestSpeedPowerUpInit(unittest.TestCase):

    def test_position_set_on_init(self):
        powerup = SpeedPowerUp(100, 200)
        self.assertEqual(powerup.position, pygame.Vector2(100, 200))

    def test_radius_set_on_init(self):
        powerup = SpeedPowerUp(0, 0)
        self.assertEqual(powerup.radius, SPEED_POWERUP_RADIUS)

    def test_lifetime_set_on_init(self):
        powerup = SpeedPowerUp(0, 0)
        self.assertEqual(powerup.lifetime, SPEED_POWERUP_LIFETIME_SECONDS)


class TestSpeedPowerUpLifetime(unittest.TestCase):

    def setUp(self):
        self.group = pygame.sprite.Group()
        SpeedPowerUp.containers = (self.group,)
        self.powerup = SpeedPowerUp(400, 300)

    def tearDown(self):
        SpeedPowerUp.containers = ()

    def test_update_counts_down_lifetime(self):
        self.powerup.update(1.0)
        self.assertAlmostEqual(self.powerup.lifetime, SPEED_POWERUP_LIFETIME_SECONDS - 1.0)

    def test_stays_before_lifetime_ends(self):
        self.powerup.update(SPEED_POWERUP_LIFETIME_SECONDS - 0.1)
        self.assertIn(self.powerup, self.group)

    def test_disappears_when_lifetime_ends(self):
        self.powerup.update(SPEED_POWERUP_LIFETIME_SECONDS)
        self.assertNotIn(self.powerup, self.group)


class TestSpeedPowerUpPickup(unittest.TestCase):

    def setUp(self):
        self.group = pygame.sprite.Group()
        SpeedPowerUp.containers = (self.group,)
        self.player = Player(400, 300)

    def tearDown(self):
        SpeedPowerUp.containers = ()

    def test_player_touching_powerup_collides(self):
        powerup = SpeedPowerUp(400 + PLAYER_RADIUS, 300)
        self.assertTrue(powerup.collides_with(self.player))

    def test_player_out_of_reach_does_not_collide(self):
        powerup = SpeedPowerUp(400 + PLAYER_RADIUS + SPEED_POWERUP_RADIUS, 300)
        self.assertFalse(powerup.collides_with(self.player))

    def test_collect_removes_powerup(self):
        powerup = SpeedPowerUp(400, 300)
        powerup.collect(self.player)
        self.assertNotIn(powerup, self.group)

    def test_collect_boosts_player_for_full_duration(self):
        powerup = SpeedPowerUp(400, 300)
        powerup.collect(self.player)
        self.assertTrue(self.player.is_speed_boosted())
        self.assertAlmostEqual(self.player.speed_boost_timer, SPEED_POWERUP_DURATION_SECONDS)


class TestSpeedPowerUpSpawner(unittest.TestCase):

    def setUp(self):
        self.group = pygame.sprite.Group()
        SpeedPowerUp.containers = (self.group,)
        SpeedPowerUpSpawner.containers = ()
        self.spawner = SpeedPowerUpSpawner()

    def tearDown(self):
        SpeedPowerUp.containers = ()

    def test_no_spawn_before_interval(self):
        self.spawner.update(SPEED_POWERUP_SPAWN_INTERVAL_SECONDS - 0.1)
        self.assertEqual(len(self.group), 0)

    def test_spawns_one_powerup_at_interval(self):
        self.spawner.update(SPEED_POWERUP_SPAWN_INTERVAL_SECONDS)
        self.assertEqual(len(self.group), 1)

    def test_spawn_restarts_interval(self):
        self.spawner.update(SPEED_POWERUP_SPAWN_INTERVAL_SECONDS)
        self.spawner.update(SPEED_POWERUP_SPAWN_INTERVAL_SECONDS - 0.1)
        self.assertEqual(len(self.group), 1)
        self.spawner.update(0.1)
        self.assertEqual(len(self.group), 2)

    @patch('classes.speed_powerup_spawner.random.uniform', side_effect=lambda low, high: low)
    def test_spawn_range_starts_margin_from_top_left(self, mock_uniform):
        self.spawner.update(SPEED_POWERUP_SPAWN_INTERVAL_SECONDS)
        powerup = self.group.sprites()[0]
        self.assertEqual(
            powerup.position,
            pygame.Vector2(SPEED_POWERUP_SPAWN_MARGIN, SPEED_POWERUP_SPAWN_MARGIN),
        )

    @patch('classes.speed_powerup_spawner.random.uniform', side_effect=lambda low, high: high)
    def test_spawn_range_ends_margin_from_bottom_right(self, mock_uniform):
        self.spawner.update(SPEED_POWERUP_SPAWN_INTERVAL_SECONDS)
        powerup = self.group.sprites()[0]
        self.assertEqual(
            powerup.position,
            pygame.Vector2(
                SCREEN_WIDTH - SPEED_POWERUP_SPAWN_MARGIN,
                SCREEN_HEIGHT - SPEED_POWERUP_SPAWN_MARGIN,
            ),
        )


if __name__ == "__main__":
    unittest.main()
