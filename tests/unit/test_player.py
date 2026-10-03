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
    SHIELD_BREAK_INVULN_SECONDS,
    SHIELD_COLOR,
    SHIELD_DURATION_SECONDS,
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


class TestPlayerShield(unittest.TestCase):

    def setUp(self):
        self.player = Player(400, 300)

    def test_initially_no_shield(self):
        self.assertFalse(self.player.has_shield())

    def test_activate_shield_turns_shield_on(self):
        self.player.activate_shield()
        self.assertTrue(self.player.has_shield())

    def test_activate_shield_sets_full_duration(self):
        self.player.activate_shield()
        self.assertAlmostEqual(self.player.shield_timer, SHIELD_DURATION_SECONDS)

    def test_activate_shield_refreshes_partly_used_shield(self):
        self.player.shield_timer = 1.0
        self.player.activate_shield()
        self.assertAlmostEqual(self.player.shield_timer, SHIELD_DURATION_SECONDS)

    def test_absorb_hit_with_shield_returns_true(self):
        self.player.activate_shield()
        self.assertTrue(self.player.absorb_hit())

    def test_absorb_hit_consumes_shield(self):
        self.player.activate_shield()
        self.player.absorb_hit()
        self.assertFalse(self.player.has_shield())

    def test_absorb_hit_grants_grace_invulnerability(self):
        self.player.activate_shield()
        self.player.absorb_hit()
        self.assertFalse(self.player.is_vulnerable())
        self.assertAlmostEqual(self.player.invulnerable_timer, SHIELD_BREAK_INVULN_SECONDS)

    def test_shield_absorbs_only_one_hit(self):
        self.player.activate_shield()
        self.player.absorb_hit()
        self.assertFalse(self.player.absorb_hit())

    def test_absorb_hit_without_shield_returns_false(self):
        self.assertFalse(self.player.absorb_hit())

    def test_absorb_hit_without_shield_leaves_player_vulnerable(self):
        self.player.absorb_hit()
        self.assertTrue(self.player.is_vulnerable())


@patch("pygame.key.get_pressed", return_value=defaultdict(bool))
class TestPlayerShieldExpiry(unittest.TestCase):

    def setUp(self):
        self.player = Player(400, 300)
        self.player.activate_shield()

    def test_shield_still_active_before_duration_elapses(self, _keys):
        self.player.update(SHIELD_DURATION_SECONDS - 0.1)
        self.assertTrue(self.player.has_shield())

    def test_shield_expires_when_duration_elapses(self, _keys):
        self.player.update(SHIELD_DURATION_SECONDS)
        self.assertFalse(self.player.has_shield())

    def test_shield_expires_over_many_frames(self, _keys):
        for _ in range(round((SHIELD_DURATION_SECONDS + 0.1) * 60)):
            self.player.update(1 / 60)
        self.assertFalse(self.player.has_shield())

    def test_shield_timer_does_not_go_negative(self, _keys):
        self.player.update(SHIELD_DURATION_SECONDS + 5)
        self.assertEqual(self.player.shield_timer, 0)

    def test_expired_shield_does_not_absorb_hit(self, _keys):
        self.player.update(SHIELD_DURATION_SECONDS)
        self.assertFalse(self.player.absorb_hit())
        self.assertTrue(self.player.is_vulnerable())


class TestPlayerShieldDraw(unittest.TestCase):

    def setUp(self):
        self.player = Player(100, 100)
        self.screen = pygame.Surface((200, 200))

    def count_shield_pixels(self):
        return pygame.mask.from_threshold(self.screen, SHIELD_COLOR, (1, 1, 1, 255)).count()

    def test_draw_shows_shield_bubble_when_active(self):
        self.player.activate_shield()
        self.player.draw(self.screen)
        self.assertGreater(self.count_shield_pixels(), 0)

    def test_draw_shows_no_shield_bubble_without_shield(self):
        self.player.draw(self.screen)
        self.assertEqual(self.count_shield_pixels(), 0)


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
