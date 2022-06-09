import pygame
import pymunk

from collision_handler import EARTH


class Earth(pygame.sprite.Sprite):
    def __init__(self, space, postion, size, group) -> None:
        super().__init__()
        # pygame
        self.image = pygame.image.load('./assets/earth.png')
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect()
        self.rect.center = postion

        # pymunk
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = postion
        self.shape = pymunk.Circle(self.body, size[0] / 2.5)
        self.shape.collision_type = EARTH
        self.shape.filter = pymunk.ShapeFilter(group=group)

        self.health = 100

        space.add(self.body, self.shape)

    def drawHealthBar(self, screen):
        myimage = pygame.image.load("./assets/earth_healthbar.png")
        myimage = pygame.transform.scale(myimage, (60, 40))
        imagerect = myimage.get_rect()
        imagerect.center = (30, 30)
        screen.blit(myimage, imagerect)
        pygame.draw.rect(screen, (5, 158, 28),
                         pygame.Rect((60, 20), (220, 28)), 2, 3)
        pygame.draw.rect(screen, (5, 158, 28),
                         pygame.Rect((65, 24), (self.health, 20)))
        

    def reduce_health(self, diff):
        self.health -= diff