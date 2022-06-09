from numpy import mat
import pygame
import pymunk
import math
from pygame import gfxdraw
from collision_handler import SHEILD


def cal_points(angle, radius, num_parts):
    points = [(0, radius)]

    angle_part = angle / num_parts

    for i in range(0, num_parts + 1):
        x = radius * math.sin(math.radians(angle_part * i))
        y = math.sqrt(math.pow(radius, 2) -
                      math.pow(x, 2))
        points.append((round(x, 4), round(y, 4)))

    return points


class shield(pygame.sprite.Sprite):
    def __init__(self, space, postion, radius, angle) -> None:
        super().__init__()
        pygame
        # self.image = pygame.image.load('./assets/shield.png')
        # self.image = pygame.transform.scale(self.image, (100,100))
        # self.rect = self.image.get_rect()
        # self.rect.center = postion
        
        #pymunk
        
        #body
        self.body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        self.body.position = postion
        
        #shape
        vertices = cal_points(angle, radius, 10)
        self.shape = pymunk.Poly(
            self.body, vertices)
        self.shape.collision_type = SHEILD
        self.shape.filter = pymunk.ShapeFilter(group=1)
        # self.shape.elasticity = 500
        
        #variable
        self.health = 200
        self.healthBar = self.health
            
        space.add(self.body, self.shape)

    def draw(self, screen):
        if not self.health <= 0:
            gfxdraw.filled_polygon(
                screen, self.get_vertices(), (232, 210, 9))

    def get_vertices(self):
        vertices = []
        for v in self.shape.get_vertices():
            x, y = v.rotated(self.shape.body.angle) + self.shape.body.position
            vertices.append((x, y))
        return vertices

    def moveR(self):
        self.body.angle += 0.1

    def moveL(self):
        self.body.angle -= 0.1

    def drawHealthBar(self, screen):
        myimage = pygame.image.load("./assets/shield_heathbar.png")
        imagerect = myimage.get_rect()
        imagerect.center = (30, 80)
        screen.blit(myimage, imagerect)
        pygame.draw.rect(screen, (205, 20, 255),
                         pygame.Rect((60, 70), ((self.healthBar + 20) / 1.5, 28)), 2, 3)
        pygame.draw.rect(screen, (205, 20, 255),
                         pygame.Rect((65, 74), (self.health / 1.5, 20)))

    def reduce_health(self, diff):

        self.health -= diff
