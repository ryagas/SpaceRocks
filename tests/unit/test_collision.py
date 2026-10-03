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

    def test_distance_exactly_equals_sum_of_radii_returns_false(self):
        # strict < means touching boundary (distance == sum of radii) is not a collision
        a = CircleShape(0, 0, 20)
        b = CircleShape(40, 0, 20)
        self.assertFalse(a.collides_with(b))

    def test_distance_just_inside_sum_of_radii_returns_true(self):
        a = CircleShape(0, 0, 20)
        b = CircleShape(39, 0, 20)
        self.assertTrue(a.collides_with(b))

    def test_both_radii_contribute_symmetrically(self):
        # Both radii are summed, so a.collides_with(b) == b.collides_with(a).
        # distance=10, radii=5+50=55 → collision in both directions.
        small = CircleShape(0, 0, 5)
        big = CircleShape(10, 0, 50)
        self.assertTrue(small.collides_with(big))
        self.assertTrue(big.collides_with(small))


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
