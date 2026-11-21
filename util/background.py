import math
import pygame

__all__ = ["load_background"]


def load_background(path, size):
    try:
        image = pygame.image.load(path)
    except (FileNotFoundError, pygame.error) as e:
        print(f"Warning: could not load background image {path}: {e}")
        fallback = pygame.Surface(size)
        fallback.fill("black")
        return fallback

    target_width, target_height = size
    width, height = image.get_size()

    # Scale to cover the target, then center-crop the overflow
    scale = max(target_width / width, target_height / height)
    scaled_size = (
        max(target_width, math.ceil(width * scale)),
        max(target_height, math.ceil(height * scale)),
    )
    scaled = pygame.transform.smoothscale(image, scaled_size)
    crop = pygame.Rect(
        (scaled_size[0] - target_width) // 2,
        (scaled_size[1] - target_height) // 2,
        target_width,
        target_height,
    )
    background = scaled.subsurface(crop).copy()

    if pygame.display.get_surface() is not None:
        background = background.convert()
    return background
