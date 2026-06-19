import unittest
import pygame
from classes.circleshape import CircleShape
from util.constants import SCREEN_WIDTH, SCREEN_HEIGHT


class TestCollidesWithOverlap(unittest.TestCase):

    def test_overlapping_circles_returns_true(self):
        a = CircleShape(0, 0, 20)
        b = CircleShape(10, 0, 20)
        self.assertTrue(a.collides_with(b))

    def test_coincident_circles_returns_true(self):
        a = CircleShape(100, 100, 20)
        b = CircleShape(100, 100, 20)
        self.assertTrue(a.collides_with(b))

    def test_non_overlapping_circles_returns_false(self):
        a = CircleShape(0, 0, 20)
        b = CircleShape(50, 0, 20)
        self.assertFalse(a.collides_with(b))

    def test_distance_exactly_equals_radius_returns_false(self):
        # collides_with uses strict < so touching boundary is False
        a = CircleShape(0, 0, 20)
        b = CircleShape(20, 0, 20)
        self.assertFalse(a.collides_with(b))

    def test_distance_just_inside_radius_returns_true(self):
        a = CircleShape(0, 0, 20)
        b = CircleShape(19, 0, 20)
        self.assertTrue(a.collides_with(b))

    def test_asymmetry_only_self_radius_matters(self):
        # collides_with checks distance_to < self.radius only — other.radius is ignored.
        # So a.collides_with(b) can differ from b.collides_with(a) when radii differ.
        small = CircleShape(0, 0, 5)
        big = CircleShape(10, 0, 50)
        self.assertFalse(small.collides_with(big))  # distance 10 >= small.radius 5
        self.assertTrue(big.collides_with(small))   # distance 10 < big.radius 50


class TestCollidesWithDiagonal(unittest.TestCase):

    def test_diagonal_overlap(self):
        a = CircleShape(0, 0, 30)
        b = CircleShape(20, 20, 30)
        # distance = sqrt(800) ≈ 28.3, which is < 30
        self.assertTrue(a.collides_with(b))

    def test_diagonal_no_overlap(self):
        a = CircleShape(0, 0, 20)
        b = CircleShape(30, 30, 20)
        # distance = sqrt(1800) ≈ 42.4, which is >= 20
        self.assertFalse(a.collides_with(b))


if __name__ == "__main__":
    unittest.main()
