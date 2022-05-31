import pygame
import pymunk


class objects(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, space) -> None:
        super().__init__()
        # self.image = pygame.image.load('earth.png')
        self.image = pygame.Surface([50,50])
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]
        
        
        self.body = pymunk.Body()
        self.body.position = pos_x, pos_y
        self.body.velocity = 10, 10
        self.shape = pymunk.Circle(self.body, 50)
        self.shape.elasticity = 5
        self.shape.density = 1
        self.shape.collision_type = 2
        space.add(self.body, self.shape)
        
    def update():
        pass
        
