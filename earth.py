import pygame


class Earth(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.health = 500
        self.image = pygame.image.load('earth.png')
        self.image = pygame.transform.scale(self.image, (300, 300))
        self.rect = self.image.get_rect()
        self.rect.center = [640, 360]