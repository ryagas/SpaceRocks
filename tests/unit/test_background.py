import os
import tempfile
import unittest
import pygame
from util.background import load_background
from util.constants import SCREEN_WIDTH, SCREEN_HEIGHT, BACKGROUND_IMAGE

RED = (255, 0, 0)
GREEN = (0, 255, 0)
TARGET = (160, 90)


class TestLoadBackgroundCrop(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.tmpdir.cleanup()

    def assertMostlyGreen(self, color):
        # smoothscale blends a few pixels near color boundaries
        self.assertGreater(color.g, 200)
        self.assertLess(color.r, 50)

    def save(self, surface):
        path = os.path.join(self.tmpdir.name, "bg.png")
        pygame.image.save(surface, path)
        return path

    def test_wide_source_is_center_cropped(self):
        # 400x100 scales to 360x90 with green at x=90..270; the centered
        # 160px crop (x=100..260) keeps only green, so red edges are gone
        source = pygame.Surface((400, 100))
        source.fill(RED)
        source.fill(GREEN, pygame.Rect(100, 0, 200, 100))
        result = load_background(self.save(source), TARGET)
        self.assertEqual(result.get_size(), TARGET)
        self.assertMostlyGreen(result.get_at((80, 45)))
        self.assertMostlyGreen(result.get_at((5, 45)))
        self.assertMostlyGreen(result.get_at((154, 45)))

    def test_tall_source_is_center_cropped(self):
        # 100x400 scales to 160x640 with green at y=160..480; the centered
        # 90px crop (y=275..365) keeps only green
        source = pygame.Surface((100, 400))
        source.fill(RED)
        source.fill(GREEN, pygame.Rect(0, 100, 100, 200))
        result = load_background(self.save(source), TARGET)
        self.assertEqual(result.get_size(), TARGET)
        self.assertMostlyGreen(result.get_at((80, 45)))
        self.assertMostlyGreen(result.get_at((80, 5)))
        self.assertMostlyGreen(result.get_at((80, 84)))


class TestLoadBackgroundFallback(unittest.TestCase):

    def test_missing_file_returns_black_surface(self):
        result = load_background("does/not/exist.jpg", TARGET)
        self.assertEqual(result.get_size(), TARGET)
        self.assertEqual(result.get_at((0, 0))[:3], (0, 0, 0))
        self.assertEqual(result.get_at((80, 45))[:3], (0, 0, 0))


class TestLoadBackgroundAsset(unittest.TestCase):

    def test_real_background_fills_screen(self):
        result = load_background(BACKGROUND_IMAGE, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.assertEqual(result.get_size(), (SCREEN_WIDTH, SCREEN_HEIGHT))


if __name__ == "__main__":
    unittest.main()
