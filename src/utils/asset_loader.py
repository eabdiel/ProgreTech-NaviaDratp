import pygame
from pathlib import Path


def load_image(path: Path, size: tuple[int, int] | None = None) -> pygame.Surface:
    image = pygame.image.load(str(path)).convert_alpha()
    if size:
        image = pygame.transform.scale(image, size)
    return image
