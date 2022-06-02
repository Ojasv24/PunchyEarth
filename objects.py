import pygame
import pymunk


class objects(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, space) -> None:
        super().__init__()
        self.body = pymunk.Body()
        self.body.position = pos_x, pos_y
        self.shape = pymunk.Circle(self.body, 30)
        self.shape.elasticity = 1
        self.shape.density = 1
        self.body.mass = 1
        self.shape.collision_type = 2
        space.add(self.body, self.shape)
        
    
        
        
