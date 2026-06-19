import unittest
import pygame
from classes.shot import Shot
from util.constants import SCREEN_WIDTH, SCREEN_HEIGHT, SHOT_RADIUS


class TestShotInit(unittest.TestCase):

    def test_position_set_on_init(self):
        s = Shot(100, 200, SHOT_RADIUS)
        self.assertEqual(s.position, pygame.Vector2(100, 200))

    def test_radius_set_on_init(self):
        s = Shot(0, 0, SHOT_RADIUS)
        self.assertEqual(s.radius, SHOT_RADIUS)

    def test_velocity_zero_on_init(self):
        s = Shot(0, 0, SHOT_RADIUS)
        self.assertEqual(s.velocity, pygame.Vector2(0, 0))


class TestShotMovement(unittest.TestCase):

    def setUp(self):
        self.shot = Shot(100, 100, SHOT_RADIUS)

    def test_update_advances_position_by_velocity_times_dt(self):
        self.shot.velocity = pygame.Vector2(50, 0)
        self.shot.update(1.0)
        self.assertAlmostEqual(self.shot.position.x, 150.0)
        self.assertAlmostEqual(self.shot.position.y, 100.0)

    def test_update_zero_dt_does_not_move(self):
        self.shot.velocity = pygame.Vector2(100, 200)
        self.shot.update(0)
        self.assertEqual(self.shot.position, pygame.Vector2(100, 100))

    def test_update_accumulates_correctly(self):
        self.shot.velocity = pygame.Vector2(0, 60)
        self.shot.update(0.5)
        self.shot.update(0.5)
        self.assertAlmostEqual(self.shot.position.y, 160.0)

    def test_update_negative_velocity_moves_backward(self):
        self.shot.velocity = pygame.Vector2(-30, 0)
        self.shot.update(2.0)
        self.assertAlmostEqual(self.shot.position.x, 40.0)


class TestShotScreenWrapping(unittest.TestCase):

    def test_wrap_left_edge(self):
        s = Shot(-SHOT_RADIUS - 1, 100, SHOT_RADIUS)
        s.wrap_position()
        self.assertAlmostEqual(s.position.x, SCREEN_WIDTH + SHOT_RADIUS)

    def test_wrap_right_edge(self):
        s = Shot(SCREEN_WIDTH + SHOT_RADIUS + 1, 100, SHOT_RADIUS)
        s.wrap_position()
        self.assertAlmostEqual(s.position.x, -SHOT_RADIUS)

    def test_wrap_top_edge(self):
        s = Shot(100, -SHOT_RADIUS - 1, SHOT_RADIUS)
        s.wrap_position()
        self.assertAlmostEqual(s.position.y, SCREEN_HEIGHT + SHOT_RADIUS)

    def test_wrap_bottom_edge(self):
        s = Shot(100, SCREEN_HEIGHT + SHOT_RADIUS + 1, SHOT_RADIUS)
        s.wrap_position()
        self.assertAlmostEqual(s.position.y, -SHOT_RADIUS)

    def test_no_wrap_when_on_screen(self):
        s = Shot(400, 300, SHOT_RADIUS)
        s.wrap_position()
        self.assertAlmostEqual(s.position.x, 400)
        self.assertAlmostEqual(s.position.y, 300)


if __name__ == "__main__":
    unittest.main()
