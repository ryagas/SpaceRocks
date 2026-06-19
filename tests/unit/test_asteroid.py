import unittest
from unittest.mock import patch
import pygame
from classes.asteroid import Asteroid
from util.constants import ASTEROID_MIN_RADIUS, SCREEN_WIDTH, SCREEN_HEIGHT


class TestAsteroidInit(unittest.TestCase):

    def test_position_set_on_init(self):
        a = Asteroid(100, 200, ASTEROID_MIN_RADIUS * 2)
        self.assertEqual(a.position, pygame.Vector2(100, 200))

    def test_radius_set_on_init(self):
        a = Asteroid(0, 0, ASTEROID_MIN_RADIUS * 2)
        self.assertEqual(a.radius, ASTEROID_MIN_RADIUS * 2)

    def test_velocity_zero_on_init(self):
        a = Asteroid(0, 0, ASTEROID_MIN_RADIUS)
        self.assertEqual(a.velocity, pygame.Vector2(0, 0))


class TestAsteroidMovement(unittest.TestCase):

    def test_update_advances_position(self):
        a = Asteroid(100, 100, ASTEROID_MIN_RADIUS)
        a.velocity = pygame.Vector2(50, 0)
        a.update(1.0)
        self.assertAlmostEqual(a.position.x, 150.0)
        self.assertAlmostEqual(a.position.y, 100.0)

    def test_update_zero_dt_no_movement(self):
        a = Asteroid(100, 100, ASTEROID_MIN_RADIUS)
        a.velocity = pygame.Vector2(100, 100)
        a.update(0)
        self.assertEqual(a.position, pygame.Vector2(100, 100))


class TestAsteroidScreenWrapping(unittest.TestCase):

    def test_wrap_left_edge(self):
        r = ASTEROID_MIN_RADIUS
        a = Asteroid(-r - 1, 300, r)
        a.wrap_position()
        self.assertAlmostEqual(a.position.x, SCREEN_WIDTH + r)

    def test_wrap_right_edge(self):
        r = ASTEROID_MIN_RADIUS
        a = Asteroid(SCREEN_WIDTH + r + 1, 300, r)
        a.wrap_position()
        self.assertAlmostEqual(a.position.x, -r)

    def test_wrap_top_edge(self):
        r = ASTEROID_MIN_RADIUS
        a = Asteroid(400, -r - 1, r)
        a.wrap_position()
        self.assertAlmostEqual(a.position.y, SCREEN_HEIGHT + r)

    def test_wrap_bottom_edge(self):
        r = ASTEROID_MIN_RADIUS
        a = Asteroid(400, SCREEN_HEIGHT + r + 1, r)
        a.wrap_position()
        self.assertAlmostEqual(a.position.y, -r)


class TestAsteroidSplitMinRadius(unittest.TestCase):

    @patch('classes.asteroid.log_event')
    @patch('classes.asteroid.create_explosion')
    def test_min_radius_asteroid_kills_self(self, mock_explosion, mock_log):
        group = pygame.sprite.Group()
        Asteroid.containers = (group,)
        try:
            a = Asteroid(300, 300, ASTEROID_MIN_RADIUS)
            group.add(a)
            a.split()
            self.assertNotIn(a, group)
        finally:
            Asteroid.containers = ()

    @patch('classes.asteroid.log_event')
    @patch('classes.asteroid.create_explosion')
    def test_min_radius_asteroid_produces_no_children(self, mock_explosion, mock_log):
        group = pygame.sprite.Group()
        Asteroid.containers = (group,)
        try:
            a = Asteroid(300, 300, ASTEROID_MIN_RADIUS)
            group.add(a)
            a.split()
            self.assertEqual(len(group), 0)
        finally:
            Asteroid.containers = ()

    @patch('classes.asteroid.log_event')
    @patch('classes.asteroid.create_explosion')
    def test_min_radius_asteroid_does_not_log_split(self, mock_explosion, mock_log):
        group = pygame.sprite.Group()
        Asteroid.containers = (group,)
        try:
            a = Asteroid(300, 300, ASTEROID_MIN_RADIUS)
            group.add(a)
            a.split()
            mock_log.assert_not_called()
        finally:
            Asteroid.containers = ()

    @patch('classes.asteroid.log_event')
    @patch('classes.asteroid.create_explosion')
    def test_min_radius_asteroid_calls_create_explosion(self, mock_explosion, mock_log):
        group = pygame.sprite.Group()
        Asteroid.containers = (group,)
        try:
            a = Asteroid(300, 300, ASTEROID_MIN_RADIUS)
            group.add(a)
            a.split()
            mock_explosion.assert_called_once()
        finally:
            Asteroid.containers = ()


class TestAsteroidSplitLarger(unittest.TestCase):

    @patch('classes.asteroid.log_event')
    @patch('classes.asteroid.create_explosion')
    def test_split_kills_parent(self, mock_explosion, mock_log):
        group = pygame.sprite.Group()
        Asteroid.containers = (group,)
        try:
            a = Asteroid(300, 300, ASTEROID_MIN_RADIUS * 2)
            group.add(a)
            a.split()
            self.assertNotIn(a, group)
        finally:
            Asteroid.containers = ()

    @patch('classes.asteroid.log_event')
    @patch('classes.asteroid.create_explosion')
    def test_split_creates_two_children(self, mock_explosion, mock_log):
        group = pygame.sprite.Group()
        Asteroid.containers = (group,)
        try:
            a = Asteroid(300, 300, ASTEROID_MIN_RADIUS * 2)
            group.add(a)
            a.split()
            self.assertEqual(len(group), 2)
        finally:
            Asteroid.containers = ()

    @patch('classes.asteroid.log_event')
    @patch('classes.asteroid.create_explosion')
    def test_children_have_correct_radius(self, mock_explosion, mock_log):
        group = pygame.sprite.Group()
        Asteroid.containers = (group,)
        try:
            parent_radius = ASTEROID_MIN_RADIUS * 2
            a = Asteroid(300, 300, parent_radius)
            group.add(a)
            a.split()
            expected_radius = parent_radius - ASTEROID_MIN_RADIUS
            for child in group:
                self.assertAlmostEqual(child.radius, expected_radius)
        finally:
            Asteroid.containers = ()

    @patch('classes.asteroid.log_event')
    @patch('classes.asteroid.create_explosion')
    def test_children_spawn_at_parent_position(self, mock_explosion, mock_log):
        group = pygame.sprite.Group()
        Asteroid.containers = (group,)
        try:
            a = Asteroid(300, 300, ASTEROID_MIN_RADIUS * 2)
            group.add(a)
            a.split()
            for child in group:
                self.assertAlmostEqual(child.position.x, 300)
                self.assertAlmostEqual(child.position.y, 300)
        finally:
            Asteroid.containers = ()

    @patch('classes.asteroid.log_event')
    @patch('classes.asteroid.create_explosion')
    def test_split_logs_asteroid_split(self, mock_explosion, mock_log):
        group = pygame.sprite.Group()
        Asteroid.containers = (group,)
        try:
            a = Asteroid(300, 300, ASTEROID_MIN_RADIUS * 2)
            group.add(a)
            a.split()
            mock_log.assert_called_once_with('asteroid_split')
        finally:
            Asteroid.containers = ()

    @patch('classes.asteroid.log_event')
    @patch('classes.asteroid.create_explosion')
    def test_split_calls_create_explosion_once(self, mock_explosion, mock_log):
        group = pygame.sprite.Group()
        Asteroid.containers = (group,)
        try:
            a = Asteroid(300, 300, ASTEROID_MIN_RADIUS * 2)
            group.add(a)
            a.split()
            mock_explosion.assert_called_once()
        finally:
            Asteroid.containers = ()

    @patch('classes.asteroid.random.uniform', return_value=45)
    @patch('classes.asteroid.log_event')
    @patch('classes.asteroid.create_explosion')
    def test_child1_velocity_magnitude_is_parent_times_1_2(self, mock_explosion, mock_log, mock_rand):
        group = pygame.sprite.Group()
        Asteroid.containers = (group,)
        try:
            a = Asteroid(300, 300, ASTEROID_MIN_RADIUS * 2)
            a.velocity = pygame.Vector2(100, 0)
            group.add(a)
            parent_speed = a.velocity.length()
            a.split()
            children = list(group)
            speeds = sorted(c.velocity.length() for c in children)
            # child1 = parent * 1.2, child2 = parent * 1.0
            self.assertAlmostEqual(speeds[0], parent_speed * 1.0, places=4)
            self.assertAlmostEqual(speeds[1], parent_speed * 1.2, places=4)
        finally:
            Asteroid.containers = ()


if __name__ == "__main__":
    unittest.main()
