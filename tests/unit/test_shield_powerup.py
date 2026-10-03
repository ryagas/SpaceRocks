import unittest
import pygame
from classes.player import Player
from classes.shield_powerup import ShieldPowerUp
from util.constants import (
    SHIELD_DURATION_SECONDS,
    SHIELD_POWERUP_LIFETIME_SECONDS,
    SHIELD_POWERUP_RADIUS,
)


class TestShieldPowerUpInit(unittest.TestCase):

    def test_position_set_on_init(self):
        p = ShieldPowerUp(100, 200)
        self.assertEqual(p.position, pygame.Vector2(100, 200))

    def test_radius_set_on_init(self):
        p = ShieldPowerUp(0, 0)
        self.assertEqual(p.radius, SHIELD_POWERUP_RADIUS)

    def test_lifetime_set_on_init(self):
        p = ShieldPowerUp(0, 0)
        self.assertEqual(p.lifetime, SHIELD_POWERUP_LIFETIME_SECONDS)


class TestShieldPowerUpLifetime(unittest.TestCase):

    def setUp(self):
        self.group = pygame.sprite.Group()
        ShieldPowerUp.containers = (self.group,)
        self.powerup = ShieldPowerUp(400, 300)

    def tearDown(self):
        ShieldPowerUp.containers = ()

    def test_update_counts_down_lifetime(self):
        self.powerup.update(1.0)
        self.assertAlmostEqual(self.powerup.lifetime, SHIELD_POWERUP_LIFETIME_SECONDS - 1.0)

    def test_stays_in_play_before_lifetime_elapses(self):
        self.powerup.update(SHIELD_POWERUP_LIFETIME_SECONDS - 0.1)
        self.assertIn(self.powerup, self.group)

    def test_disappears_when_lifetime_elapses(self):
        self.powerup.update(SHIELD_POWERUP_LIFETIME_SECONDS)
        self.assertNotIn(self.powerup, self.group)


class TestShieldPowerUpPickup(unittest.TestCase):

    def setUp(self):
        self.group = pygame.sprite.Group()
        ShieldPowerUp.containers = (self.group,)
        self.powerup = ShieldPowerUp(400, 300)
        self.player = Player(400, 300)

    def tearDown(self):
        ShieldPowerUp.containers = ()

    def test_player_touching_powerup_collides(self):
        self.assertTrue(self.powerup.collides_with(self.player))

    def test_player_away_from_powerup_does_not_collide(self):
        self.player.position = pygame.Vector2(800, 600)
        self.assertFalse(self.powerup.collides_with(self.player))

    def test_pick_up_activates_player_shield(self):
        self.powerup.pick_up(self.player)
        self.assertTrue(self.player.has_shield())

    def test_pick_up_gives_full_shield_duration(self):
        self.powerup.pick_up(self.player)
        self.assertAlmostEqual(self.player.shield_timer, SHIELD_DURATION_SECONDS)

    def test_pick_up_removes_powerup_from_play(self):
        self.powerup.pick_up(self.player)
        self.assertNotIn(self.powerup, self.group)


if __name__ == "__main__":
    unittest.main()
