import unittest
from collections import defaultdict
from unittest.mock import patch, MagicMock
import pygame
from classes.player import Player
from classes.shot import Shot
from util.constants import (
    PLAYER_ACCELERATION,
    PLAYER_MAX_SPEED,
    PLAYER_RADIUS,
    PLAYER_RESPAWN_INVULN_SECONDS,
    PLAYER_SHOOT_COOLDOWN_SECONDS,
    PLAYER_TURN_SPEED,
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    SPEED_POWERUP_COLOR,
    SPEED_POWERUP_DURATION_SECONDS,
    SPEED_POWERUP_MULTIPLIER,
)


class TestPlayerRotation(unittest.TestCase):

    def setUp(self):
        self.player = Player(400, 300)

    def test_rotate_positive_dt_increases_rotation(self):
        self.player.rotate(1.0)
        self.assertAlmostEqual(self.player.rotation, PLAYER_TURN_SPEED * 1.0)

    def test_rotate_negative_dt_decreases_rotation(self):
        self.player.rotate(-1.0)
        self.assertAlmostEqual(self.player.rotation, -PLAYER_TURN_SPEED * 1.0)

    def test_rotate_accumulates(self):
        self.player.rotate(0.5)
        self.player.rotate(0.5)
        self.assertAlmostEqual(self.player.rotation, PLAYER_TURN_SPEED * 1.0)

    def test_rotate_zero_dt_no_change(self):
        self.player.rotation = 45
        self.player.rotate(0)
        self.assertAlmostEqual(self.player.rotation, 45)


class TestPlayerThrust(unittest.TestCase):

    def setUp(self):
        self.player = Player(400, 300)

    def test_thrust_changes_velocity(self):
        self.player.thrust(1.0)
        self.assertGreater(self.player.velocity.length(), 0)

    def test_thrust_direction_matches_rotation(self):
        self.player.rotation = 0
        self.player.thrust(1.0)
        direction = pygame.Vector2(0, 1).rotate(0)
        expected = direction * PLAYER_ACCELERATION * 1.0
        self.assertAlmostEqual(self.player.velocity.x, expected.x, places=4)
        self.assertAlmostEqual(self.player.velocity.y, expected.y, places=4)

    def test_thrust_capped_at_max_speed(self):
        for _ in range(200):
            self.player.thrust(0.1)
        self.assertLessEqual(self.player.velocity.length(), PLAYER_MAX_SPEED + 1e-6)

    def test_negative_thrust_reverses_direction(self):
        self.player.rotation = 0
        self.player.thrust(-1.0)
        self.assertLess(self.player.velocity.y, 0)


class TestPlayerShootCooldown(unittest.TestCase):

    def setUp(self):
        self.shot_group = pygame.sprite.Group()
        Shot.containers = (self.shot_group,)
        self.player = Player(400, 300)

    def tearDown(self):
        Shot.containers = ()

    def test_shoot_creates_shot_in_group(self):
        self.player.shoot()
        self.assertEqual(len(self.shot_group), 1)

    def test_shoot_sets_cooldown(self):
        self.player.shoot()
        self.assertAlmostEqual(self.player.shot_cooldown, PLAYER_SHOOT_COOLDOWN_SECONDS)

    def test_shoot_blocked_during_cooldown(self):
        self.player.shoot()
        self.player.shoot()
        self.assertEqual(len(self.shot_group), 1)

    def test_shoot_allowed_after_cooldown_expires(self):
        self.player.shoot()
        self.player.shot_cooldown = 0
        self.player.shoot()
        self.assertEqual(len(self.shot_group), 2)

    def test_initial_cooldown_is_zero(self):
        self.assertEqual(self.player.shot_cooldown, 0)


class TestPlayerInvulnerability(unittest.TestCase):

    def setUp(self):
        self.player = Player(400, 300)

    def test_initially_vulnerable(self):
        self.assertTrue(self.player.is_vulnerable())

    def test_respawn_sets_invulnerable(self):
        self.player.respawn((400, 300))
        self.assertFalse(self.player.is_vulnerable())

    def test_respawn_sets_correct_timer(self):
        self.player.respawn((400, 300))
        self.assertAlmostEqual(self.player.invulnerable_timer, PLAYER_RESPAWN_INVULN_SECONDS)

    def test_is_vulnerable_when_timer_zero(self):
        self.player.invulnerable_timer = 0
        self.assertTrue(self.player.is_vulnerable())

    def test_is_not_vulnerable_when_timer_positive(self):
        self.player.invulnerable_timer = 0.1
        self.assertFalse(self.player.is_vulnerable())

    def test_respawn_resets_position(self):
        self.player.respawn((100, 200))
        self.assertEqual(self.player.position, pygame.Vector2(100, 200))

    def test_respawn_resets_velocity(self):
        self.player.velocity = pygame.Vector2(100, 100)
        self.player.respawn((400, 300))
        self.assertEqual(self.player.velocity, pygame.Vector2(0, 0))

    def test_respawn_resets_rotation(self):
        self.player.rotation = 90
        self.player.respawn((400, 300))
        self.assertEqual(self.player.rotation, 0)


class TestPlayerScreenWrapping(unittest.TestCase):

    def test_wrap_left_edge(self):
        p = Player(-PLAYER_RADIUS - 1, 300)
        p.wrap_position()
        self.assertAlmostEqual(p.position.x, SCREEN_WIDTH + PLAYER_RADIUS)

    def test_wrap_right_edge(self):
        p = Player(SCREEN_WIDTH + PLAYER_RADIUS + 1, 300)
        p.wrap_position()
        self.assertAlmostEqual(p.position.x, -PLAYER_RADIUS)

    def test_wrap_top_edge(self):
        p = Player(400, -PLAYER_RADIUS - 1)
        p.wrap_position()
        self.assertAlmostEqual(p.position.y, SCREEN_HEIGHT + PLAYER_RADIUS)

    def test_wrap_bottom_edge(self):
        p = Player(400, SCREEN_HEIGHT + PLAYER_RADIUS + 1)
        p.wrap_position()
        self.assertAlmostEqual(p.position.y, -PLAYER_RADIUS)


class TestPlayerSpeedBoost(unittest.TestCase):

    def setUp(self):
        self.player = Player(400, 300)

    def update_without_input(self, dt):
        with patch('pygame.key.get_pressed', return_value=defaultdict(bool)):
            self.player.update(dt)

    def test_initially_not_boosted(self):
        self.assertFalse(self.player.is_speed_boosted())

    def test_apply_speed_boost_starts_full_duration(self):
        self.player.apply_speed_boost()
        self.assertTrue(self.player.is_speed_boosted())
        self.assertAlmostEqual(self.player.speed_boost_timer, SPEED_POWERUP_DURATION_SECONDS)

    def test_boosted_thrust_multiplies_acceleration(self):
        self.player.apply_speed_boost()
        self.player.thrust(1.0)
        expected = PLAYER_ACCELERATION * SPEED_POWERUP_MULTIPLIER * 1.0
        self.assertAlmostEqual(self.player.velocity.length(), expected, places=4)

    def test_boosted_top_speed_multiplies_max_speed(self):
        self.player.apply_speed_boost()
        for _ in range(200):
            self.player.thrust(0.1)
        expected = PLAYER_MAX_SPEED * SPEED_POWERUP_MULTIPLIER
        self.assertAlmostEqual(self.player.velocity.length(), expected, places=4)

    @patch('classes.player.pygame.draw.polygon')
    def test_boosted_ship_drawn_in_powerup_color(self, mock_polygon):
        self.player.apply_speed_boost()
        self.player.draw(None)
        self.assertEqual(mock_polygon.call_args.args[1], SPEED_POWERUP_COLOR)

    def test_boost_still_active_before_duration_ends(self):
        self.player.apply_speed_boost()
        self.update_without_input(SPEED_POWERUP_DURATION_SECONDS - 0.1)
        self.assertTrue(self.player.is_speed_boosted())

    def test_boost_expires_after_duration(self):
        self.player.apply_speed_boost()
        self.update_without_input(SPEED_POWERUP_DURATION_SECONDS)
        self.assertFalse(self.player.is_speed_boosted())
        self.assertEqual(self.player.speed_boost_timer, 0)

    def test_thrust_back_to_normal_after_expiry(self):
        self.player.apply_speed_boost()
        self.update_without_input(SPEED_POWERUP_DURATION_SECONDS)
        self.player.velocity = pygame.Vector2(0, 0)
        self.player.thrust(1.0)
        self.assertAlmostEqual(self.player.velocity.length(), PLAYER_ACCELERATION, places=4)

    def test_new_pickup_refreshes_remaining_time(self):
        self.player.apply_speed_boost()
        self.player.speed_boost_timer = 1.0
        self.player.apply_speed_boost()
        self.assertAlmostEqual(self.player.speed_boost_timer, SPEED_POWERUP_DURATION_SECONDS)

    def test_respawn_clears_speed_boost(self):
        self.player.apply_speed_boost()
        self.player.respawn((400, 300))
        self.assertFalse(self.player.is_speed_boosted())


if __name__ == "__main__":
    unittest.main()
