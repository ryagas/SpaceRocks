import unittest
import pygame
from classes.shield_powerup import ShieldPowerUp
from classes.shield_spawner import ShieldSpawner
from util.constants import (
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    SHIELD_POWERUP_RADIUS,
    SHIELD_POWERUP_SPAWN_SECONDS,
)


class TestShieldSpawner(unittest.TestCase):

    def setUp(self):
        self.powerups = pygame.sprite.Group()
        ShieldPowerUp.containers = (self.powerups,)
        ShieldSpawner.containers = ()
        self.spawner = ShieldSpawner()

    def tearDown(self):
        ShieldPowerUp.containers = ()
        ShieldSpawner.containers = ()

    def test_no_spawn_before_interval_elapses(self):
        self.spawner.update(SHIELD_POWERUP_SPAWN_SECONDS)
        self.assertEqual(len(self.powerups), 0)

    def test_spawns_one_powerup_after_interval(self):
        self.spawner.update(SHIELD_POWERUP_SPAWN_SECONDS + 0.1)
        self.assertEqual(len(self.powerups), 1)

    def test_timer_accumulates_across_updates(self):
        self.spawner.update(SHIELD_POWERUP_SPAWN_SECONDS / 2)
        self.spawner.update(SHIELD_POWERUP_SPAWN_SECONDS / 2 + 0.1)
        self.assertEqual(len(self.powerups), 1)

    def test_spawn_resets_timer(self):
        self.spawner.update(SHIELD_POWERUP_SPAWN_SECONDS + 0.1)
        self.assertEqual(self.spawner.spawn_timer, 0)

    def test_spawned_powerups_are_fully_on_screen(self):
        for _ in range(50):
            self.spawner.update(SHIELD_POWERUP_SPAWN_SECONDS + 0.1)
        self.assertEqual(len(self.powerups), 50)
        for powerup in self.powerups:
            self.assertGreaterEqual(powerup.position.x, SHIELD_POWERUP_RADIUS)
            self.assertLessEqual(powerup.position.x, SCREEN_WIDTH - SHIELD_POWERUP_RADIUS)
            self.assertGreaterEqual(powerup.position.y, SHIELD_POWERUP_RADIUS)
            self.assertLessEqual(powerup.position.y, SCREEN_HEIGHT - SHIELD_POWERUP_RADIUS)


if __name__ == "__main__":
    unittest.main()
