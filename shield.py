from numpy import mat
import pygame
import pymunk
import math


def cal_points(angle, radius, num_parts):
    points = [(0, radius)]

    angle_part = angle / num_parts

    for i in range(0, num_parts + 1):
        x = radius * math.sin(math.radians(angle_part * i))
        y = math.sqrt(math.pow(radius, 2) -
                      math.pow(x, 2))
        points.append((round(x, 4), round(y, 4)))

    return points


class Sheld(pygame.sprite.Sprite):
    def __init__(self, space, postion, radius, angle) -> None:
        super().__init__()
        # pygame
        # self.image = pygame.image.load('sheld.png')
        # # self.image = pygame.transform.scale(self.image, (100,100))
        # self.rect = self.image.get_rect()
        # self.rect.center = postion

        self.body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        vertices = cal_points(angle, radius, 10)
        self.body.position = postion
        self.shape = pymunk.Poly(
            self.body, vertices)
        self.shape.collision_type = 3
        self.shape.filter = pymunk.ShapeFilter(group=1)
        self.shape.elasticity = 500
        space.add(self.body, self.shape)

    def get_vertices(self):
        vertices = []
        for v in self.shape.get_vertices():
            x, y = v.rotated(self.shape.body.angle) + self.shape.body.position
            vertices.append((x, y))
        return vertices

    def moveR(self):
        # bx, by = self.body.position
        # self.body.position = (bx + 100, by)
        self.body.angle += 0.1

    def moveL(self):
        # bx, by = self.body.position
        # self.body.position = (bx - 100, by)
        self.body.angle -= 0.1
