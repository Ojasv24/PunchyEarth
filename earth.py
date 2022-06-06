import pygame
import pymunk


class Earth(pygame.sprite.Sprite):
    def __init__(self, space, postion, size, group) -> None:
        super().__init__()
        # pygame
        self.image = pygame.image.load('earth.png')
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect()
        self.rect.center = postion

        # pymunk
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = postion
        self.shape = pymunk.Circle(self.body, size[0] / 2.5)
        self.shape.collision_type = 3
        self.shape.filter = pymunk.ShapeFilter(group=group)

        self.health = 500

        space.add(self.body, self.shape)
